import pandas as pd
import numpy as np
import random
import os
from datetime import datetime, timedelta
from typing import List, Dict, Set, Tuple

RANDOM_SEED = 42
random.seed(RANDOM_SEED)
np.random.seed(RANDOM_SEED)

NUM_COMPANIES = 500
NUM_DIRECTORS = 200
NUM_TENDERS = 150
NUM_DEPARTMENTS = 20
FRAUD_CLUSTER_SIZE = 7 
SHELL_CLUSTER_SIZE = 6 
PROLIFIC_DIRECTOR_THRESHOLD = 6  

OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "data", "raw")

class ProcurementDataGenerator:
    def __init__(self, seed=RANDOM_SEED):
        random.seed(seed)
        np.random.seed(seed)
        self.seed = seed
  
        self.companies = []
        self.directors = []
        self.tenders = []
        self.departments = []
        self.relationships = []
      
        self.fraudulent_companies = set()
        self.fraudulent_directors = set()
        self.fraudulent_tenders = set()
        
    def generate_companies(self) -> pd.DataFrame:
        print("[1/6] Generating companies...")
        
        industries = [
            "Construction", "IT Services", "Healthcare", "Manufacturing",
            "Transportation", "Energy", "Telecommunications", "Engineering",
            "Consulting", "Security Services", "Architecture", "Finance"
        ]
        
        for i in range(NUM_COMPANIES):
            company_id = f"COMP_{i:04d}"
            name = f"{self._generate_company_name()} {random.choice(['Ltd.', 'Inc.', 'corp.', 'LLC'])}"
            registration_year = random.randint(1995, 2023)
            industry = random.choice(industries)
            address = f"{random.randint(1, 999)} {random.choice(['Main', 'Oak', 'Elm', 'Park', 'Central'])} St, {random.choice(['City', 'Town', 'Village'])} {random.randint(10000, 99999)}"
            
            self.companies.append({
                'company_id': company_id,
                'name': name,
                'registration_year': registration_year,
                'industry_type': industry,
                'address': address,
                'fraud_label': 0
            })
        
        return pd.DataFrame(self.companies)
    
    def generate_directors(self) -> pd.DataFrame:
        print("[2/6] Generating directors...")
        
        first_names = [
            "Vishu", "Zeel", "Yash", "Diya", "Golu", "Mahek", "Mahesh", "Freya",
            "Parv", "Mansi", "Priyal", "Venisha", "Pratham", "Heer", "Stuti", "Julie"
        ]
        last_names = [
            "Doshi", "Sharma", "Parekh", "Sangani", "Shah", "Gandhi", "Mandani", "Jasani",
            "Malkan", "Lotia", "Kapoor", "Raghani", "Janani", "Dhruve", "Bhuptani"
        ]
        
        for i in range(NUM_DIRECTORS):
            director_id = f"DIR_{i:04d}"
            name = f"{random.choice(first_names)} {random.choice(last_names)}"
            age = random.randint(30, 75)
            
            self.directors.append({
                'director_id': director_id,
                'name': name,
                'age': age,
                'fraud_label': 0
            })
        
        return pd.DataFrame(self.directors)
    
    def generate_tenders(self) -> pd.DataFrame:
        print("[3/6] Generating tenders...")
        
        for i in range(NUM_TENDERS):
            tender_id = f"TEND_{i:04d}"
            department_id = f"DEPT_{random.randint(0, NUM_DEPARTMENTS-1):02d}"
            contract_value = random.randint(50000, 5000000)
            year = random.randint(2018, 2023)
            winning_company_id = f"COMP_{random.randint(0, NUM_COMPANIES-1):04d}"
            
            self.tenders.append({
                'tender_id': tender_id,
                'department_id': department_id,
                'contract_value': contract_value,
                'year': year,
                'winning_company_id': winning_company_id,
                'fraud_label': 0
            })
        
        return pd.DataFrame(self.tenders)
    
    def generate_departments(self) -> pd.DataFrame:
        print("[4/6] Generating departments...")
        
        dept_names = [
            "Ministry of Transportation", "Department of Health",
            "Ministry of Energy", "Department of Education",
            "Ministry of Defense", "Department of Public Works",
            "Ministry of Commerce", "Department of Agriculture",
            "Ministry of Infrastructure", "Department of Finance",
            "Ministry of Environment", "Department of Justice",
            "Ministry of Interior", "Department of Social Services",
            "Ministry of Communication", "Department of Housing",
            "Ministry of Culture", "Department of Veterans Affairs",
            "Ministry of Labor", "Department of Veterans Services"
        ]
        
        for i in range(NUM_DEPARTMENTS):
            dept_id = f"DEPT_{i:02d}"
            name = dept_names[i % len(dept_names)]
            location = f"Capital City, Region {i % 5 + 1}"
            
            self.departments.append({
                'department_id': dept_id,
                'name': name,
                'location': location
            })
        
        return pd.DataFrame(self.departments)
    
    def create_director_company_relationships(self) -> None:
        print("[5a/6] Creating director-company relationships...")
        
        director_company_count = {}  # Track how many companies each director is linked to
        
        for director_idx in range(NUM_DIRECTORS):
            director_id = f"DIR_{director_idx:04d}"
            num_companies = random.randint(1, 4)
            
            for _ in range(num_companies):
                company_idx = random.randint(0, NUM_COMPANIES - 1)
                company_id = f"COMP_{company_idx:04d}"
                
                self.relationships.append({
                    'source_id': director_id,
                    'target_id': company_id,
                    'relationship_type': 'DIRECTOR_OF'
                })
                
                director_company_count[director_id] = director_company_count.get(director_id, 0) + 1
        
        return director_company_count
    
    def create_company_tender_relationships(self, company_df: pd.DataFrame) -> None:
        print("[5b/6] Creating company-tender relationships...")
        
        for tender_idx, tender_row in company_df.iterrows():
            tender_id = f"TEND_{tender_idx:04d}"
            
            num_bidders = random.randint(3, 7)
            
            bidding_companies = set()
            for _ in range(num_bidders):
                company_idx = random.randint(0, NUM_COMPANIES - 1)
                bidding_companies.add(f"COMP_{company_idx:04d}")
            
            for company_id in bidding_companies:
                self.relationships.append({
                    'source_id': company_id,
                    'target_id': tender_id,
                    'relationship_type': 'BIDDED_FOR'
                })
            
            winning_company_id = f"COMP_{random.randint(0, NUM_COMPANIES-1):04d}"
            self.relationships.append({
                'source_id': winning_company_id,
                'target_id': tender_id,
                'relationship_type': 'WON'
            })
    
    def create_tender_department_relationships(self, tender_df: pd.DataFrame) -> None:
        """Create ISSUED_BY relationships"""
        print("[5c/6] Creating tender-department relationships...")
        
        for _, tender_row in tender_df.iterrows():
            tender_id = tender_row['tender_id']
            dept_id = tender_row['department_id']
            
            self.relationships.append({
                'source_id': tender_id,
                'target_id': dept_id,
                'relationship_type': 'ISSUED_BY'
            })
    
    def inject_fraud_patterns(self, company_df: pd.DataFrame, 
                             director_df: pd.DataFrame,
                             tender_df: pd.DataFrame) -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
        print("[6/6] Injecting fraud patterns...")
        
        company_df_copy = company_df.copy()
        director_df_copy = director_df.copy()
        tender_df_copy = tender_df.copy()
        
        self._inject_shared_directors(company_df_copy, director_df_copy)
        self._inject_collusive_cluster(company_df_copy, tender_df_copy)
        self._inject_shell_companies(company_df_copy)
        self._inject_prolific_directors(company_df_copy, director_df_copy)
        self._inject_high_contract_winners(company_df_copy, tender_df_copy)
        self._inject_circular_ownership(company_df_copy, director_df_copy)
        
        return company_df_copy, director_df_copy, tender_df_copy
    
    def _inject_shared_directors(self, company_df: pd.DataFrame, director_df: pd.DataFrame) -> None:
        print("  Injecting Pattern 1: Shared Directors...")
        
        for group in range(5):
            shared_director_idx = random.randint(0, NUM_DIRECTORS - 1)
            shared_director_id = f"DIR_{shared_director_idx:04d}"
            
            group_companies = random.sample(range(NUM_COMPANIES), k=random.randint(3, 4))
            
            for company_idx in group_companies:
                company_id = f"COMP_{company_idx:04d}"
                self.relationships.append({
                    'source_id': shared_director_id,
                    'target_id': company_id,
                    'relationship_type': 'DIRECTOR_OF'
                })
                
                self.fraudulent_companies.add(company_id)
                self.fraudulent_directors.add(shared_director_id)
    
    def _inject_collusive_cluster(self, company_df: pd.DataFrame, tender_df: pd.DataFrame) -> None:
        print("  Injecting Pattern 2: Collusive Cluster...")
        
        num_clusters = random.randint(3, 4)
        
        for cluster in range(num_clusters):
            cluster_companies = random.sample(range(NUM_COMPANIES), k=FRAUD_CLUSTER_SIZE)
            cluster_company_ids = [f"COMP_{idx:04d}" for idx in cluster_companies]
            
            high_value_tenders = tender_df.nlargest(int(NUM_TENDERS * 0.15), 'contract_value')
            
            for _, tender_row in high_value_tenders.iterrows():
                tender_id = tender_row['tender_id']
                
                for company_id in cluster_company_ids:
                    self.relationships.append({
                        'source_id': company_id,
                        'target_id': tender_id,
                        'relationship_type': 'BIDDED_FOR'
                    })
                
                winner = random.choice(cluster_company_ids)
                self.relationships.append({
                    'source_id': winner,
                    'target_id': tender_id,
                    'relationship_type': 'WON'
                })
                
                self.fraudulent_tenders.add(tender_id)
            
            self.fraudulent_companies.update(cluster_company_ids)
    
    def _inject_shell_companies(self, company_df: pd.DataFrame) -> None:
        print("  Injecting Pattern 3: Shell Companies...")
        
        num_shell_groups = random.randint(3, 4)
        
        for group in range(num_shell_groups):
            shell_year = random.randint(2018, 2023)
            shell_addresses = [f"{random.randint(1, 10)} Dummy Street, Shell City 00000"]
            
            shell_indices = random.sample(range(NUM_COMPANIES), k=SHELL_CLUSTER_SIZE)
            
            for idx in shell_indices:
                company_df.at[idx, 'registration_year'] = shell_year
                company_df.at[idx, 'address'] = shell_addresses[0]
                company_df.at[idx, 'fraud_label'] = 1
                
                company_id = f"COMP_{idx:04d}"
                self.fraudulent_companies.add(company_id)
    
    def _inject_prolific_directors(self, company_df: pd.DataFrame, director_df: pd.DataFrame) -> None:
        print("  Injecting Pattern 4: Prolific Directors...")
        
        prolific_count = random.randint(5, 8)
        prolific_directors = random.sample(range(NUM_DIRECTORS), k=prolific_count)
        
        for director_idx in prolific_directors:
            director_id = f"DIR_{director_idx:04d}"
            num_linked = random.randint(15, 25)
            linked_companies = random.sample(range(NUM_COMPANIES), k=num_linked)
            
            for company_idx in linked_companies:
                company_id = f"COMP_{company_idx:04d}"
                
                self.relationships.append({
                    'source_id': director_id,
                    'target_id': company_id,
                    'relationship_type': 'DIRECTOR_OF'
                })
                
                self.fraudulent_directors.add(director_id)
                self.fraudulent_companies.add(company_id)
    
    def _inject_high_contract_winners(self, company_df: pd.DataFrame, tender_df: pd.DataFrame) -> None:
        print("  Injecting Pattern 5: High Contract Winners...")
        high_value_companies = random.sample(range(NUM_COMPANIES), k=random.randint(5, 7))
        
        for company_idx in high_value_companies:
            company_id = f"COMP_{company_idx:04d}"
            high_tenders = tender_df[tender_df['contract_value'] > tender_df['contract_value'].quantile(0.75)]
            num_wins = min(random.randint(5, 10), len(high_tenders))
            winning_tenders = random.sample(list(high_tenders['tender_id']), k=num_wins)
            
            for tender_id in winning_tenders:
                self.relationships.append({
                    'source_id': company_id,
                    'target_id': tender_id,
                    'relationship_type': 'WON'
                })
                
                self.fraudulent_companies.add(company_id)
                self.fraudulent_tenders.add(tender_id)
    
    def _inject_circular_ownership(self, company_df: pd.DataFrame, director_df: pd.DataFrame) -> None:
        print("  Injecting Pattern 6: Circular Ownership...")
        num_circles = random.randint(2, 3)
        
        for circle in range(num_circles):
            circle_size = random.randint(3, 5)
            
            circle_companies = random.sample(range(NUM_COMPANIES), k=circle_size)
            circle_directors = random.sample(range(NUM_DIRECTORS), k=circle_size)
            for i in range(circle_size):
                company_id = f"COMP_{circle_companies[i]:04d}"
                director_id = f"DIR_{circle_directors[(i + 1) % circle_size]:04d}"
                
                self.relationships.append({
                    'source_id': director_id,
                    'target_id': company_id,
                    'relationship_type': 'DIRECTOR_OF'
                })
                
                self.fraudulent_companies.add(company_id)
                self.fraudulent_directors.add(director_id)
    
    def mark_fraudulent_entities(self, company_df: pd.DataFrame, 
                                director_df: pd.DataFrame,
                                tender_df: pd.DataFrame) -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
        """Mark fraudulent entities with fraud_label = 1"""
        company_df_copy = company_df.copy()
        director_df_copy = director_df.copy()
        tender_df_copy = tender_df.copy()
        for company_id in self.fraudulent_companies:
            idx = int(company_id.split('_')[1])
            company_df_copy.at[idx, 'fraud_label'] = 1
    
        for director_id in self.fraudulent_directors:
            idx = int(director_id.split('_')[1])
            director_df_copy.at[idx, 'fraud_label'] = 1
        
        for tender_id in self.fraudulent_tenders:
            idx = int(tender_id.split('_')[1])
            tender_df_copy.at[idx, 'fraud_label'] = 1
        
        return company_df_copy, director_df_copy, tender_df_copy
    
    def generate(self) -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame]:
        """Generate complete synthetic dataset"""
        print("\n" + "="*60)
        print("STARTING SYNTHETIC PROCUREMENT DATASET GENERATION")
        print("="*60 + "\n")
        
        company_df = self.generate_companies()
        director_df = self.generate_directors()
        tender_df = self.generate_tenders()
        department_df = self.generate_departments()
        
        self.create_director_company_relationships()
        self.create_company_tender_relationships(tender_df)
        self.create_tender_department_relationships(tender_df)
        
        company_df, director_df, tender_df = self.inject_fraud_patterns(
            company_df, director_df, tender_df
        )
        
        company_df, director_df, tender_df = self.mark_fraudulent_entities(
            company_df, director_df, tender_df
        )
        
        print("\n" + "="*60)
        print("DATASET GENERATION COMPLETE")
        print("="*60 + "\n")
        
        print("Summary Statistics:")
        print(f"  Companies: {len(company_df)} (Fraudulent: {company_df['fraud_label'].sum()})")
        print(f"  Directors: {len(director_df)} (Fraudulent: {director_df['fraud_label'].sum()})")
        print(f"  Tenders: {len(tender_df)} (Fraudulent: {tender_df['fraud_label'].sum()})")
        print(f"  Departments: {len(department_df)}")
        print(f"  Relationships: {len(self.relationships)}")
        print()
        
        return company_df, director_df, tender_df, department_df, pd.DataFrame(self.relationships)
    
    def save(self, company_df: pd.DataFrame, director_df: pd.DataFrame,
             tender_df: pd.DataFrame, department_df: pd.DataFrame,
             relationship_df: pd.DataFrame) -> None:
        print("Saving datasets to CSV files...")
        
        os.makedirs(OUTPUT_DIR, exist_ok=True)
        
        company_df.to_csv(os.path.join(OUTPUT_DIR, 'companies.csv'), index=False)
        director_df.to_csv(os.path.join(OUTPUT_DIR, 'directors.csv'), index=False)
        tender_df.to_csv(os.path.join(OUTPUT_DIR, 'tenders.csv'), index=False)
        department_df.to_csv(os.path.join(OUTPUT_DIR, 'departments.csv'), index=False)
        relationship_df.to_csv(os.path.join(OUTPUT_DIR, 'relationships.csv'), index=False)
        
        print(f"✓ Datasets saved to: {OUTPUT_DIR}\n")
        print("Files created:")
        print(f"  - companies.csv ({len(company_df)} rows)")
        print(f"  - directors.csv ({len(director_df)} rows)")
        print(f"  - tenders.csv ({len(tender_df)} rows)")
        print(f"  - departments.csv ({len(department_df)} rows)")
        print(f"  - relationships.csv ({len(relationship_df)} rows)")
    
    @staticmethod
    def _generate_company_name() -> str:
        prefixes = ["Tech", "Global", "Smart", "Prime", "Elite", "Forward", 
                   "Dynamic", "Apex", "Nexus", "Quantum", "Venture", "Summit"]
        middles = ["Solutions", "Systems", "Services", "Group", "Holdings", 
                  "Enterprises", "Industries", "Ventures", "Labs"]
        
        return f"{random.choice(prefixes)} {random.choice(middles)}"


if __name__ == "__main__":
    generator = ProcurementDataGenerator(seed=RANDOM_SEED)
    
    company_df, director_df, tender_df, department_df, relationship_df = generator.generate()
    
    generator.save(company_df, director_df, tender_df, department_df, relationship_df)
    
    print("\n" + "="*60)
    print("Dataset generation completed successfully!")
    print("="*60)
