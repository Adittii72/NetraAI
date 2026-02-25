"""
NetraAI Data Models
Pydantic models for API requests/responses
"""

from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from enum import Enum

class RiskCategory(str, Enum):
    LOW = "Low"
    MEDIUM = "Medium"
    HIGH = "High"

class EntityType(str, Enum):
    COMPANY = "Company"
    DIRECTOR = "Director"
    TENDER = "Tender"
    DEPARTMENT = "Department"

class RiskIndicator(BaseModel):
    indicator: str
    severity: str
    description: str

class CompanyProfile(BaseModel):
    company_id: str
    name: str
    registration_year: int
    industry_type: str
    address: str
    risk_score: float
    risk_category: RiskCategory
    confidence_score: float
    fraud_label: int
    
class DirectorProfile(BaseModel):
    director_id: str
    name: str
    age: int
    risk_score: float
    risk_category: RiskCategory
    fraud_label: int
    company_count: int

class TenderProfile(BaseModel):
    tender_id: str
    department_id: str
    contract_value: float
    year: int
    winning_company_id: str
    risk_score: float
    risk_category: RiskCategory
    fraud_label: int

class NetworkNode(BaseModel):
    id: str
    label: str
    type: EntityType
    risk_score: float
    risk_category: RiskCategory

class NetworkEdge(BaseModel):
    source: str
    target: str
    relationship_type: str

class NetworkGraph(BaseModel):
    nodes: List[NetworkNode]
    edges: List[NetworkEdge]

class EntityDetail(BaseModel):
    entity_id: str
    entity_type: EntityType
    risk_score: float
    risk_category: RiskCategory
    risk_indicators: List[RiskIndicator]
    connected_entities: List[Dict[str, Any]]
    tender_history: Optional[List[Dict[str, Any]]] = None

class DashboardStats(BaseModel):
    total_entities: int
    high_risk_count: int
    fraud_cluster_count: int
    total_tenders: int
    total_contract_value: float
    risk_distribution: Dict[str, int]

class InvestigationSummary(BaseModel):
    entity_id: str
    entity_type: EntityType
    risk_score: float
    risk_category: RiskCategory
    key_findings: List[str]
    risk_indicators: List[RiskIndicator]
    connected_suspicious_entities: List[str]
    recommendation: str
