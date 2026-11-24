# AtmoGraph: Supply Chain Ripple Effect Predictor
## Comprehensive B.Tech Final-Year Project Report & Synopsis
**Department of Artificial Intelligence & Data Science**

---

### Abstract
Global supply networks are deeply interconnected, multi-tier ecosystems where localized disturbances—such as maritime chokepoint strikes, semiconductor fab shutdowns, mineral export quotas, and geopolitical detours—rapidly cascade into systemic international shortages. Traditional supply chain management systems rely on isolated univariate time-series algorithms (ARIMA, LSTM) that treat individual suppliers as independent entities, failing to capture high-order topological dependencies and multi-hop ripple effects.

This project presents **AtmoGraph**, an end-to-end AI and Machine Learning system that predicts supply chain ripple effects. AtmoGraph integrates:
1. An **NLP Ingestion Engine** that monitors unstructured news text to extract named entities (organizations, ports, geographies) and classifies disruption events with automated severity and delay scoring.
2. A **Graph Knowledge Base** (Neo4j & in-memory graph engine) storing suppliers (Tier 3/2/1), logistics hubs, OEMs, and distribution channels with dependency edge attributes.
3. A **Message Passing Graph Neural Network (MPNN)** that propagates disruption shocks across directed multi-tier paths, incorporating inventory buffer damping and transit attenuations to classify node risk (Low, Medium, High) and estimate downstream delivery delays in days.
4. An **Interactive Web Dashboard** (FastAPI, React, D3.js) providing real-time shockwave visualizations and what-if resilience simulations.

On empirical evaluation across 50 multi-hop disruption trials, AtmoGraph achieved **80.26% overall classification accuracy**, a **Macro F1-score of 0.7217**, and a **Mean Absolute Error (MAE) of 2.16 days** on downstream delay regression.

---

### Chapter 1: Introduction & Problem Statement

#### 1.1 Background
Contemporary manufacturing relies heavily on Just-In-Time (JIT) production principles. While JIT minimizes warehouse holding costs, it drastically reduces inventory buffer cushions. A disturbance at a single Tier-3 raw material mine in Chile or a transshipment port in the Netherlands can halt assembly lines at automotive OEMs across Europe and retail fulfillment centers in North America.

#### 1.2 Problem Statement
Existing supply chain visibility software tools face three core limitations:
- **Data Fragmentation**: Supplier records, transit logs, and external news alerts reside in decoupled silos.
- **Lack of Relational Modeling**: Time-series models evaluate each node in isolation without factoring in directed graph network topology.
- **Latency in Risk Detection**: Disruption warnings from external events (strikes, fires, earthquakes) take days to be manually evaluated by supply chain analysts.

#### 1.3 Project Objectives
- Construct a realistic, multi-tier global supply chain network spanning semiconductor, automotive, pharmaceutical, and logistics sectors.
- Formulate an automated NLP pipeline for entity extraction and disruption classification from unstructured text.
- Formulate and train a Graph Neural Network message passing architecture to predict ripple effects.
- Implement what-if simulation capabilities for evaluating resilience strategies (buffer expansion, emergency rerouting).

---

### Chapter 2: Literature Review & Comparative Analysis

| Feature | Classical ERP Systems | Univariate Time-Series (ARIMA/LSTM) | AtmoGraph (Proposed) |
|---|---|---|---|
| **Data Structure** | Relational Tables (RDBMS) | Linear Sequential Vectors | Heterogeneous Directed Graphs |
| **Topology Awareness** | Static Bill-of-Materials (BOM) | None | Multi-Hop GNN Message Passing |
| **External Event Ingestion**| Manual user entry | Not supported | Automated NLP & NER Extraction |
| **Propagation Modeling** | Static deterministic rules | Heuristic lookup | Dynamic buffer absorption & edge damping |
| **Visual Analytics** | Tabular grids | Static line charts | Interactive D3.js Force Network & Shockwaves |

---

### Chapter 3: System Architecture & Module Decomposition

#### Module 1: Graph Database & Schema (Neo4j & Cypher)
- Nodes represent supply entities categorized by tier:
  - `Tier-3`: Raw material extractors (Lithium, Silicon, Cobalt, Chemicals).
  - `Tier-2`: Component specialists (ASML EUV optics, CATL battery cells, TSMC silicon fabs).
  - `Logistics Hub`: Maritime seaports (Rotterdam, Shanghai, Singapore, Los Angeles).
  - `Tier-1`: Subassembly manufacturers (Bosch Mobility, Foxconn, Novartis).
  - `OEM`: Original equipment assemblers (Tesla Gigafactory, Apple, BMW).
  - `Distribution & Retail`: Regional sorting hubs (DHL, FedEx) and omnichannel distributors (Amazon, Best Buy).
- Directed relationships:
  - `(:Supplier)-[:SUPPLIES_TO]->(:Manufacturer)`
  - `(:Supplier)-[:TRANSSHIPS_VIA]->(:Port)`
  - `(:Port)-[:TRANSSHIPS_VIA]->(:Port)`
  - `(:OEM)-[:STORES_FOR]->(:Warehouse)`
  - `(:Warehouse)-[:DISTRIBUTES_TO]->(:Distributor)`

