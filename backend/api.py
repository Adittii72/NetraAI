"""
NetraAI Investigation API
FastAPI backend for government-grade investigative platform
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Dict, Any
import pandas as pd
import os

from config import config
from models import (
    DashboardStats, CompanyProfile, DirectorProfile, TenderProfile,
    NetworkGraph, NetworkNode, NetworkEdge, EntityDetail, InvestigationSummary,
    RiskCategory, EntityType, RiskIndicator
)
from risk_engine import RiskScoringEngine

# Initialize FastAPI
app = FastAPI(
    title=config.API_TITLE,
    version=config.API_VERSION,
    description=config.API_DESCRIPTION
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load data
data_cache = {}
risk_engine = None

def load_data():
    """Load all datasets"""
    global data_cache, risk_engine
    
    print("  Loading CSV files...")
    data_cache['companies'] = pd.read_csv(os.path.join(config.DATA_DIR, 'companies.csv'))
    data_cache['directors'] = pd.read_csv(os.path.join(config.DATA_DIR, 'directors.csv'))
    data_cache['tenders'] = pd.read_csv(os.path.join(config.DATA_DIR, 'tenders.csv'))
    data_cache['departments'] = pd.read_csv(os.path.join(config.DATA_DIR, 'departments.csv'))
    data_cache['relationships'] = pd.read_csv(os.path.join(config.DATA_DIR, 'relationships.csv'))
    
    print("  Initializing risk engine...")
    risk_engine = RiskScoringEngine(data_cache)
    
    # Calculate risk scores (this may take a moment)
    print("  Calculating risk scores for all entities...")
    risk_scores = risk_engine.calculate_all_risk_scores()
    data_cache['risk_scores'] = risk_scores
    print(f"  Risk scores calculated for {len(risk_scores)} companies")

@app.on_event("startup")
async def startup_event():
    """Load data on startup"""
    print("Loading NetraAI data...")
    load_data()
    print("✓ NetraAI API initialized successfully")

@app.get("/")
async def root():
    """API root endpoint"""
    return {
        "message": "NetraAI Investigation API",
        "version": config.API_VERSION,
        "status": "operational"
    }

@app.get("/api/dashboard/stats", response_model=DashboardStats)
async def get_dashboard_stats():
    """Get dashboard overview statistics"""
    companies = data_cache['companies']
    tenders = data_cache['tenders']
    risk_scores = data_cache['risk_scores']
    
    # Detect fraud clusters
    fraud_clusters = risk_engine.detect_fraud_clusters()
    
    # Risk distribution
    risk_dist = risk_scores['risk_category'].value_counts().to_dict()
    
    return DashboardStats(
        total_entities=len(companies) + len(data_cache['directors']),
        high_risk_count=len(risk_scores[risk_scores['risk_category'] == 'High']),
        fraud_cluster_count=len(fraud_clusters),
        total_tenders=len(tenders),
        total_contract_value=float(tenders['contract_value'].sum()),
        risk_distribution=risk_dist
    )

@app.get("/api/companies", response_model=List[CompanyProfile])
async def get_companies(risk_category: str = None, limit: int = 100):
    """Get list of companies with risk scores"""
    companies = data_cache['companies']
    risk_scores = data_cache['risk_scores']
    
    # Merge data
    merged = companies.merge(risk_scores, on='company_id')
    
    # Filter by risk category
    if risk_category:
        merged = merged[merged['risk_category'] == risk_category]
    
    # Limit results
    merged = merged.head(limit)
    
    results = []
    for _, row in merged.iterrows():
        results.append(CompanyProfile(
            company_id=row['company_id'],
            name=row['name'],
            registration_year=int(row['registration_year']),
            industry_type=row['industry_type'],
            address=row['address'],
            risk_score=float(row['risk_score']),
            risk_category=RiskCategory(row['risk_category']),
            confidence_score=float(row['confidence_score']),
            fraud_label=int(row['fraud_label'])
        ))
    
    return results

@app.get("/api/company/{company_id}", response_model=EntityDetail)
async def get_company_detail(company_id: str):
    """Get detailed company profile"""
    companies = data_cache['companies']
    relationships = data_cache['relationships']
    
    company = companies[companies['company_id'] == company_id]
    if company.empty:
        raise HTTPException(status_code=404, detail="Company not found")
    
    company = company.iloc[0]
    
    # Calculate risk score
    risk_score, confidence, indicators = risk_engine.calculate_company_risk_score(company_id)
    risk_category = risk_engine.get_risk_category(risk_score)
    
    # Get connected entities
    connected = relationships[
        (relationships['source_id'] == company_id) | 
        (relationships['target_id'] == company_id)
    ]
    
    connected_entities = []
    for _, rel in connected.head(20).iterrows():
        entity_id = rel['target_id'] if rel['source_id'] == company_id else rel['source_id']
        connected_entities.append({
            'entity_id': entity_id,
            'relationship_type': rel['relationship_type']
        })
    
    # Get tender history
    won_tenders = relationships[
        (relationships['source_id'] == company_id) &
        (relationships['relationship_type'] == 'WON')
    ]
    
    tender_history = []
    for _, rel in won_tenders.iterrows():
        tender = data_cache['tenders'][data_cache['tenders']['tender_id'] == rel['target_id']]
        if not tender.empty:
            tender = tender.iloc[0]
            tender_history.append({
                'tender_id': tender['tender_id'],
                'contract_value': float(tender['contract_value']),
                'year': int(tender['year'])
            })
    
    return EntityDetail(
        entity_id=company_id,
        entity_type=EntityType.COMPANY,
        risk_score=risk_score,
        risk_category=risk_category,
        risk_indicators=indicators,
        connected_entities=connected_entities,
        tender_history=tender_history
    )

@app.get("/api/network/graph", response_model=NetworkGraph)
async def get_network_graph(entity_id: str = None, depth: int = 2):
    """Get network graph for visualization"""
    relationships = data_cache['relationships']
    risk_scores = data_cache['risk_scores']
    companies = data_cache['companies']
    
    if entity_id:
        # Get subgraph around entity - only include companies
        nodes_to_include = {entity_id}
        edges = []
        
        for _ in range(depth):
            new_nodes = set()
            for node in nodes_to_include:
                connected = relationships[
                    (relationships['source_id'] == node) | 
                    (relationships['target_id'] == node)
                ]
                for _, rel in connected.iterrows():
                    # Only include company nodes
                    if rel['source_id'].startswith('COMP_'):
                        new_nodes.add(rel['source_id'])
                    if rel['target_id'].startswith('COMP_'):
                        new_nodes.add(rel['target_id'])
                    edges.append(rel)
            nodes_to_include.update(new_nodes)
            
            if len(nodes_to_include) > 50:  # Limit graph size
                break
        
        # Filter to only company nodes
        nodes_to_include = {n for n in nodes_to_include if n.startswith('COMP_')}
    else:
        # Get high-risk entities (companies only)
        high_risk = risk_scores[risk_scores['risk_category'] == 'High'].head(20)
        nodes_to_include = set(high_risk['company_id'].tolist())
        
        edges = relationships[
            (relationships['source_id'].isin(nodes_to_include) & relationships['target_id'].isin(nodes_to_include))
        ].to_dict('records')
    
    # Build nodes - only companies
    nodes = []
    for node_id in nodes_to_include:
        if not node_id.startswith('COMP_'):
            continue
            
        node_type = EntityType.COMPANY
        risk_score = 0.0
        risk_category = RiskCategory.LOW
        
        risk_data = risk_scores[risk_scores['company_id'] == node_id]
        if not risk_data.empty:
            risk_score = float(risk_data.iloc[0]['risk_score'])
            risk_category = RiskCategory(risk_data.iloc[0]['risk_category'])
        
        nodes.append(NetworkNode(
            id=node_id,
            label=_get_entity_label(node_id, data_cache),
            type=node_type,
            risk_score=risk_score,
            risk_category=risk_category
        ))
    
    # Build edges - only between companies
    network_edges = []
    for edge in edges:
        if isinstance(edge, pd.Series):
            edge = edge.to_dict()
        
        # Only include edges between companies
        if edge['source_id'].startswith('COMP_') and edge['target_id'].startswith('COMP_'):
            if edge['source_id'] in nodes_to_include and edge['target_id'] in nodes_to_include:
                network_edges.append(NetworkEdge(
                    source=edge['source_id'],
                    target=edge['target_id'],
                    relationship_type=edge['relationship_type']
                ))
    
    return NetworkGraph(nodes=nodes, edges=network_edges)

@app.get("/api/investigation/summary/{entity_id}", response_model=InvestigationSummary)
async def generate_investigation_summary(entity_id: str):
    """Generate investigation summary for an entity"""
    if not entity_id.startswith('COMP_'):
        raise HTTPException(status_code=400, detail="Only company investigations supported")
    
    companies = data_cache['companies']
    company = companies[companies['company_id'] == entity_id]
    
    if company.empty:
        raise HTTPException(status_code=404, detail="Company not found")
    
    # Calculate risk
    risk_score, confidence, indicators = risk_engine.calculate_company_risk_score(entity_id)
    risk_category = risk_engine.get_risk_category(risk_score)
    
    # Generate key findings
    key_findings = []
    for indicator in indicators:
        key_findings.append(f"{indicator.indicator}: {indicator.description}")
    
    # Find connected suspicious entities
    relationships = data_cache['relationships']
    connected = relationships[
        (relationships['source_id'] == entity_id) | 
        (relationships['target_id'] == entity_id)
    ]
    
    suspicious_entities = []
    for _, rel in connected.iterrows():
        other_id = rel['target_id'] if rel['source_id'] == entity_id else rel['source_id']
        if other_id.startswith('COMP_'):
            other_risk = risk_scores[risk_scores['company_id'] == other_id]
            if not other_risk.empty and other_risk.iloc[0]['risk_category'] == 'High':
                suspicious_entities.append(other_id)
    
    # Generate recommendation
    if risk_category == RiskCategory.HIGH:
        recommendation = "IMMEDIATE INVESTIGATION RECOMMENDED: High-risk indicators detected. Recommend full audit and cross-reference with procurement records."
    elif risk_category == RiskCategory.MEDIUM:
        recommendation = "MONITORING REQUIRED: Medium-risk indicators present. Recommend enhanced due diligence and periodic review."
    else:
        recommendation = "STANDARD MONITORING: Low-risk profile. Continue routine oversight."
    
    return InvestigationSummary(
        entity_id=entity_id,
        entity_type=EntityType.COMPANY,
        risk_score=risk_score,
        risk_category=risk_category,
        key_findings=key_findings,
        risk_indicators=indicators,
        connected_suspicious_entities=suspicious_entities[:10],
        recommendation=recommendation
    )

@app.get("/api/clusters")
async def get_fraud_clusters():
    """Get detected fraud clusters"""
    clusters = risk_engine.detect_fraud_clusters()
    
    result = []
    for i, cluster in enumerate(clusters):
        cluster_info = {
            'cluster_id': i,
            'size': len(cluster),
            'members': cluster[:10]  # Limit to 10 for display
        }
        result.append(cluster_info)
    
    return {"clusters": result, "total_clusters": len(clusters)}

def _get_entity_type(entity_id: str) -> EntityType:
    """Get entity type from ID"""
    if entity_id.startswith('COMP_'):
        return EntityType.COMPANY
    elif entity_id.startswith('DIR_'):
        return EntityType.DIRECTOR
    elif entity_id.startswith('TEND_'):
        return EntityType.TENDER
    elif entity_id.startswith('DEPT_'):
        return EntityType.DEPARTMENT
    return EntityType.COMPANY

def _get_entity_label(entity_id: str, data: Dict) -> str:
    """Get entity label for display"""
    if entity_id.startswith('COMP_'):
        company = data['companies'][data['companies']['company_id'] == entity_id]
        return company.iloc[0]['name'] if not company.empty else entity_id
    elif entity_id.startswith('DIR_'):
        director = data['directors'][data['directors']['director_id'] == entity_id]
        return director.iloc[0]['name'] if not director.empty else entity_id
    return entity_id

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
