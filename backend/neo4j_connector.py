"""
NetraAI Neo4j Database Connector
Real-time connection to Neo4j graph database
"""

from neo4j import GraphDatabase
import pandas as pd
import os
from typing import Dict, List, Optional
from config import config

class Neo4jConnector:
    """Neo4j database connector for NetraAI"""
    
    def __init__(self, uri: str = None, user: str = None, password: str = None):
        """Initialize Neo4j connection"""
        self.uri = uri or config.NEO4J_URI
        self.user = user or config.NEO4J_USER
        self.password = password or config.NEO4J_PASSWORD
        self.driver = None
        
    def connect(self):
        """Establish connection to Neo4j"""
        try:
            self.driver = GraphDatabase.driver(self.uri, auth=(self.user, self.password))
            # Test connection
            with self.driver.session() as session:
                result = session.run("RETURN 1 as test")
                result.single()
            print(f"✓ Connected to Neo4j at {self.uri}")
            return True
        except Exception as e:
            print(f"✗ Failed to connect to Neo4j: {e}")
            print(f"  URI: {self.uri}")
            print(f"  Make sure Neo4j is running and credentials are correct")
            return False
    
    def close(self):
        """Close Neo4j connection"""
        if self.driver:
            self.driver.close()
            print("✓ Neo4j connection closed")
    
    def clear_database(self):
        """Clear all nodes and relationships"""
        with self.driver.session() as session:
            session.run("MATCH (n) DETACH DELETE n")
            print("✓ Database cleared")
    
    def create_constraints(self):
        """Create uniqueness constraints"""
        constraints = [
            "CREATE CONSTRAINT company_id IF NOT EXISTS FOR (c:Company) REQUIRE c.company_id IS UNIQUE",
            "CREATE CONSTRAINT director_id IF NOT EXISTS FOR (d:Director) REQUIRE d.director_id IS UNIQUE",
            "CREATE CONSTRAINT tender_id IF NOT EXISTS FOR (t:Tender) REQUIRE t.tender_id IS UNIQUE",
            "CREATE CONSTRAINT dept_id IF NOT EXISTS FOR (d:Department) REQUIRE d.department_id IS UNIQUE"
        ]
        
        with self.driver.session() as session:
            for constraint in constraints:
                try:
                    session.run(constraint)
                except Exception as e:
                    # Constraint might already exist
                    pass
        print("✓ Constraints created")
    
    def load_companies(self, companies_df: pd.DataFrame):
        """Load company nodes into Neo4j"""
        with self.driver.session() as session:
            for _, row in companies_df.iterrows():
                query = """
                CREATE (c:Company {
                    company_id: $company_id,
                    name: $name,
                    registration_year: $registration_year,
                    industry_type: $industry_type,
                    address: $address,
                    fraud_label: $fraud_label
                })
                """
                session.run(query, 
                    company_id=row['company_id'],
                    name=row['name'],
                    registration_year=int(row['registration_year']),
                    industry_type=row['industry_type'],
                    address=row['address'],
                    fraud_label=int(row['fraud_label'])
                )
        print(f"✓ Loaded {len(companies_df)} companies")
    
    def load_directors(self, directors_df: pd.DataFrame):
        """Load director nodes into Neo4j"""
        with self.driver.session() as session:
            for _, row in directors_df.iterrows():
                query = """
                CREATE (d:Director {
                    director_id: $director_id,
                    name: $name,
                    age: $age,
                    fraud_label: $fraud_label
                })
                """
                session.run(query,
                    director_id=row['director_id'],
                    name=row['name'],
                    age=int(row['age']),
                    fraud_label=int(row['fraud_label'])
                )
        print(f"✓ Loaded {len(directors_df)} directors")
    
    def load_tenders(self, tenders_df: pd.DataFrame):
        """Load tender nodes into Neo4j"""
        with self.driver.session() as session:
            for _, row in tenders_df.iterrows():
                query = """
                CREATE (t:Tender {
                    tender_id: $tender_id,
                    department_id: $department_id,
                    contract_value: $contract_value,
                    year: $year,
                    winning_company_id: $winning_company_id,
                    fraud_label: $fraud_label
                })
                """
                session.run(query,
                    tender_id=row['tender_id'],
                    department_id=row['department_id'],
                    contract_value=float(row['contract_value']),
                    year=int(row['year']),
                    winning_company_id=row['winning_company_id'],
                    fraud_label=int(row['fraud_label'])
                )
        print(f"✓ Loaded {len(tenders_df)} tenders")
    
    def load_departments(self, departments_df: pd.DataFrame):
        """Load department nodes into Neo4j"""
        with self.driver.session() as session:
            for _, row in departments_df.iterrows():
                query = """
                CREATE (d:Department {
                    department_id: $department_id,
                    name: $name,
                    location: $location
                })
                """
                session.run(query,
                    department_id=row['department_id'],
                    name=row['name'],
                    location=row['location']
                )
        print(f"✓ Loaded {len(departments_df)} departments")
    
    def load_relationships(self, relationships_df: pd.DataFrame):
        """Load relationships into Neo4j"""
        with self.driver.session() as session:
            for _, row in relationships_df.iterrows():
                rel_type = row['relationship_type']
                source = row['source_id']
                target = row['target_id']
                
                # Determine node types
                source_type = self._get_node_type(source)
                target_type = self._get_node_type(target)
                
                query = f"""
                MATCH (s:{source_type} {{{source_type.lower()}_id: $source}})
                MATCH (t:{target_type} {{{target_type.lower()}_id: $target}})
                CREATE (s)-[:{rel_type}]->(t)
                """
                session.run(query, source=source, target=target)
        print(f"✓ Loaded {len(relationships_df)} relationships")
    
    def _get_node_type(self, entity_id: str) -> str:
        """Determine node type from entity ID"""
        if entity_id.startswith('COMP_'):
            return 'Company'
        elif entity_id.startswith('DIR_'):
            return 'Director'
        elif entity_id.startswith('TEND_'):
            return 'Tender'
        elif entity_id.startswith('DEPT_'):
            return 'Department'
        return 'Unknown'
    
    def get_company(self, company_id: str) -> Optional[Dict]:
        """Get company by ID"""
        with self.driver.session() as session:
            result = session.run("""
                MATCH (c:Company {company_id: $company_id})
                RETURN c
            """, company_id=company_id)
            record = result.single()
            return dict(record['c']) if record else None
    
    def get_company_relationships(self, company_id: str) -> List[Dict]:
        """Get all relationships for a company"""
        with self.driver.session() as session:
            result = session.run("""
                MATCH (c:Company {company_id: $company_id})-[r]-(other)
                RETURN type(r) as relationship_type, 
                       labels(other)[0] as other_type,
                       properties(other) as other_properties
                LIMIT 50
            """, company_id=company_id)
            return [dict(record) for record in result]
    
    def get_high_risk_companies(self, limit: int = 20) -> List[Dict]:
        """Get companies with fraud_label = 1"""
        with self.driver.session() as session:
            result = session.run("""
                MATCH (c:Company {fraud_label: 1})
                RETURN c
                LIMIT $limit
            """, limit=limit)
            return [dict(record['c']) for record in result]
    
    def get_network_subgraph(self, entity_id: str, depth: int = 2) -> Dict:
        """Get network subgraph around an entity"""
        with self.driver.session() as session:
            # Get nodes and relationships within depth
            result = session.run("""
                MATCH path = (start {company_id: $entity_id})-[*1..$depth]-(connected)
                WHERE ALL(node IN nodes(path) WHERE 'Company' IN labels(node))
                WITH nodes(path) as nodes, relationships(path) as rels
                UNWIND nodes as n
                WITH collect(DISTINCT n) as unique_nodes, rels
                UNWIND rels as r
                RETURN unique_nodes, collect(DISTINCT r) as unique_rels
                LIMIT 1
            """, entity_id=entity_id, depth=depth)
            
            record = result.single()
            if not record:
                return {'nodes': [], 'edges': []}
            
            nodes = [dict(node) for node in record['unique_nodes']]
            edges = []
            for rel in record['unique_rels']:
                edges.append({
                    'source': rel.start_node['company_id'],
                    'target': rel.end_node['company_id'],
                    'type': rel.type
                })
            
            return {'nodes': nodes, 'edges': edges}
    
    def detect_fraud_clusters(self) -> List[List[str]]:
        """Detect fraud clusters using graph algorithms"""
        with self.driver.session() as session:
            # Find connected components of fraudulent companies
            result = session.run("""
                MATCH (c:Company {fraud_label: 1})
                MATCH path = (c)-[*1..3]-(other:Company {fraud_label: 1})
                WITH c, collect(DISTINCT other.company_id) as cluster
                WHERE size(cluster) >= 3
                RETURN c.company_id as seed, cluster
                LIMIT 10
            """)
            
            clusters = []
            seen = set()
            for record in result:
                cluster = [record['seed']] + record['cluster']
                cluster_key = tuple(sorted(cluster))
                if cluster_key not in seen:
                    seen.add(cluster_key)
                    clusters.append(cluster)
            
            return clusters
    
    def get_statistics(self) -> Dict:
        """Get database statistics"""
        with self.driver.session() as session:
            result = session.run("""
                MATCH (c:Company)
                WITH count(c) as total_companies, 
                     sum(CASE WHEN c.fraud_label = 1 THEN 1 ELSE 0 END) as fraud_companies
                MATCH (d:Director)
                WITH total_companies, fraud_companies, count(d) as total_directors
                MATCH (t:Tender)
                WITH total_companies, fraud_companies, total_directors, 
                     count(t) as total_tenders,
                     sum(t.contract_value) as total_value
                MATCH ()-[r]->()
                RETURN total_companies, fraud_companies, total_directors, 
                       total_tenders, total_value, count(r) as total_relationships
            """)
            
            record = result.single()
            return dict(record) if record else {}


