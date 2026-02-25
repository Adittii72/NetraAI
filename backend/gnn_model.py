"""
NetraAI Graph Neural Network Model
GCN-based fraud detection model
"""

import torch
import torch.nn.functional as F
from torch_geometric.nn import GCNConv, global_mean_pool
from torch_geometric.data import HeteroData, Data
import pandas as pd
import numpy as np
from typing import Dict, Tuple
from sklearn.preprocessing import StandardScaler

class FraudDetectionGCN(torch.nn.Module):
    """Graph Convolutional Network for fraud detection"""
    
    def __init__(self, input_dim: int, hidden_dim: int = 64, output_dim: int = 2):
        super(FraudDetectionGCN, self).__init__()
        self.conv1 = GCNConv(input_dim, hidden_dim)
        self.conv2 = GCNConv(hidden_dim, hidden_dim)
        self.conv3 = GCNConv(hidden_dim, hidden_dim)
        self.fc = torch.nn.Linear(hidden_dim, output_dim)
        self.dropout = torch.nn.Dropout(0.3)
        
    def forward(self, x, edge_index):
        # First GCN layer
        x = self.conv1(x, edge_index)
        x = F.relu(x)
        x = self.dropout(x)
        
        # Second GCN layer
        x = self.conv2(x, edge_index)
        x = F.relu(x)
        x = self.dropout(x)
        
        # Third GCN layer
        x = self.conv3(x, edge_index)
        x = F.relu(x)
        
        # Classification layer
        x = self.fc(x)
        
        return F.log_softmax(x, dim=1)

class GraphDataProcessor:
    """Process tabular data into PyTorch Geometric format"""
    
    def __init__(self, data: Dict[str, pd.DataFrame]):
        self.companies = data['companies']
        self.directors = data['directors']
        self.tenders = data['tenders']
        self.relationships = data['relationships']
        self.scaler = StandardScaler()
        
    def prepare_graph_data(self) -> Data:
        """Convert data to PyTorch Geometric Data object"""
        
        # Create node mappings
        company_ids = self.companies['company_id'].tolist()
        director_ids = self.directors['director_id'].tolist()
        tender_ids = self.tenders['tender_id'].tolist()
        
        all_nodes = company_ids + director_ids + tender_ids
        node_to_idx = {node: idx for idx, node in enumerate(all_nodes)}
        
        # Prepare node features
        company_features = self._extract_company_features()
        director_features = self._extract_director_features()
        tender_features = self._extract_tender_features()
        
        # Combine all features
        all_features = np.vstack([company_features, director_features, tender_features])
        
        # Normalize features
        all_features = self.scaler.fit_transform(all_features)
        
        # Prepare labels (only for companies)
        labels = np.zeros(len(all_nodes), dtype=np.long)
        labels[:len(company_ids)] = self.companies['fraud_label'].values
        
        # Prepare edges
        edge_index = self._build_edge_index(node_to_idx)
        
        # Create PyG Data object
        data = Data(
            x=torch.FloatTensor(all_features),
            edge_index=torch.LongTensor(edge_index),
            y=torch.LongTensor(labels)
        )
        
        # Create train/val/test masks (only for companies)
        num_companies = len(company_ids)
        train_size = int(0.6 * num_companies)
        val_size = int(0.2 * num_companies)
        
        train_mask = torch.zeros(len(all_nodes), dtype=torch.bool)
        val_mask = torch.zeros(len(all_nodes), dtype=torch.bool)
        test_mask = torch.zeros(len(all_nodes), dtype=torch.bool)
        
        train_mask[:train_size] = True
        val_mask[train_size:train_size + val_size] = True
        test_mask[train_size + val_size:num_companies] = True
        
        data.train_mask = train_mask
        data.val_mask = val_mask
        data.test_mask = test_mask
        
        return data
    
    def _extract_company_features(self) -> np.ndarray:
        """Extract numerical features for companies"""
        features = []
        
        for _, company in self.companies.iterrows():
            # Registration year (normalized)
            reg_year = (company['registration_year'] - 1995) / (2023 - 1995)
            
            # Industry type (one-hot encoded - simplified to hash)
            industry_hash = hash(company['industry_type']) % 10 / 10.0
            
            # Address hash (for shell company detection)
            address_hash = hash(company['address']) % 100 / 100.0
            
            # Degree features (will be computed from graph)
            features.append([reg_year, industry_hash, address_hash, 0.0, 0.0])
        
        return np.array(features)
    
    def _extract_director_features(self) -> np.ndarray:
        """Extract numerical features for directors"""
        features = []
        
        for _, director in self.directors.iterrows():
            # Age (normalized)
            age_norm = (director['age'] - 30) / (75 - 30)
            
            # Name hash
            name_hash = hash(director['name']) % 100 / 100.0
            
            features.append([age_norm, name_hash, 0.0, 0.0, 0.0])
        
        return np.array(features)
    
    def _extract_tender_features(self) -> np.ndarray:
        """Extract numerical features for tenders"""
        features = []
        
        for _, tender in self.tenders.iterrows():
            # Contract value (log-normalized)
            value_norm = np.log1p(tender['contract_value']) / np.log1p(5000000)
            
            # Year (normalized)
            year_norm = (tender['year'] - 2018) / (2023 - 2018)
            
            # Department hash
            dept_hash = hash(tender['department_id']) % 20 / 20.0
            
            features.append([value_norm, year_norm, dept_hash, 0.0, 0.0])
        
        return np.array(features)
    
    def _build_edge_index(self, node_to_idx: Dict[str, int]) -> np.ndarray:
        """Build edge index for PyG"""
        edges = []
        
        for _, rel in self.relationships.iterrows():
            source = rel['source_id']
            target = rel['target_id']
            
            if source in node_to_idx and target in node_to_idx:
                source_idx = node_to_idx[source]
                target_idx = node_to_idx[target]
                
                # Add bidirectional edges
                edges.append([source_idx, target_idx])
                edges.append([target_idx, source_idx])
        
        return np.array(edges).T

