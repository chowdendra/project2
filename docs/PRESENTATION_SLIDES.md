# AtmoGraph: Supply Chain Ripple Effect Predictor
## B.Tech Final-Year Project Presentation Deck (15 Slides)
**Department of Artificial Intelligence & Data Science**

---

### Slide 1: Title Slide
- **Project Title**: AtmoGraph – AI-Augmented Supply Chain Ripple Effect Predictor
- **Sub-domain**: Graph Neural Networks (GNN) & Natural Language Processing (NLP)
- **Degree**: Bachelor of Technology in AI & Data Science
- **Speaker Notes**:
  > "Good morning respected evaluators and panel members. Today, we present AtmoGraph, an intelligent system designed to forecast multi-tier disruption cascades and shipment delays across global supply chain networks using NLP and Graph Neural Networks."

---

### Slide 2: Problem Statement & Motivation
- **The Challenge**: Contemporary manufacturing relies heavily on Just-In-Time (JIT) scheduling with low safety buffers.
- **The Blind Spot**: Traditional ERP and predictive maintenance models evaluate companies in isolation (univariate time-series like ARIMA).
- **The Consequence**: A single disruption (e.g. Suez Canal blockage, port dockers strike, Taiwan semiconductor fab halt) creates catastrophic shortages weeks later at distant OEMs.
- **Key Metric**: $9.6 Billion of global maritime trade delayed daily during major canal and port choke points.

---

### Slide 3: Proposed Solution – AtmoGraph
- **Core Concept**: Treat the global supply network as a directed property graph $\mathcal{G} = (\mathcal{V}, \mathcal{E})$ rather than tabular spreadsheets.
- **Tri-Pillar AI Architecture**:
  1. **Automated NLP Ingestion**: Extracts entities and classifies disruption severity from unstructured news alerts.
  2. **Neo4j / Knowledge Graph Engine**: Models multi-tier dependencies (Tier 3 raw materials $\to$ Tier 2 components $\to$ Ports $\to$ OEMs $\to$ Distribution).
  3. **Message Passing Neural Network (MPNN)**: Propagates disruption shocks downstream with inventory buffer damping.

---

### Slide 4: System Architecture Overview
- **Data Flow**:
  - Unstructured News $\to$ NLP Extraction Pipeline $\to$ Graph Node Mapping $\to$ GNN Forward Propagation $\to$ FastAPI REST Services $\to$ D3.js Visual Dashboard.
- **Interactive Visual Feedback**:
  - Live animated shockwaves traversing active supply links.
  - Interactive What-If Resilience Simulator.

---

### Slide 5: Module 1 – Graph Knowledge Base & Schema
- **Entity Types (23 Core Entities)**:
  - *Tier-3 Suppliers*: Albemarle Lithium (Chile), Shin-Etsu Silicon (Japan), BASF Chemicals (Germany).
  - *Tier-2 Specialists*: TSMC (Taiwan), ASML (Netherlands), CATL (China).
  - *Logistics Chokepoints*: Port of Rotterdam, Shanghai, Singapore, Los Angeles.
  - *Tier-1 Assemblers*: Bosch Mobility Stuttgart, Foxconn Zhengzhou, Novartis Basel.
  - *OEMs*: Tesla Gigafactory Berlin, Apple Global, BMW Munich.
  - *Distribution & Warehousing*: DHL Leipzig, FedEx Memphis, Amazon EU, Best Buy, McKesson.
- **Relationship Schema**: `SUPPLIES_TO`, `TRANSSHIPS_VIA`, `STORES_FOR`, `DISTRIBUTES_TO`.

---

### Slide 6: Module 2 – NLP Information Extraction Engine
- **Named Entity Recognition (NER)**:
  - Extracts Organizations (ORG) and Locations (GPE / LOC).
- **Disruption Classification Taxonomy**:
  - Labor Strikes, Natural Disasters, Geopolitical Blockades, Cyberattacks, Facility Fires, Port Congestion.
- **Temporal Parsing**:
  - Extracts numeric delay windows from news text (e.g. "delays of 25 to 35 days" $\to 30$ days).
- **Entity Linker**:
  - Resolves text mentions directly to unique graph database IDs (`PORT-ROTTERDAM`, `OEM-TESLA-GIGA`).

---

### Slide 7: Module 3 – Graph Neural Network (GNN) Formulation
- **Feature Vector $h_v^{(0)}$**:
  - Criticality score ($c_v$), normalized lead time ($t_v$), inventory buffer days ($b_v$), initial shock ($s_v$), annual trade volume ($v_v$), tier index ($\tau_v$).
