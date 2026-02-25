"""
NetraAI Graph Database Loader
Loads synthetic data into Neo4j graph database
"""

import pandas as pd
import os
from typing import Dict, List
from config import config

class GraphDatabaseLoader:
    def __init__(self):
        self.data_dir = config.DATA_DIR
        
    def load_data(self) -> Dict[str, pd.DataFrame]:
        """Load all CSV datasets"""
        print("Loading datasets...")
        
        companies = pd.read_csv(os.path.join(self.data_dir, 'companies.csv'))
        directors = pd.read_csv(os.path.join(self.data_dir, 'directors.csv'))
        tenders = pd.read_csv(os.path.join(self.data_dir, 'tenders.csv'))
        departments = pd.read_csv(os.path.join(self.data_dir, 'departments.csv'))
        relationships = pd.read_csv(os.path.join(self.data_dir, 'relationships.csv'))
        
        return {
            'companies': companies,
            'directors': directors,
            'tenders': tenders,
            'departments': departments,
            'relationships': relationships
        }
    
    def generate_cypher_queries(self, data: Dict[str, pd.DataFrame]) -> List[str]:
        """Generate Cypher queries for Neo4j"""
        queries = []
        
        # Clear existing data
        queries.append("MATCH (n) DETACH DELETE n")
        
        # Create constraints
        queries.append("CREATE CONSTRAINT company_id IF NOT EXISTS FOR (c:Company) REQUIRE c.company_id IS UNIQUE")
        queries.append("CREATE CONSTRAINT director_id IF NOT EXISTS FOR (d:Director) REQUIRE d.director_id IS UNIQUE")
        queries.append("CREATE CONSTRAINT tender_id IF NOT EXISTS FOR (t:Tender) REQUIRE t.tender_id IS UNIQUE")
        queries.append("CREATE CONSTRAINT dept_id IF NOT EXISTS FOR (d:Department) REQUIRE d.department_id IS UNIQUE")
        
        # Create Company nodes
        for _, row in data['companies'].iterrows():
            query = f"""
            CREATE (c:Company {{
                company_id: '{row['company_id']}',
                name: '{row['name'].replace("'", "\\'")}',
                registration_year: {row['registration_year']},
                industry_type: '{row['industry_type']}',
                address: '{row['address'].replace("'", "\\'")}',
                fraud_label: {row['fraud_label']}
            }})
            """
            queries.append(query)
        
        # Create Director nodes
        for _, row in data['directors'].iterrows():
            query = f"""
            CREATE (d:Director {{
                director_id: '{row['director_id']}',
                name: '{row['name'].replace("'", "\\'")}',
                age: {row['age']},
                fraud_label: {row['fraud_label']}
            }})
            """
            queries.append(query)
        
        # Create Tender nodes
        for _, row in data['tenders'].iterrows():
            query = f"""
            CREATE (t:Tender {{
                tender_id: '{row['tender_id']}',
                department_id: '{row['department_id']}',
                contract_value: {row['contract_value']},
                year: {row['year']},
                winning_company_id: '{row['winning_company_id']}',
                fraud_label: {row['fraud_label']}
            }})
            """
            queries.append(query)
        
        # Create Department nodes
        for _, row in data['departments'].iterrows():
            query = f"""
            CREATE (d:Department {{
                department_id: '{row['department_id']}',
                name: '{row['name'].replace("'", "\\'")}',
                location: '{row['location'].replace("'", "\\'")}'
            }})
            """
            queries.append(query)
        
        # Create relationships
        for _, row in data['relationships'].iterrows():
            rel_type = row['relationship_type']
            source = row['source_id']
            target = row['target_id']
            
            # Determine node types
            source_type = self._get_node_type(source)
            target_type = self._get_node_type(target)
            
            query = f"""
            MATCH (s:{source_type} {{{source_type.lower()}_id: '{source}'}})
            MATCH (t:{target_type} {{{target_type.lower()}_id: '{target}'}})
            CREATE (s)-[:{rel_type}]->(t)
            """
            queries.append(query)
        
        return queries
    
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
    
    def save_cypher_script(self, queries: List[str], output_file: str = 'load_graph.cypher'):
        """Save Cypher queries to file"""
        output_path = os.path.join(os.path.dirname(__file__), output_file)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            for query in queries:
                f.write(query.strip() + ';\n\n')
        
        print(f"Cypher script saved to: {output_path}")
        print(f"Total queries: {len(queries)}")

if __name__ == "__main__":
    loader = GraphDatabaseLoader()
    data = loader.load_data()
    queries = loader.generate_cypher_queries(data)
    loader.save_cypher_script(queries)
    print("\nGraph loading script generated successfully!")
