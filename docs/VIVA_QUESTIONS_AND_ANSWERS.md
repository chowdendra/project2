# AtmoGraph: Viva-Voce Examination Q&A Guide
## Top 25 Questions & Detailed Technical Answers for External Examiners

---

### Q1: What is the core problem AtmoGraph solves?
**Answer**: Traditional supply chain analytics relies on isolated, univariate time-series data (e.g., predicting an individual company's inventory using ARIMA or LSTM). These models fail to capture relational network topology—how a disruption at an upstream raw material supplier or maritime chokepoint propagates across multi-tier tiers to affect downstream manufacturers and distributors. AtmoGraph solves this by combining NLP news extraction with Graph Neural Networks (GNNs) on a graph database to forecast multi-hop ripple effects and shipment delays.

---

### Q2: Why use Graph Neural Networks (GNN) instead of traditional Machine Learning?
**Answer**: Standard machine learning models (Random Forest, SVM, MLPs) assume that data samples are independent and identically distributed (i.i.d.). In supply networks, entities are inherently non-independent; their operational state is conditioned on their suppliers and logistics routes. GNNs operate directly on graph structure $\mathcal{G}=(\mathcal{V}, \mathcal{E})$ through message passing, aggregating feature vectors and topological dependencies from neighboring nodes to predict downstream node states.

---

### Q3: What is the Message Passing mechanism in your GNN?
**Answer**: At each layer $k$, every node $v$ receives messages from its incoming neighbors $u \in \mathcal{N}_{in}(v)$. The message is scaled by edge dependency weight $w_{uv}$ and transit time. The messages are aggregated (summed) and combined with the node's existing embedding $h_v^{(k)}$ through a non-linear activation (LeakyReLU). Over $K$ hops, nodes learn representations reflecting both their local attributes and distant multi-hop shockwaves.

---

### Q4: How does the NLP Ingestion Engine extract disruption intelligence?
**Answer**: The NLP pipeline uses a hybrid architecture:
1. **Named Entity Recognition (NER)** (via spaCy and statistical pattern matching) extracts company names, facilities, and geographic locations.
2. **Disruption Classification Taxonomy** categorizes events (Labor Strike, Natural Disaster, Geopolitical Blockade, Cyberattack, Factory Fire, etc.) and computes severity scores based on matched trigger keywords.
3. **Temporal Parser** extracts numeric delay mentions (e.g., "delayed for 3 to 4 weeks" $\to 24.5$ days).
4. **Entity Linker** resolves extracted text names to unique node identifiers in the graph database.

---

### Q5: Why is Neo4j used in this project?
**Answer**: Neo4j is a native graph database using the property graph model. Relational databases require expensive recursive multi-table SQL `JOIN` operations to trace supply chain paths, leading to exponential slowdowns with depth. In Neo4j, relationships are first-class entities with index-free adjacency, allowing constant-time traversal of multi-tier supply routes via Cypher queries.

---

### Q6: How does inventory buffer stock factor into your prediction?
**Answer**: Inventory buffer acts as a damping cushion. In our propagation formulation, downstream impact is modulated by:
$$\text{cushion\_ratio} = \max\left(0.15, \, 1.0 - \frac{\text{buffer\_days}}{\text{incoming\_delay} + 1}\right)$$
If a manufacturer has 20 days of buffer inventory and the upstream delay is 15 days, the buffer absorbs the shock, preventing assembly line shutdown.

---

### Q7: What are the input features for each node in the GNN?
**Answer**:
1. Criticality score $c_v \in [0, 1]$
2. Normalized lead time $t_v$
3. Normalized inventory buffer days $b_v$
4. Initial disruption shock intensity $s_v \in [0, 1]$
5. Normalized annual financial trade volume $v_v$
6. Tier encoding (Tier-3, Tier-2, Port, Tier-1, OEM, Distributor)

---

### Q8: What are the output predictions of AtmoGraph?
**Answer**:
1. **Node Risk Level** (Multi-class classification): Low, Medium, or High risk.
2. **Predicted Delay Days** (Regression): Estimated shipment delay in days.
3. **Propagation Trace**: Exact step-by-step path of shockwave transmission across the graph.

---

### Q9: What evaluation metrics did you achieve?
**Answer**:
Across 50 stochastic multi-hop disruption trials (1,150 evaluated node instances):
- **Overall Accuracy**: **80.26%**
- **Macro F1-Score**: **0.7217**
- **Delay MAE**: **2.16 Days**
- **Delay RMSE**: **3.93 Days**

---

### Q10: How do you handle class imbalance between Low and High risk nodes?
**Answer**: In any disruption, the majority of distant nodes remain Low Risk, causing class imbalance. We evaluated performance using **Macro F1-score** (which treats all classes equally regardless of support size) and inspected the complete Confusion Matrix to confirm that High Risk recall reached 66.4% and precision reached 95.1%.

---

### Q11: What happens if Neo4j is not running on the examiner's machine?
**Answer**: AtmoGraph includes a resilient dual-mode architecture: if Neo4j is offline, the system automatically falls back to an in-memory graph engine (`graph_engine.py`) with identical graph semantics and zero loss of functionality. Furthermore, `scripts/run_server.py` runs with standard Python libraries if third-party packages are pending installation.

---

### Q12: Can you explain a real-world supply chain crisis that mirrors AtmoGraph's capabilities?
**Answer**: The 2021 Suez Canal blockage by the *Ever Given* vessel stranded 369 ships carrying $9.6 billion of goods daily. It created multi-week delays across European automotive factories that were waiting for Asian microchips and batteries. AtmoGraph directly simulates such chokepoints and forecasts which specific OEMs and retailers will experience stockouts.

---

### Q13: What is the "What-If" simulation capability?
**Answer**: It allows supply chain planners to test proactive resilience strategies before disruptions occur—such as increasing safety stock by $+10$ days or rerouting freight via air cargo. The dashboard compares baseline vs. mitigated average delay and high-risk node counts.

---

### Q14: How does your GNN handle directed vs. undirected edges?
**Answer**: Supply chains are strictly directed: raw materials flow downstream from suppliers to manufacturers to retailers. Our message passing propagates forward along outgoing edges (`source` $\to$ `target`), accurately modeling the physical movement of components.

---

### Q15: What are the primary limitations of the current implementation?
**Answer**:
1. News credibility: assumes published news reports are accurate.
2. Data accessibility: proprietary commercial supply contracts are not publicly disclosed; model operates on open-source and simulated corporate relationship datasets.
3. Dynamic pricing: current version predicts temporal delay and operational risk rather than dynamic spot-market component price surges.