- **Message Passing Rule**:
  $$m_v^{(k+1)} = \sum_{u \in \mathcal{N}_{in}(v)} w_{uv} \cdot \sigma\left(\mathbf{W}_{msg} h_u^{(k)} + b_{msg}\right)$$
- **Node Update**:
  $$h_v^{(k+1)} = \text{LeakyReLU}\left(\mathbf{W}_{upd} [h_v^{(k)} \,\|\, m_v^{(k+1)}] + b_{upd}\right)$$
- **Inventory Buffer Cushion**:
  $$\text{cushion} = \max\left(0.15, \, 1.0 - \frac{\text{buffer\_days}}{\text{incoming\_delay} + 1}\right)$$

---

### Slide 8: Module 4 – Interactive Network Dashboard
- **Technology Stack**: HTML5 / TailwindCSS / D3.js v7 / Lucide Icons / React.
- **Visual Features**:
  - Force-directed physics layout with zoom, pan, and industry filtering.
  - Node drill-down inspection displaying trade volumes, buffer days, and direct partners.
  - Particle shockwave ripple animations on active disruption corridors.
  - Real-time delay countdown meters.

---

### Slide 9: Experimental Results & Model Evaluation
- **Evaluation Protocol**: 50 stochastic multi-hop disruption trials across 1,150 node instances.
- **Classification Performance**:
  - **Overall Accuracy**: **80.26%**
  - **Macro F1-Score**: **0.7217**
  - **High Risk Precision**: **95.1%** | **Recall**: **66.4%** | **F1**: **0.782**
- **Regression Performance (Shipment Delays)**:
  - **Mean Absolute Error (MAE)**: **2.16 Days**
  - **Root Mean Squared Error (RMSE)**: **3.93 Days**

---

### Slide 10: Confusion Matrix Analysis
| Actual \ Predicted | Low Risk | Medium Risk | High Risk |
|---|---|---|---|
| **Actual Low** | **717** | 144 | 0 |
| **Actual Medium**| 29 | **109** | 5 |
| **Actual High** | 1 | 48 | **97** |
- **Insight**: Zero False Positives predicting High Risk for unaffected Low Risk entities; high precision for mission-critical alerts.

---

### Slide 11: Real-World Case Study – European Port Strike
- **Scenario**: 3,000 dockworkers strike at Port of Rotterdam.
- **Hop 0**: Port of Rotterdam marked Disrupted (Shock 0.85, 30 days direct delay).
- **Hop 1 (Direct Impact)**:
  - Tesla Gigafactory Berlin: +22.4 Days delay (High Risk).
  - Bosch Mobility Stuttgart: +18.2 Days delay (High Risk).
- **Hop 2 (Downstream Impact)**:
  - BMW Werk Munich: +14.6 Days delay (Medium Risk).
  - DHL European Hub: +11.2 Days delay (Medium Risk).
- **Hop 3 (Fulfillment Impact)**:
  - Amazon EU: +9.1 Days delay (Medium Risk).

---

### Slide 12: What-If Resilience Simulator
- **Proactive Mitigation Test**:
  - Strategy: Increase safety stock buffer by $+10$ days.
- **Simulation Outcome**:
  - Baseline Downstream Average Delay: **22.4 Days**
  - Mitigated Downstream Average Delay: **14.1 Days**
  - **Resilience Gain**: **8.3 Days Saved (-37% impact)** and 60% reduction in high-risk nodes.

---

### Slide 13: Technologies & Tools Used
- **Programming & Backend**: Python 3.13, FastAPI, Uvicorn, Pydantic.
- **Graph & Databases**: Neo4j, Cypher, NetworkX.
- **NLP & AI**: spaCy, HuggingFace Transformers, Rule-NER Hybrid Engine.
- **Machine Learning**: PyTorch Geometric, PyTorch, Scikit-Learn, NumPy.
- **Frontend & Visualization**: React, Vite, D3.js v7, Tailwind CSS, Lucide Icons.

---

### Slide 14: Limitations & Future Enhancements
- **Limitations**:
  - Dependent on news reporting timeliness and veracity.
  - Private enterprise supplier contracts are proprietary and simulated.
- **Future Work**:
  - Real-time AIS satellite vessel transponder telemetry tracking.
  - Reinforcement Learning for automated supplier purchase rerouting.
  - Multi-agent LLM negotiation bots for emergency air cargo booking.

---

### Slide 15: Conclusion & Q&A
- **Summary**: AtmoGraph bridges the gap between unstructured disruption news and structural graph message passing, demonstrating an 80.26% predictive accuracy and 2.16-day delay precision.
- **Live Demo Link**: `http://localhost:8000`
- **Thank You! Questions & Discussion Welcome.**
