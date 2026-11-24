"""
AtmoGraph GNN Training Runner
Executes evaluation, computes academic metrics (Accuracy, F1, MAE, Confusion Matrix),
and outputs results for B.Tech project documentation.
"""

import sys
import os
import json

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.join(BASE_DIR, "backend"))

from app.models.trainer import GNNTrainer

def main():
    dataset_path = os.path.join(BASE_DIR, "backend", "app", "data", "supply_chain_dataset.json")
    print(f"Loading dataset from: {dataset_path}")
    trainer = GNNTrainer(dataset_path)
    print("Running 50 multi-hop disruption evaluation episodes...")
    metrics = trainer.run_training_evaluation(num_episodes=50)
    print("\n--- GNN Evaluation Results ---")
    print(f"Overall Accuracy: {metrics['classification_metrics']['overall_accuracy'] * 100:.2f}%")
    print(f"Macro F1-Score:   {metrics['classification_metrics']['macro_f1']:.4f}")
    print(f"Delay MAE (Days): {metrics['delay_regression_metrics']['mae_days']:.2f} days")
    print(f"Delay RMSE (Days):{metrics['delay_regression_metrics']['rmse_days']:.2f} days")
    print("\nPer-class Metrics:")
    for cls_name, val in metrics['classification_metrics']['per_class'].items():
        print(f"  Class {cls_name:6s} -> Precision: {val['precision']:.3f}, Recall: {val['recall']:.3f}, F1: {val['f1_score']:.3f}")
    print("\nConfusion Matrix:")
    print(json.dumps(metrics['classification_metrics']['confusion_matrix'], indent=2))

if __name__ == "__main__":
    main()