def load_data_to_neo4j():
    """Main function to load all data into Neo4j"""
    print("\n" + "="*60)
    print("LOADING DATA INTO NEO4J")
    print("="*60 + "\n")
    
    # Initialize connector
    connector = Neo4jConnector()
    
    # Connect to Neo4j
    if not connector.connect():
        print("\n⚠️  Neo4j is not running or not configured.")
        print("\nTo use Neo4j:")
        print("1. Install Neo4j Desktop or Docker")
        print("2. Start Neo4j instance")
        print("3. Update credentials in backend/config.py")
        print("4. Run this script again")
        return False
    
    try:
        # Load CSV data
        print("\nLoading CSV files...")
        data_dir = config.DATA_DIR
        companies = pd.read_csv(os.path.join(data_dir, 'companies.csv'))
        directors = pd.read_csv(os.path.join(data_dir, 'directors.csv'))
        tenders = pd.read_csv(os.path.join(data_dir, 'tenders.csv'))
        departments = pd.read_csv(os.path.join(data_dir, 'departments.csv'))
        relationships = pd.read_csv(os.path.join(data_dir, 'relationships.csv'))
        
        # Clear existing data
        print("\nClearing existing data...")
        connector.clear_database()
        
        # Create constraints
        print("\nCreating constraints...")
        connector.create_constraints()
        
        # Load nodes
        print("\nLoading nodes...")
        connector.load_companies(companies)
        connector.load_directors(directors)
        connector.load_tenders(tenders)
        connector.load_departments(departments)
        
        # Load relationships
        print("\nLoading relationships...")
        connector.load_relationships(relationships)
        
        # Get statistics
        print("\n" + "="*60)
        print("LOADING COMPLETE")
        print("="*60)
        stats = connector.get_statistics()
        print(f"\nDatabase Statistics:")
        print(f"  Companies: {stats.get('total_companies', 0)} ({stats.get('fraud_companies', 0)} fraudulent)")
        print(f"  Directors: {stats.get('total_directors', 0)}")
        print(f"  Tenders: {stats.get('total_tenders', 0)}")
        print(f"  Relationships: {stats.get('total_relationships', 0)}")
        print(f"  Total Contract Value: ₹{stats.get('total_value', 0):,.0f}")
        
        print("\n✓ Data successfully loaded into Neo4j!")
        print(f"\nAccess Neo4j Browser at: http://localhost:7474")
        
        return True
        
    except Exception as e:
        print(f"\n✗ Error loading data: {e}")
        import traceback
        traceback.print_exc()
        return False
    finally:
        connector.close()


if __name__ == "__main__":
    load_data_to_neo4j()
