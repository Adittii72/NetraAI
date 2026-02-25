"""
NetraAI Risk Scoring Engine
AI-powered risk assessment for entities
"""

import pandas as pd
import numpy as np
import networkx as nx
from typing import Dict, List, Tuple
from models import RiskCategory, RiskIndicator
import community as community_louvain

class RiskScoringEngine:
    def __init__(self, data: Dict[str, pd.DataFrame]):
        self.companies = data['companies']
        self.directors = data['directors']
        self.tenders = data['tenders']
        self.relationships = data['relationships']
        self.graph = self._build_networkx_graph()
        
    def _build_networkx_graph(self) -> nx.Graph:
        """Build NetworkX graph from relationships"""
        G = nx.Graph()
        
        # Add nodes
        for _, row in self.companies.iterrows():
            G.add_node(row['company_id'], type='company', **row.to_dict())
        
        for _, row in self.directors.iterrows():
            G.add_node(row['director_id'], type='director', **row.to_dict())
        
        for _, row in self.tenders.iterrows():
            G.add_node(row['tender_id'], type='tender', **row.to_dict())
        
        # Add edges
        for _, row in self.relationships.iterrows():
            G.add_edge(row['source_id'], row['target_id'], 
                      relationship_type=row['relationship_type'])
        
        return G
    
    def calculate_company_risk_score(self, company_id: str) -> Tuple[float, float, List[RiskIndicator]]:
        """Calculate risk score for a company"""
        indicators = []
        risk_factors = []
        
        company = self.companies[self.companies['company_id'] == company_id].iloc[0]
        
        # Factor 1: Shared directors with competing companies
        shared_director_score = self._check_shared_directors(company_id)
        if shared_director_score > 0.3:
            indicators.append(RiskIndicator(
                indicator="Shared Directors",
                severity="High" if shared_director_score > 0.6 else "Medium",
                description=f"Shares directors with {int(shared_director_score * 10)} competing bidders"
            ))
        risk_factors.append(shared_director_score * 0.25)
        
        # Factor 2: Tender win patterns
        win_pattern_score = self._check_tender_patterns(company_id)
        if win_pattern_score > 0.4:
            indicators.append(RiskIndicator(
                indicator="Suspicious Win Pattern",
                severity="High" if win_pattern_score > 0.7 else "Medium",
                description="Consecutive high-value tender wins above network mean"
            ))
        risk_factors.append(win_pattern_score * 0.30)
        
        # Factor 3: Network centrality
        centrality_score = self._calculate_centrality(company_id)
        if centrality_score > 0.5:
            indicators.append(RiskIndicator(
                indicator="High Network Centrality",
                severity="Medium",
                description="Dense cluster centrality indicating potential collusion"
            ))
        risk_factors.append(centrality_score * 0.20)
        
        # Factor 4: Shell company indicators
        shell_score = self._check_shell_indicators(company_id)
        if shell_score > 0.5:
            indicators.append(RiskIndicator(
                indicator="Shell Company Indicators",
                severity="High",
                description="Shared address and registration year with multiple entities"
            ))
        risk_factors.append(shell_score * 0.25)
        
        # Calculate final risk score
        risk_score = min(sum(risk_factors), 1.0)
        
        # Confidence score based on data availability
        confidence = self._calculate_confidence(company_id)
        
        return risk_score, confidence, indicators
    
    def _check_shared_directors(self, company_id: str) -> float:
        """Check for shared directors across competing companies"""
        # Get directors of this company
        director_rels = self.relationships[
            (self.relationships['target_id'] == company_id) &
            (self.relationships['relationship_type'] == 'DIRECTOR_OF')
        ]
        
        if len(director_rels) == 0:
            return 0.0
        
        director_ids = director_rels['source_id'].tolist()
        
        # Count companies sharing these directors
        shared_companies = set()
        for director_id in director_ids:
            other_companies = self.relationships[
                (self.relationships['source_id'] == director_id) &
                (self.relationships['relationship_type'] == 'DIRECTOR_OF') &
                (self.relationships['target_id'] != company_id)
            ]['target_id'].tolist()
            shared_companies.update(other_companies)
        
        # Normalize score
        return min(len(shared_companies) / 10.0, 1.0)
    
    def _check_tender_patterns(self, company_id: str) -> float:
        """Analyze tender winning patterns"""
        won_tenders = self.relationships[
            (self.relationships['source_id'] == company_id) &
            (self.relationships['relationship_type'] == 'WON')
        ]
        
        if len(won_tenders) == 0:
            return 0.0
        
        tender_ids = won_tenders['target_id'].tolist()
        tender_values = self.tenders[self.tenders['tender_id'].isin(tender_ids)]['contract_value']
        
        if len(tender_values) == 0:
            return 0.0
        
        # Check if average value is significantly above mean
        avg_value = tender_values.mean()
        overall_mean = self.tenders['contract_value'].mean()
        
        value_ratio = avg_value / overall_mean if overall_mean > 0 else 1.0
        
        # Check win frequency
        win_frequency = len(won_tenders) / len(self.tenders)
        
        return min((value_ratio - 1.0) * 0.5 + win_frequency * 2.0, 1.0)
    
    def _calculate_centrality(self, entity_id: str) -> float:
        """Calculate network centrality score"""
        if entity_id not in self.graph:
            return 0.0
        
        try:
            # Simplified centrality - just use degree
            degree = self.graph.degree(entity_id)
            max_degree = max(dict(self.graph.degree()).values()) if self.graph.number_of_nodes() > 0 else 1
            return degree / max_degree if max_degree > 0 else 0.0
        except:
            return 0.0
    
    def _check_shell_indicators(self, company_id: str) -> float:
        """Check for shell company indicators"""
        company = self.companies[self.companies['company_id'] == company_id].iloc[0]
        
        # Check for shared addresses
        same_address = self.companies[
            (self.companies['address'] == company['address']) &
            (self.companies['company_id'] != company_id)
        ]
        
        # Check for same registration year
        same_year = self.companies[
            (self.companies['registration_year'] == company['registration_year']) &
            (self.companies['company_id'] != company_id)
        ]
        
        address_score = min(len(same_address) / 5.0, 1.0)
        year_score = min(len(same_year) / 10.0, 0.5)
        
        return address_score + year_score
    
    def _calculate_confidence(self, entity_id: str) -> float:
        """Calculate confidence score based on data availability"""
        if entity_id not in self.graph:
            return 0.3
        
        # More connections = higher confidence
        degree = self.graph.degree(entity_id)
        return min(0.5 + (degree / 20.0), 1.0)
    
    def get_risk_category(self, risk_score: float) -> RiskCategory:
        """Convert risk score to category"""
        if risk_score >= 0.7:
            return RiskCategory.HIGH
        elif risk_score >= 0.4:
            return RiskCategory.MEDIUM
        else:
            return RiskCategory.LOW
    
    def detect_fraud_clusters(self) -> List[List[str]]:
        """Detect fraud clusters using community detection"""
        # Use Louvain method for community detection
        partition = community_louvain.best_partition(self.graph)
        
        # Group entities by community
        communities = {}
        for node, comm_id in partition.items():
            if comm_id not in communities:
                communities[comm_id] = []
            communities[comm_id].append(node)
        
        # Filter for suspicious clusters (high fraud concentration)
        fraud_clusters = []
        for comm_id, members in communities.items():
            company_members = [m for m in members if m.startswith('COMP_')]
            if len(company_members) < 3:
                continue
            
            # Check fraud concentration
            fraud_count = sum(1 for m in company_members 
                            if self.companies[self.companies['company_id'] == m]['fraud_label'].iloc[0] == 1)
            
            if fraud_count / len(company_members) > 0.5:
                fraud_clusters.append(company_members)
        
        return fraud_clusters
    
    def calculate_all_risk_scores(self) -> pd.DataFrame:
        """Calculate risk scores for all companies"""
        results = []
        
        for _, company in self.companies.iterrows():
            company_id = company['company_id']
            risk_score, confidence, indicators = self.calculate_company_risk_score(company_id)
            risk_category = self.get_risk_category(risk_score)
            
            results.append({
                'company_id': company_id,
                'risk_score': risk_score,
                'confidence_score': confidence,
                'risk_category': risk_category.value,
                'indicator_count': len(indicators)
            })
        
        return pd.DataFrame(results)
