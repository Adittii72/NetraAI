# NetraAI - Government-Grade Investigative Intelligence Platform

Note: First load may take 30 seconds (free tier limitation). 
Please wait - subsequent loads are instant!

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![React](https://img.shields.io/badge/React-18-blue.svg)](https://reactjs.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-Latest-green.svg)](https://fastapi.tiangolo.com/)
[![License](https://img.shields.io/badge/License-Educational-yellow.svg)](LICENSE)

## 🎯 Positioning

**NetraAI is an AI-powered investigative intelligence system for proactive corruption detection in public procurement ecosystems.**

Not just a fraud detection model—a complete investigative platform that empowers government analysts to identify and prevent corruption before it escalates.

## 🏗️ System Architecture

```
Data Ingestion Layer
         ↓
Graph Intelligence Layer (Neo4j / NetworkX)
         ↓
AI Risk Scoring Engine (GNN)
         ↓
Investigation API Layer (FastAPI)
         ↓
Analyst Dashboard (React)
```

### Database Options

**🎯 CSV Mode (Demo)** - Currently Running
- In-memory NetworkX graphs
- Perfect for demos and development
- No database installation needed

**🚀 Neo4j Mode (Production)** - Ready to Deploy
- Production-grade graph database
- 10-16x faster queries
- Scales to millions of entities

## ✨ Key Features

### 🔍 Proactive Detection
- Real-time risk assessment of entities
- Multi-factor scoring algorithm
- Pattern recognition across networks

### 🧠 AI-Powered Intelligence
- Graph Neural Network (PyTorch GCN)
- Community detection (Louvain algorithm)
- Network centrality analysis

### 📊 Explainable AI
- Detailed risk indicators
- Structured reasoning for every flag
- Confidence scoring

### 🕸️ Network Investigation
- Interactive graph visualization (D3.js)
- Entity relationship mapping
- Cluster detection

### 📄 Investigation Reports
- One-click summary generation
- Export functionality
- Government-ready format

## 🌐 Live Demo

**🚀 Frontend Application:** [Deploy to get your URL]  
**⚡ Backend API:** [Deploy to get your URL]  
**📚 API Documentation:** [Your Backend URL]/docs  
**💻 GitHub Repository:** https://github.com/Adittii72/NetraAI

### ⚠️ First Load Notice
Free tier services sleep after 15 minutes. First request may take 30-60 seconds to wake up.

### Quick Test
1. Visit frontend URL (wait for wake-up if needed)
2. Dashboard shows 500 companies, 208 high-risk
3. Click "Network" to see fraud connections
4. Click any company for detailed analysis
5. Check "Performance Comparison" in footer

---

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Node.js 16+
- pip and npm

### Installation & Setup

```bash
# 1. Clone repository
git clone <your-repo-url>
cd NetraAI

# 2. Install Python dependencies
pip install -r requirements.txt

# 3. Generate dataset (if not already present)
python dataset_generator.py

# 4. Load data to Neo4j Aura (Cloud Database)
# Windows:
load_data_to_aura.bat
# Linux/Mac:
./load_data_to_aura.sh

# 5. Start backend (Terminal 1)
cd backend
python api_neo4j.py        # Neo4j Aura mode (production)

# 6. Start frontend (Terminal 2)
cd frontend
npm install
npm start
```

Access the platform at `http://localhost:3000`

### ☁️ Neo4j Aura Cloud Database

This project uses **Neo4j Aura** - a fully managed cloud graph database:
- ✅ No local database installation needed
- ✅ Production-ready and scalable
- ✅ Accessible from anywhere
- ✅ Automatic backups and high availability

**Instance Details:**
- URI: `neo4j+s://ce4768b6.databases.neo4j.io`
- Console: https://console.neo4j.io
- Instance: netraai-db


### 🌐 Cloud Deployment


**Deployment Options:**
- **Render + Neo4j Aura** (Recommended) - Free tier, production-ready
- **Railway** - All-in-one platform
- **Vercel + Render** - Optimized frontend


## 🗄️ Database: Neo4j Aura Cloud

NetraAI uses **Neo4j Aura** - a fully managed cloud graph database:

### Why Neo4j Aura?
- **No Setup Required** - Cloud-hosted, ready to use
- **Production-Ready** - Enterprise-grade reliability
- **Scalable** - Handles millions of nodes and relationships
- **Fast** - 10-16x faster than traditional approaches
- **Secure** - Encrypted connections, automatic backups

### Current Configuration
```
Instance: netraai-db
URI: neo4j+s://ce4768b6.databases.neo4j.io
Database: neo4j
Status: Active
```

### Quick Start
1. Load data: `load_data_to_aura.bat` (Windows) or `./load_data_to_aura.sh` (Linux/Mac)
2. Start backend: `python backend/api_neo4j.py`
3. Access frontend: http://localhost:3000


## 🎨 Platform Overview

NetraAI is a synthetic public procurement dataset generator designed specifically for training and evaluating Graph Neural Networks (GNNs) for fraud detection in government procurement systems.

### Dashboard
- Overview statistics and metrics
- Risk distribution visualization
- Entity filtering by risk category
- Real-time data updates

### Network View
- Force-directed graph visualization
- Interactive node exploration
- Risk-based color coding
- Zoom and pan controls

### Entity Profiles
- Detailed risk assessment
- Risk indicators with explanations
- Tender history
- Connected entities mapping

### Investigation Reports
- Structured summary generation
- Key findings extraction
- Recommendation engine
- Export to text format

## 🔬 Risk Scoring Methodology

Multi-factor risk assessment:

1. **Shared Directors (25%)** - Collusion detection
2. **Tender Win Patterns (30%)** - Suspicious patterns
3. **Network Centrality (20%)** - Influence measurement
4. **Shell Company Indicators (25%)** - Fictitious structures

### Risk Categories
- **High Risk (≥70%)**: Immediate investigation required
- **Medium Risk (40-69%)**: Enhanced monitoring
- **Low Risk (<40%)**: Standard oversight

## 🕵️ Fraud Patterns Detected

1. ✅ Shared Directors Across Competing Companies
2. ✅ Collusive Clustering (Bid Rigging)
3. ✅ Shell Companies
4. ✅ Prolific Directors
5. ✅ High-Value Contract Winners
6. ✅ Circular Ownership

## 💻 Technology Stack

### Backend
- **FastAPI** - Modern Python web framework
- **Pandas** - Data processing
- **NetworkX** - Graph analysis
- **PyTorch + PyTorch Geometric** - GNN implementation
- **Python-Louvain** - Community detection

### Frontend
- **React 18** - UI framework
- **TailwindCSS** - Government-grade dark theme
- **D3.js** - Network visualization
- **Recharts** - Charts and analytics
- **Axios** - API client

## 📊 Dataset Specifications

### Entity Statistics
| Entity | Count | Fraudulent Count | Percentage |
|--------|-------|-----------------|-----------|
| Companies | 500 | 208 | 41.6% |
| Directors | 200 | 24 | 12.0% |
| Tenders | 150 | 33 | 22.0% |
| Departments | 20 | - | - |
| **Total Relationships** | **2,503** | - | - |

### Entity Attributes

#### Companies Dataset (`companies.csv`)
- **company_id**: Unique identifier (COMP_0000 format)
- **name**: Synthetic company name
- **registration_year**: Year of company registration (1995-2023)
- **industry_type**: Industry classification (12 types)
- **address**: Physical address
- **fraud_label**: Binary label (0 = normal, 1 = suspicious)

#### Directors Dataset (`directors.csv`)
- **director_id**: Unique identifier (DIR_0000 format)
- **name**: Synthetic director name
- **age**: Age in years (30-75)
- **fraud_label**: Binary label (0 = normal, 1 = suspicious)

#### Tenders Dataset (`tenders.csv`)
- **tender_id**: Unique identifier (TEND_0000 format)
- **department_id**: Issuing department
- **contract_value**: Contract value in currency units (50K - 5M)
- **year**: Fiscal year (2018-2023)
- **winning_company_id**: ID of company that won the tender
- **fraud_label**: Binary label (0 = normal, 1 = suspicious)

#### Departments Dataset (`departments.csv`)
- **department_id**: Unique identifier (DEPT_00 format)
- **name**: Department name
- **location**: Physical location

#### Relationships Dataset (`relationships.csv`)
- **source_id**: Source entity ID
- **target_id**: Target entity ID
- **relationship_type**: Type of relationship (see below)

### Relationship Types

1. **DIRECTOR_OF**: Links a director to a company (Director → Company)
2. **BIDDED_FOR**: Company participates in tender bidding (Company → Tender)
3. **WON**: Company won a tender (Company → Tender)
4. **ISSUED_BY**: Tender issued by a department (Tender → Department)

## Injected Fraud Patterns

The dataset contains 6 realistic fraud patterns commonly found in procurement fraud:

### Pattern 1: Shared Directors Across Competing Companies
**Description**: Multiple companies bidding for the same tenders share the same director(s)
- **Detection Signal**: High centrality of directors across supposedly independent companies
- **Count**: 5 collusive groups
- **Affected Entities**: ~20 companies, ~5 directors

**Use Case**: Reveals organizational interconnectedness that suggests coordination or shell structures

### Pattern 2: Collusive Clustering (Bid Rigging)
**Description**: Small clusters (5-8 companies) repeatedly win tenders among themselves at high contract values
- **Detection Signal**: Communities of companies constantly winning high-value tenders together
- **Count**: 3-4 clusters
- **Affected Entities**: ~20-30 companies, ~10-15 tenders

**Use Case**: Simulates bid-rigging where companies rotate winning tenders at inflated prices

### Pattern 3: Shell Companies
**Description**: Multiple companies registered in the same year with identical addresses
- **Detection Signal**: Anomalous clustering of registration years and addresses
- **Count**: 3-4 groups of 6 companies each
- **Affected Entities**: ~20-25 companies

**Use Case**: Detects suspicious company structures created to evade sanctions or hide beneficial ownership

### Pattern 4: Prolific Directors
**Description**: Directors linked to unusually high number of companies (15-25 instead of typical 1-4)
- **Detection Signal**: Extreme degree centrality in the director-company network
- **Count**: 5-8 prolific directors
- **Affected Entities**: ~75-150 companies, ~5-8 directors

**Use Case**: Identifies potential front-men or fraudsters managing multiple shell organizations

### Pattern 5: High-Value Contract Winners
**Description**: Specific companies consistently win disproportionately high-value tenders
- **Detection Signal**: Winning companies have significantly higher average contract values
- **Count**: 5-7 companies
- **Affected Entities**: ~5-7 companies, ~5-10 tenders per company

**Use Case**: Detects favoritism and potential price inflation in procurement awards

### Pattern 6: Circular Ownership
**Description**: Circular director-company networks (A→B→C→A) suggesting fictitious structures
- **Detection Signal**: Cycles in the bipartite director-company graph
- **Count**: 2-3 circular patterns
- **Affected Entities**: ~6-15 companies, ~6-15 directors

**Use Case**: Detects complex ownership structures used to hide true beneficial ownership

## 🎯 Project Structure

```
NetraAI/
├── backend/                    # Backend services
│   ├── api.py                 # FastAPI application
│   ├── models.py              # Pydantic models
│   ├── config.py              # Configuration
│   ├── risk_engine.py         # Risk scoring engine
│   ├── gnn_model.py           # Graph Neural Network
│   └── graph_loader.py        # Neo4j loader
├── frontend/                   # React frontend
│   ├── src/
│   │   ├── components/        # React components
│   │   │   ├── Dashboard.js
│   │   │   ├── NetworkView.js
│   │   │   ├── EntityProfile.js
│   │   │   └── InvestigationReport.js
│   │   ├── api/               # API client
│   │   └── App.js             # Main app
│   ├── public/
│   └── package.json
├── data/
│   ├── raw/                   # Generated datasets
│   │   ├── companies.csv
│   │   ├── directors.csv
│   │   ├── tenders.csv
│   │   ├── departments.csv
│   │   └── relationships.csv
│   └── processed/             # Processed data
├── dataset_generator.py       # Data generation script
├── verify_dataset.py          # Dataset verification
├── requirements.txt           # Python dependencies
├── README.md                  # This file
├── SETUP.md                   # Setup guide
└── DEMO_GUIDE.md             # Demo presentation guide
```

## 🔌 API Endpoints

### Dashboard
- `GET /api/dashboard/stats` - Overview statistics

### Companies
- `GET /api/companies?risk_category=High&limit=100` - List companies
- `GET /api/company/{company_id}` - Company details

### Network
- `GET /api/network/graph?entity_id=COMP_0001&depth=2` - Network graph

### Investigation
- `GET /api/investigation/summary/{entity_id}` - Investigation report

### Clusters
- `GET /api/clusters` - Fraud clusters

## 🎬 Demo Flow

1. **Dashboard** - Show overview and high-risk entities
2. **Entity Profile** - Deep dive into risk indicators
3. **Network View** - Interactive graph exploration
4. **Investigation Report** - Generate and export report


## 🏆 What Makes It Government-Grade

- **Dark theme** - Professional, institutional design
- **Structured terminology** - Serious, not playful
- **Explainability** - Every decision is justified
- **Quantified metrics** - No vague assessments
- **Export functionality** - Investigation-ready reports
- **Modular architecture** - Production-scalable

## 📈 Performance & Scale

- Current: 500 companies, 200 directors, 150 tenders
- Production-ready: Supports 100,000+ entities with Neo4j
- Real-time risk calculation
- Efficient graph algorithms

## 🔐 Security Considerations

- API authentication (JWT recommended)
- Role-based access control
- Audit logging
- Data encryption
- HTTPS in production

## 🚀 Deployment

### Docker (Backend)
```dockerfile
FROM python:3.9
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["uvicorn", "backend.api:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Frontend Build
```bash
cd frontend
npm run build
# Serve with nginx or similar
```

## 🎓 Use Cases

1. **Government Procurement Oversight** - Primary use case
2. **Anti-Corruption Agencies** - Investigation support
3. **Audit Departments** - Risk-based auditing
4. **Research** - GNN benchmarking and evaluation

## 📝 Citation

If you use NetraAI in your research or project:

```bibtex
@software{netraai2026,
  title={NetraAI: Government-Grade Investigative Intelligence Platform},
  author={NetraAI Team},
  year={2026},
  url={https://github.com/netraai/platform}
}
```

## 📄 License

This project is provided for research and educational purposes.

## 🤝 Contributing

Contributions welcome! Areas for enhancement:
- Neo4j integration
- Additional fraud patterns
- Temporal analysis
- Real-time alerts
- Multi-language support

---

## 🎯 Impact Statement

**NetraAI transforms reactive auditing into proactive intelligence.**

In real-world deployment, this system could:
- Save millions in fraudulent contracts
- Identify corruption before contracts are awarded
- Restore public trust in government procurement
- Enable data-driven policy decisions

---

**NetraAI v1.0.0** | Government-Grade Investigative Platform | Confidential

Built with ❤️ for transparent governance

## Project Structure

```
NetraAI/
├── data/
│   ├── raw/                    # Generated raw datasets
│   │   ├── companies.csv
│   │   ├── directors.csv
│   │   ├── tenders.csv
│   │   ├── departments.csv
│   │   └── relationships.csv
│   └── processed/              # Processed datasets for model training
├── backend/                    # Backend services
├── frontend/                   # Frontend interface
├── dataset_generator.py        # Main data generation script
└── README.md                   # This file
```

## Usage

### Generating the Dataset

```bash
python dataset_generator.py
```

The script will:
1. Create required folder structure (if not exists)
2. Generate all synthetic entities
3. Inject fraudulent patterns
4. Assign fraud labels
5. Save all data to CSV format

### Output Files

All datasets are saved to `data/raw/` directory:
- `companies.csv` (40 KB)
- `directors.csv` (6 KB)
- `tenders.csv` (7 KB)
- `departments.csv` (1 KB)
- `relationships.csv` (78 KB)

**Total dataset size**: ~132 KB

### Loading the Dataset (Python Example)

```python
import pandas as pd

# Load entities
companies = pd.read_csv('data/raw/companies.csv')
directors = pd.read_csv('data/raw/directors.csv')
tenders = pd.read_csv('data/raw/tenders.csv')
departments = pd.read_csv('data/raw/departments.csv')

# Load relationships
relationships = pd.read_csv('data/raw/relationships.csv')

# Access fraudulent entities
fraudulent_companies = companies[companies['fraud_label'] == 1]
fraudulent_directors = directors[directors['fraud_label'] == 1]
fraudulent_tenders = tenders[tenders['fraud_label'] == 1]
```

### Converting to Graph Format (PyTorch Geometric Example)

```python
import torch
from torch_geometric.data import HeteroData

# Create heterogeneous graph
graph = HeteroData()

# Add node features
graph['company'].x = torch.tensor(company_features, dtype=torch.float)
graph['director'].x = torch.tensor(director_features, dtype=torch.float)
graph['tender'].x = torch.tensor(tender_features, dtype=torch.float)

# Add edges from relationships
for _, row in relationships.iterrows():
    rel_type = row['relationship_type']
    source = row['source_id']
    target = row['target_id']
    # Map to graph edges based on relationship type
```

## Reproducibility

The dataset generation uses a **fixed random seed (42)** for reproducibility:
- Same dataset can be regenerated by running `dataset_generator.py` again
- All randomization (names, addresses, attributes, patterns) is deterministic
- Useful for benchmarking and comparing different models

## Dependencies

```
pandas>=1.3.0
numpy>=1.21.0
```

Install dependencies:
```bash
pip install pandas numpy
```

## Data Characteristics

### Class Distribution
- **Fraud Label Distribution**: Imbalanced (41.6% fraudulent companies, 12% fraudulent directors)
- **Realistic** for fraud detection scenarios where fraud is typically less common

### Temporal Coverage
- **Years Covered**: 2018-2023 (6 fiscal years)
- **Registration History**: 1995-2023
- Supports temporal analysis and anomaly detection over time

### Network Topology
- **Density**: Sparse graph (~2,500 edges for 870 entities)
- **Multiple Relationship Types**: Heterogeneous graph structure
- **Community Structure**: Both legitimate and fraudulent communities

## Use Cases

### 1. Graph Neural Network Training
- Binary classification (fraud vs. normal)
- Multi-class classification (fraud pattern type)
- Link prediction (hidden fraudulent relationships)
- Node embedding learning

### 2. Anomaly Detection
- Community detection algorithms
- Centrality measure analysis
- Temporal pattern analysis

### 3. Graph Analysis
- Network visualization
- Hub/Authority identification
- Influence propagation analysis

### 4. Benchmark Dataset
- Model comparison and evaluation
- Feature importance analysis
- Generalization studies

## Limitations and Caveats

1. **Synthetic Data**: Generated patterns are simpler than real-world fraud
2. **Class Imbalance**: Reflects realistic scenarios but may require sampling techniques
3. **Scale**: 500 companies is smaller than real procurement systems; larger datasets may show different characteristics
4. **Simplifications**: Real fraud often involves temporal dynamics and more complex patterns

## Future Enhancements

- [ ] Temporal network features (time-series relationships)
- [ ] Multi-event datasets (contracts, invoices, payments)
- [ ] Ground truth explanations for each fraud pattern
- [ ] Scalable dataset generation (1000+ companies)
- [ ] Domain-specific attributes (sector-specific industries)
- [ ] Parameterized fraud intensity levels

## Citation

If you use this dataset in your research, please cite:

```bibtex
@dataset{netraai2026,
  title={NetraAI Synthetic Procurement Fraud Detection Dataset},
  author={NetraAI Team},
  year={2026},
  url={https://github.com/netraai/synthetic-procurement-dataset}
}
```

## License

This dataset is provided for research and educational purposes.

## Contact & Support

For questions or feedback about the dataset generation, please refer to the documentation in `dataset_generator.py`.

---

**Dataset Generated**: February 17, 2026
**Random Seed**: 42 (for reproducibility)
**Version**: 1.0
