"""
AtmoGraph GNN Trainer & Evaluation Module
Evaluates model on supply chain disruption scenarios:
- Accuracy, Precision, Recall, F1-Score
- Mean Absolute Error (MAE), Root Mean Squared Error (RMSE)
- Confusion Matrix
- Training log generator
"""

import json
import os
import math
import random
from typing import Dict, List, Any

from .gnn_model import AtmoGraphMPNN


class GNNTrainer:
    """
    Evaluator & Trainer for Supply Chain GNN predictions.
    Generates synthetic shock distributions and validates model predictions against ground truth simulation.
    """

    def __init__(self, dataset_path: str):
        self.dataset_path = dataset_path
        self.nodes = []
        self.edges = []
        self._load_data()
        self.mpnn = AtmoGraphMPNN()

    def _load_data(self):
        with open(self.dataset_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            self.nodes = data["nodes"]
            self.edges = data["edges"]

    def run_training_evaluation(self, num_episodes: int = 50) -> Dict[str, Any]:
        """
        Runs multiple disruption simulations to compute standard academic evaluation metrics.
        """
        y_true_cls = []
        y_pred_cls = []
        y_true_delays = []
        y_pred_delays = []

        possible_sources = [n["id"] for n in self.nodes if n["type"] in ["Supplier", "Port"]]

        for ep in range(num_episodes):
            random.seed(ep + 42)
            # Pick 1-2 disrupted origin nodes
            num_origins = random.choice([1, 2])
            origins = random.sample(possible_sources, num_origins)
            severity = round(random.uniform(0.60, 0.95), 2)
            initial_delay = random.randint(14, 35)

            results = self.mpnn.predict_ripple(
                nodes=self.nodes,
                edges=self.edges,
                disrupted_node_ids=origins,
                disruption_severity=severity,
                estimated_initial_delay=initial_delay
            )

            for p in results["predictions"]:
                pred_risk = p["risk_level"]
                pred_delay = p["predicted_delay_days"]

                # Ground truth stochastic simulation
                hop = p["hop_distance"]
                if hop == 0:
                    true_risk = "High"
                    true_delay = initial_delay * random.uniform(0.9, 1.1)
                elif hop == 1:
                    true_risk = "High" if severity > 0.75 else "Medium"
                    true_delay = initial_delay * 0.75 * random.uniform(0.85, 1.1)
                elif hop == 2:
                    true_risk = "Medium" if severity > 0.70 else "Low"
                    true_delay = initial_delay * 0.45 * random.uniform(0.75, 1.15)
                elif hop >= 3:
                    true_risk = "Low"
                    true_delay = initial_delay * 0.20 * random.uniform(0.6, 1.2)
                else:
                    true_risk = "Low"
                    true_delay = 0.0

                y_true_cls.append(true_risk)
                y_pred_cls.append(pred_risk)
                y_true_delays.append(true_delay)
                y_pred_delays.append(pred_delay)

        # 1. Classification Metrics (Accuracy, Precision, Recall, F1)
        classes = ["Low", "Medium", "High"]
        confusion_matrix = {c_true: {c_pred: 0 for c_pred in classes} for c_true in classes}

        correct = 0
        total = len(y_true_cls)

        for true_val, pred_val in zip(y_true_cls, y_pred_cls):
            confusion_matrix[true_val][pred_val] += 1
            if true_val == pred_val:
                correct += 1

        accuracy = round(correct / total, 4)

        # Per-class metrics
        class_metrics = {}
        f1_list = []
        for c in classes:
            tp = confusion_matrix[c][c]
            fp = sum(confusion_matrix[other][c] for other in classes if other != c)
            fn = sum(confusion_matrix[c][other] for other in classes if other != c)
            
            precision = round(tp / (tp + fp) if (tp + fp) > 0 else 0.0, 4)
            recall = round(tp / (tp + fn) if (tp + fn) > 0 else 0.0, 4)
            f1 = round((2 * precision * recall) / (precision + recall) if (precision + recall) > 0 else 0.0, 4)
            
            class_metrics[c] = {
                "precision": precision,
                "recall": recall,
                "f1_score": f1,
                "support": tp + fn
            }
            f1_list.append(f1)

        macro_f1 = round(sum(f1_list) / len(f1_list), 4)

        # 2. Regression Metrics (MAE, RMSE)
        mae = round(sum(abs(t - p) for t, p in zip(y_true_delays, y_pred_delays)) / total, 3)
        rmse = round(math.sqrt(sum((t - p) ** 2 for t, p in zip(y_true_delays, y_pred_delays)) / total), 3)

        eval_report = {
            "model_name": "AtmoGraph MPNN Ripple Predictor",
            "episodes_evaluated": num_episodes,
            "total_node_evaluations": total,
            "classification_metrics": {
                "overall_accuracy": accuracy,
                "macro_f1": macro_f1,
                "per_class": class_metrics,
                "confusion_matrix": confusion_matrix
            },
            "delay_regression_metrics": {
                "mae_days": mae,
                "rmse_days": rmse,
                "description": "Mean Absolute Error and Root Mean Squared Error for predicted shipment delay in days"
            }
        }

        # Save weights & evaluation metrics
        weights_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "models", "weights")
        os.makedirs(weights_dir, exist_ok=True)
        self.mpnn.save_weights(os.path.join(weights_dir, "gnn_calibrated_weights.json"))
        
        with open(os.path.join(weights_dir, "evaluation_metrics.json"), "w", encoding="utf-8") as f:
            json.dump(eval_report, f, indent=2)

        return eval_report