#### Module 2: NLP Disruption Ingestion Engine
- Identifies supply entities via Named Entity Recognition (NER).
- Classifies disruption events into standard taxonomy: Labor Strike, Natural Disaster, Geopolitical Blockade, Cyberattack, Factory Fire, Port Congestion, and Raw Material Shortage.
- Resolves entity mentions directly to unique graph node identifiers (`node_id`).

#### Module 3: Graph Neural Network (MPNN)
- Encodes node features: Criticality $c_v$, Lead Time $t_v$, Buffer Days $b_v$, Shock Intensity $s_v$, Trade Volume $v_v$, and Tier Index.
- Propagates shocks through edge dependency weights with buffer damping:
  $$\text{cushion} = \max\left(0.15, \, 1.0 - \frac{\text{buffer\_days}}{\text{incoming\_delay} + 1}\right)$$
- Output heads classify risk level (Low, Medium, High) and estimate downstream delay days.

#### Module 4: Interactive Dashboard
- Single Page Application rendering dynamic D3.js force-directed networks, animated shockwaves, news analyzers, and resilience comparison drawers.

---

### Chapter 4: Mathematical Formulation of GNN Message Passing

Given directed supply chain graph $\mathcal{G} = (\mathcal{V}, \mathcal{E})$:
1. **Initial Node Embedding**:
   $$h_v^{(0)} = [c_v, \, \tilde{t}_v, \, \tilde{b}_v, \, s_v, \, \tilde{v}_v, \, \tau_v]^T$$
2. **Message Aggregation**:
   For each node $v$, incoming messages from immediate upstream suppliers $u \in \mathcal{N}_{in}(v)$:
   $$m_v^{(k+1)} = \sum_{u \in \mathcal{N}_{in}(v)} w_{uv} \cdot \sigma\left(\mathbf{W}_{msg} h_u^{(k)} + b_{msg}\right)$$
3. **Node State Update**:
   $$h_v^{(k+1)} = \text{LeakyReLU}\left(\mathbf{W}_{upd} [h_v^{(k)} \,\|\, m_v^{(k+1)}] + b_{upd}\right)$$
4. **Classification & Regression Heads**:
   $$\hat{y}_{risk} = \text{Softmax}(\mathbf{W}_{cls} h_v^{(K)} + b_{cls})$$
   $$\hat{d}_{delay} = \text{ReLU}(\mathbf{W}_{reg} h_v^{(K)} + b_{reg}) \times \text{Scale}$$

---

### Chapter 5: Experimental Results & Model Performance

The model was evaluated across 50 stochastic multi-hop disruption trials generating 1,150 node prediction instances:

```
Overall Classification Accuracy: 80.26%
Macro F1-Score:                  0.7217
Delay MAE (Mean Absolute Error): 2.16 Days
Delay RMSE:                      3.93 Days

Per-Class Performance:
  Class Low    -> Precision: 0.960, Recall: 0.833, F1: 0.892
  Class Medium -> Precision: 0.362, Recall: 0.762, F1: 0.491
  Class High   -> Precision: 0.951, Recall: 0.664, F1: 0.782

Confusion Matrix:
  Actual Low    -> Pred Low: 717, Pred Med: 144, Pred High: 0
  Actual Medium -> Pred Low:  29, Pred Med: 109, Pred High: 5
  Actual High   -> Pred Low:   1, Pred Med:  48, Pred High: 97
```

---

### Chapter 6: Case Study & What-If Resilience Analysis

#### Scenario: Port of Rotterdam Labor Strike
- **Trigger**: 3,000 dockworkers strike halting container unloading for 30 days.
- **Direct Impact (Hop 0)**: Port of Rotterdam marked Disrupted (Shock: 0.85).
- **First-Hop Impact (Hop 1)**:
  - Bosch Mobility Stuttgart: Delay +18.2 Days (High Risk).
  - Tesla Gigafactory Berlin: Delay +22.4 Days (High Risk).
- **Second-Hop Impact (Hop 2)**:
  - BMW Werk Munich: Delay +14.6 Days (Medium Risk).
  - DHL European Central Hub: Delay +11.2 Days (Medium Risk).
- **Resilience Mitigation Test**:
  - Proactively increasing safety stock inventory buffers by +10 days absorbed 37% of the shock, reducing average downstream delay from **22.4 days to 14.1 days** and cutting high-risk nodes by 60%.

---

### Chapter 7: Conclusion & Future Scope

AtmoGraph demonstrates the efficacy of fusing NLP information extraction with Graph Neural Networks for predictive supply chain management. By treating the global supply chain as an interconnected topological graph rather than disjoint time-series datasets, businesses can identify downstream vulnerabilities weeks in advance.

**Future Enhancements**:
- Integration with live AIS satellite vessel tracking feeds.
- Automated generation of alternative supplier procurement orders via reinforcement learning.
- Large Language Model (LLM) agents that draft negotiation memorandums during logistics disputes.
