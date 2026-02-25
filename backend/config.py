import os
from typing import Optional

class Config:
    # Neo4j Configuration (Aura Cloud)
    NEO4J_URI: str = os.getenv("NEO4J_URI", "neo4j+s://ce4768b6.databases.neo4j.io")
    NEO4J_USER: str = os.getenv("NEO4J_USER", "neo4j")
    NEO4J_PASSWORD: str = os.getenv("NEO4J_PASSWORD", "_pZBi1mHZrnXxYexLgi1tcHN-zRbDX97jqVcc3P3TNA")
    NEO4J_DATABASE: str = os.getenv("NEO4J_DATABASE", "neo4j")
    
    # Data paths
    DATA_DIR: str = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "raw")
    
    # Risk scoring thresholds
    RISK_THRESHOLD_HIGH: float = 0.7
    RISK_THRESHOLD_MEDIUM: float = 0.4
    
    # API Configuration
    API_TITLE: str = "NetraAI Investigation API"
    API_VERSION: str = "1.0.0"
    API_DESCRIPTION: str = "AI-powered investigative intelligence system for proactive corruption detection"
    
    # Model paths
    MODEL_DIR: str = os.path.join(os.path.dirname(os.path.dirname(__file__)), "models")
    
config = Config()