def train_model(data: Data, model: FraudDetectionGCN, epochs: int = 200):
    """Train the GCN model"""
    optimizer = torch.optim.Adam(model.parameters(), lr=0.01, weight_decay=5e-4)
    
    model.train()
    for epoch in range(epochs):
        optimizer.zero_grad()
        out = model(data.x, data.edge_index)
        
        # Only compute loss on training nodes
        loss = F.nll_loss(out[data.train_mask], data.y[data.train_mask])
        loss.backward()
        optimizer.step()
        
        if (epoch + 1) % 20 == 0:
            # Evaluate
            model.eval()
            with torch.no_grad():
                pred = model(data.x, data.edge_index).argmax(dim=1)
                train_acc = (pred[data.train_mask] == data.y[data.train_mask]).sum().item() / data.train_mask.sum().item()
                val_acc = (pred[data.val_mask] == data.y[data.val_mask]).sum().item() / data.val_mask.sum().item()
            
            print(f'Epoch {epoch+1:03d}, Loss: {loss:.4f}, Train Acc: {train_acc:.4f}, Val Acc: {val_acc:.4f}')
            model.train()
    
    return model

def evaluate_model(data: Data, model: FraudDetectionGCN):
    """Evaluate model performance"""
    model.eval()
    with torch.no_grad():
        pred = model(data.x, data.edge_index).argmax(dim=1)
        
        test_acc = (pred[data.test_mask] == data.y[data.test_mask]).sum().item() / data.test_mask.sum().item()
        
        # Calculate precision, recall for fraud class
        test_pred = pred[data.test_mask]
        test_true = data.y[data.test_mask]
        
        tp = ((test_pred == 1) & (test_true == 1)).sum().item()
        fp = ((test_pred == 1) & (test_true == 0)).sum().item()
        fn = ((test_pred == 0) & (test_true == 1)).sum().item()
        
        precision = tp / (tp + fp) if (tp + fp) > 0 else 0
        recall = tp / (tp + fn) if (tp + fn) > 0 else 0
        f1 = 2 * precision * recall / (precision + recall) if (precision + recall) > 0 else 0
        
        print(f'\nTest Accuracy: {test_acc:.4f}')
        print(f'Precision: {precision:.4f}')
        print(f'Recall: {recall:.4f}')
        print(f'F1 Score: {f1:.4f}')
    
    return test_acc, precision, recall, f1

if __name__ == "__main__":
    import os
    import sys
    sys.path.append(os.path.dirname(__file__))
    
    from config import config
    
    # Load data
    print("Loading data...")
    data_dict = {
        'companies': pd.read_csv(os.path.join(config.DATA_DIR, 'companies.csv')),
        'directors': pd.read_csv(os.path.join(config.DATA_DIR, 'directors.csv')),
        'tenders': pd.read_csv(os.path.join(config.DATA_DIR, 'tenders.csv')),
        'relationships': pd.read_csv(os.path.join(config.DATA_DIR, 'relationships.csv'))
    }
    
    # Prepare graph data
    print("Preparing graph data...")
    processor = GraphDataProcessor(data_dict)
    graph_data = processor.prepare_graph_data()
    
    print(f"Graph: {graph_data.num_nodes} nodes, {graph_data.num_edges} edges")
    print(f"Features: {graph_data.x.shape}")
    
    # Initialize model
    print("\nInitializing GCN model...")
    model = FraudDetectionGCN(input_dim=graph_data.x.shape[1])
    
    # Train model
    print("\nTraining model...")
    model = train_model(graph_data, model, epochs=200)
    
    # Evaluate model
    print("\nEvaluating model...")
    evaluate_model(graph_data, model)
    
    # Save model
    os.makedirs(config.MODEL_DIR, exist_ok=True)
    model_path = os.path.join(config.MODEL_DIR, 'fraud_detection_gcn.pt')
    torch.save(model.state_dict(), model_path)
    print(f"\nModel saved to: {model_path}")
