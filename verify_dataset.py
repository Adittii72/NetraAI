import pandas as pd
import os

data_dir = 'data/raw'

companies = pd.read_csv(os.path.join(data_dir, 'companies.csv'))
directors = pd.read_csv(os.path.join(data_dir, 'directors.csv'))
tenders = pd.read_csv(os.path.join(data_dir, 'tenders.csv'))
departments = pd.read_csv(os.path.join(data_dir, 'departments.csv'))
relationships = pd.read_csv(os.path.join(data_dir, 'relationships.csv'))

print('='*70)
print('NETRAAI SYNTHETIC PROCUREMENT DATASET - FINAL SUMMARY')
print('='*70)
print()

print('ENTITY COUNTS:')
print(f'  Companies:      {len(companies)} records')
print(f'  Directors:      {len(directors)} records')
print(f'  Tenders:        {len(tenders)} records')
print(f'  Departments:    {len(departments)} records')
print(f'  Relationships:  {len(relationships)} records')
print()

print('FRAUD DISTRIBUTION:')
print(f'  Fraudulent Companies: {companies["fraud_label"].sum()} ({companies["fraud_label"].sum()/len(companies)*100:.1f}%)')
print(f'  Fraudulent Directors: {directors["fraud_label"].sum()} ({directors["fraud_label"].sum()/len(directors)*100:.1f}%)')
print(f'  Fraudulent Tenders:   {tenders["fraud_label"].sum()} ({tenders["fraud_label"].sum()/len(tenders)*100:.1f}%)')
print()

print('COMPANY ATTRIBUTES:')
print(f'  Industries: {companies["industry_type"].nunique()} unique')
print(f'  Reg. Years: {companies["registration_year"].min()}-{companies["registration_year"].max()}')
print()

print('TENDER ATTRIBUTES:')
print(f'  Year Range:         {tenders["year"].min()}-{tenders["year"].max()}')
print(f'  Contract Value:     \u20B9{tenders["contract_value"].min():,.0f} - \u20B9{tenders["contract_value"].max():,.0f}')
print(f'  Avg Contract Value: \u20B9{tenders["contract_value"].mean():,.0f}')
print()

print('RELATIONSHIP TYPES:')
for rel_type in relationships['relationship_type'].unique():
    count = len(relationships[relationships['relationship_type'] == rel_type])
    print(f'  {rel_type}: {count}')
print()

print('='*70)
print('ALL DATASETS SUCCESSFULLY GENERATED AND READY FOR USE!')
print('='*70)
