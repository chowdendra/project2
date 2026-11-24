"""
AtmoGraph Data Generator
Generates realistic multi-tier global supply chain network dataset (Nodes & Edges)
and disruption news corpus for NLP entity & disruption extraction.
"""

import json
import os

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "backend", "app", "data")
os.makedirs(DATA_DIR, exist_ok=True)

# 1. Multi-tier global supply chain graph
nodes = [
    # Tier 3: Raw Materials
    {
        "id": "SUP-LITHIUM-01",
        "name": "Albemarle Salar Extraction",
        "type": "Supplier",
        "tier": "Tier-3",
        "industry": "Automotive / Energy",
        "country": "Chile",
        "location": "Atacama",
        "lead_time_days": 45,
        "inventory_buffer_days": 14,
        "criticality_score": 0.88,
        "financial_volume_mil": 650.0,
        "current_status": "Normal",
        "description": "High-purity brine lithium carbonate extraction for battery cathode production."
    },
    {
        "id": "SUP-SILICON-02",
        "name": "Shin-Etsu Silicon Crystals",
        "type": "Supplier",
        "tier": "Tier-3",
        "industry": "Electronics",
        "country": "Japan",
        "location": "Niigata",
        "lead_time_days": 30,
        "inventory_buffer_days": 20,
        "criticality_score": 0.92,
        "financial_volume_mil": 820.0,
        "current_status": "Normal",
        "description": "Electronic-grade silicon ingots and high-purity polysilicon wafers."
    },
    {
        "id": "SUP-COBALT-03",
        "name": "Katanga Cobalt Reserves",
        "type": "Supplier",
        "tier": "Tier-3",
        "industry": "Automotive / Energy",
        "country": "DR Congo",
        "location": "Kolwezi",
        "lead_time_days": 50,
        "inventory_buffer_days": 10,
        "criticality_score": 0.82,
        "financial_volume_mil": 420.0,
        "current_status": "Normal",
        "description": "Refined battery-grade cobalt cathode precursors."
    },
    {
        "id": "SUP-CHEM-04",
        "name": "BASF Specialty Chemicals",
        "type": "Supplier",
        "tier": "Tier-3",
        "industry": "Pharmaceuticals",
        "country": "Germany",
        "location": "Ludwigshafen",
        "lead_time_days": 21,
        "inventory_buffer_days": 25,
        "criticality_score": 0.85,
        "financial_volume_mil": 910.0,
        "current_status": "Normal",
        "description": "Reagents, active pharmaceutical precursors and organic synthesizers."
    },

    # Tier 2: Component Specialists
    {
        "id": "SUP-CHIP-TSMC",
        "name": "TSMC Fab 18",
        "type": "Supplier",
        "tier": "Tier-2",
        "industry": "Electronics",
        "country": "Taiwan",
        "location": "Tainan",
        "lead_time_days": 35,
        "inventory_buffer_days": 12,
        "criticality_score": 0.98,
        "financial_volume_mil": 3400.0,
        "current_status": "Normal",
        "description": "Advanced 3nm and 5nm logic semiconductor fabrication foundry."
    },
    {
        "id": "SUP-CHIP-ASML",
        "name": "ASML Veldhoven Optics",
        "type": "Supplier",
        "tier": "Tier-2",
        "industry": "Electronics",
        "country": "Netherlands",
        "location": "Veldhoven",
        "lead_time_days": 60,
        "inventory_buffer_days": 30,
        "criticality_score": 0.99,
        "financial_volume_mil": 2900.0,
        "current_status": "Normal",
        "description": "EUV photolithography equipment and precision optical stepper systems."
    },
    {
        "id": "SUP-BATT-CATL",
        "name": "CATL Battery Cells",
        "type": "Supplier",
        "tier": "Tier-2",
        "industry": "Automotive / Energy",
        "country": "China",
        "location": "Ningde",
        "lead_time_days": 28,
        "inventory_buffer_days": 15,
        "criticality_score": 0.91,
        "financial_volume_mil": 2100.0,
        "current_status": "Normal",
        "description": "LFP and NMC automotive prismatic and cylindrical lithium cell blocks."
    },
    {
        "id": "SUP-API-DIVI",
        "name": "Divi's Active Ingredients",
        "type": "Supplier",
        "tier": "Tier-2",
        "industry": "Pharmaceuticals",
        "country": "India",
        "location": "Hyderabad",
        "lead_time_days": 18,
        "inventory_buffer_days": 30,
        "criticality_score": 0.79,
        "financial_volume_mil": 550.0,
        "current_status": "Normal",
        "description": "Active Pharmaceutical Ingredients (API) for antibiotics and pain medications."
    },

    # Ports & Maritime Chokepoints (Logistics Hubs)
    {
        "id": "PORT-ROTTERDAM",
        "name": "Port of Rotterdam",
        "type": "Port",
        "tier": "Logistics Hub",
        "industry": "Multi-Industry",
        "country": "Netherlands",
        "location": "Rotterdam",
        "lead_time_days": 7,
        "inventory_buffer_days": 5,
        "criticality_score": 0.96,
        "financial_volume_mil": 4800.0,
        "current_status": "Normal",
        "description": "Europe's largest transshipment seaport handling 470 million tons of freight."
    },
    {
        "id": "PORT-SHANGHAI",
        "name": "Port of Shanghai (Yangshan)",
        "type": "Port",
        "tier": "Logistics Hub",
        "industry": "Multi-Industry",
        "country": "China",
        "location": "Shanghai",
        "lead_time_days": 5,
        "inventory_buffer_days": 6,
        "criticality_score": 0.97,
        "financial_volume_mil": 6200.0,
        "current_status": "Normal",
        "description": "World's busiest container port linking East Asia with European and American trade."
    },
    {
        "id": "PORT-SINGAPORE",
        "name": "Port of Singapore",
        "type": "Port",
        "tier": "Logistics Hub",
        "industry": "Multi-Industry",
        "country": "Singapore",
        "location": "Jurong",
        "lead_time_days": 4,
        "inventory_buffer_days": 7,
        "criticality_score": 0.94,
        "financial_volume_mil": 5100.0,
        "current_status": "Normal",
        "description": "Global premier transshipment hub connecting Indian Ocean and Pacific routes."
    },
    {
        "id": "PORT-LA-LONG-BEACH",
        "name": "Port of Los Angeles / Long Beach",
        "type": "Port",
        "tier": "Logistics Hub",
        "industry": "Multi-Industry",
        "country": "USA",
        "location": "California",
        "lead_time_days": 6,
        "inventory_buffer_days": 6,
        "criticality_score": 0.93,
        "financial_volume_mil": 4300.0,
        "current_status": "Normal",
        "description": "Primary Pacific gateway handling 35% of all containerized maritime imports into the US."
    },

    # Tier 1: Subsystem Assembly
    {
        "id": "MFG-BOSCH-AUTO",
        "name": "Bosch Mobility Stuttgart",
        "type": "Manufacturer",
        "tier": "Tier-1",
        "industry": "Automotive",
        "country": "Germany",
        "location": "Stuttgart",
        "lead_time_days": 14,
        "inventory_buffer_days": 10,
        "criticality_score": 0.90,
        "financial_volume_mil": 1800.0,
        "current_status": "Normal",
        "description": "Engine control units (ECU), ABS brake actuators, and automotive radar sensors."
    },
    {
        "id": "MFG-FOXCONN-01",
        "name": "Foxconn Zhengzhou Complex",
        "type": "Manufacturer",
        "tier": "Tier-1",
        "industry": "Electronics",
        "country": "China",
        "location": "Zhengzhou",
        "lead_time_days": 10,
        "inventory_buffer_days": 8,
        "criticality_score": 0.95,
        "financial_volume_mil": 4500.0,
        "current_status": "Normal",
        "description": "Precision electronic contract assembly for high-end smartphones and tablets."
    },
    {
        "id": "MFG-NOVARTIS-FORM",
        "name": "Novartis Drug Formulation",
        "type": "Manufacturer",
        "tier": "Tier-1",
        "industry": "Pharmaceuticals",
        "country": "Switzerland",
        "location": "Basel",
        "lead_time_days": 16,
        "inventory_buffer_days": 20,
        "criticality_score": 0.87,
        "financial_volume_mil": 1400.0,
        "current_status": "Normal",
        "description": "Sterile injectable ampoules, oncology therapeutics, and cardiovascular tablets."
    },

    # OEMs (Original Equipment Manufacturers - Finished Goods)
    {
        "id": "OEM-TESLA-GIGA",
        "name": "Tesla Gigafactory Berlin",
        "type": "Manufacturer",
        "tier": "OEM",
        "industry": "Automotive",
        "country": "Germany",
        "location": "Gruenheide",
        "lead_time_days": 8,
        "inventory_buffer_days": 6,
        "criticality_score": 0.92,
        "financial_volume_mil": 3100.0,
        "current_status": "Normal",
        "description": "Electric passenger vehicle assembly (Model Y) and structural battery pack integration."
    },
    {
        "id": "OEM-APPLE-GLOBAL",
        "name": "Apple Global Operations",
        "type": "Manufacturer",
        "tier": "OEM",
        "industry": "Electronics",
        "country": "USA",
        "location": "Cupertino",
        "lead_time_days": 7,
        "inventory_buffer_days": 7,
        "criticality_score": 0.96,
        "financial_volume_mil": 7500.0,
        "current_status": "Normal",
        "description": "Consumer smart hardware final packaging, iOS calibration, and firmware flashing."
    },
    {
        "id": "OEM-BMW-MUNICH",
        "name": "BMW Werk Munich",
        "type": "Manufacturer",
        "tier": "OEM",
        "industry": "Automotive",
        "country": "Germany",
        "location": "Munich",
        "lead_time_days": 9,
        "inventory_buffer_days": 8,
        "criticality_score": 0.89,
        "financial_volume_mil": 2800.0,
        "current_status": "Normal",
        "description": "Luxury sedans and electric drivetrains assembly lines."
    },

    # Warehouses & Logistics Distribution Centers
    {
        "id": "WH-DHL-EUROPE",
        "name": "DHL European Central Hub",
        "type": "Warehouse",
        "tier": "Distribution Hub",
        "industry": "Multi-Industry",
        "country": "Germany",
        "location": "Leipzig",
        "lead_time_days": 3,
        "inventory_buffer_days": 12,
        "criticality_score": 0.86,
        "financial_volume_mil": 1600.0,
        "current_status": "Normal",
        "description": "Air express sorting depot and temperature-controlled medical logistics terminal."
    },
    {
        "id": "WH-FEDEX-MEMPHIS",
        "name": "FedEx SuperHub Memphis",
        "type": "Warehouse",
        "tier": "Distribution Hub",
        "industry": "Multi-Industry",
        "country": "USA",
        "location": "Memphis",
        "lead_time_days": 2,
        "inventory_buffer_days": 10,
        "criticality_score": 0.88,
        "financial_volume_mil": 2200.0,
        "current_status": "Normal",
        "description": "Global freight sorting facility processing over 3.3 million shipments daily."
    },

    # Distributors & Retail Channels
    {
        "id": "DIST-AMAZON-EU",
        "name": "Amazon EU Fulfillment Network",
        "type": "Distributor",
        "tier": "Retail Distribution",
        "industry": "Electronics / Multi",
        "country": "Luxembourg",
        "location": "Luxembourg City",
        "lead_time_days": 2,
        "inventory_buffer_days": 5,
        "criticality_score": 0.91,
        "financial_volume_mil": 5800.0,
        "current_status": "Normal",
        "description": "Pan-European distribution network supplying prime next-day deliveries."
    },
    {
        "id": "DIST-BESTBUY-NA",
        "name": "Best Buy North America Supply",
        "type": "Retailer",
        "tier": "Retail Distribution",
        "industry": "Electronics",
        "country": "USA",
        "location": "Richfield",
        "lead_time_days": 3,
        "inventory_buffer_days": 7,
        "criticality_score": 0.82,
        "financial_volume_mil": 1900.0,
        "current_status": "Normal",
        "description": "Consumer electronics omnichannel retail chain spanning 1,000+ outlets."
    },
    {
        "id": "DIST-MCKESSON-MED",
        "name": "McKesson Healthcare Logistics",
        "type": "Distributor",
        "tier": "Retail Distribution",
        "industry": "Pharmaceuticals",
        "country": "USA",
        "location": "Irving",
        "lead_time_days": 1,
        "inventory_buffer_days": 14,
        "criticality_score": 0.94,
        "financial_volume_mil": 4200.0,
        "current_status": "Normal",
        "description": "Distributes 1/3 of all pharmaceuticals used across North American hospitals and pharmacies."
    }
]

edges = [
    # Upstream -> Component
    {"source": "SUP-LITHIUM-01", "target": "SUP-BATT-CATL", "relationship": "SUPPLIES_TO", "product": "Lithium Carbonate", "transit_time_days": 22, "shipping_mode": "Maritime", "dependency_weight": 0.85},
    {"source": "SUP-COBALT-03", "target": "SUP-BATT-CATL", "relationship": "SUPPLIES_TO", "product": "Cobalt Cathodes", "transit_time_days": 25, "shipping_mode": "Maritime", "dependency_weight": 0.75},
    {"source": "SUP-SILICON-02", "target": "SUP-CHIP-TSMC", "relationship": "SUPPLIES_TO", "product": "Pure Silicon Wafers", "transit_time_days": 6, "shipping_mode": "Air Freight", "dependency_weight": 0.95},
    {"source": "SUP-CHIP-ASML", "target": "SUP-CHIP-TSMC", "relationship": "SUPPLIES_TO", "product": "EUV Lithography Systems", "transit_time_days": 14, "shipping_mode": "Air Freight", "dependency_weight": 0.98},
    {"source": "SUP-CHEM-04", "target": "SUP-API-DIVI", "relationship": "SUPPLIES_TO", "product": "Chemical Precursors", "transit_time_days": 18, "shipping_mode": "Maritime", "dependency_weight": 0.70},

    # Component -> Maritime Ports
    {"source": "SUP-BATT-CATL", "target": "PORT-SHANGHAI", "relationship": "TRANSSHIPS_VIA", "product": "Battery Modules", "transit_time_days": 3, "shipping_mode": "Trucking", "dependency_weight": 0.90},
    {"source": "SUP-CHIP-TSMC", "target": "PORT-SINGAPORE", "relationship": "TRANSSHIPS_VIA", "product": "Microchips & Processors", "transit_time_days": 4, "shipping_mode": "Air Freight", "dependency_weight": 0.80},
    {"source": "SUP-API-DIVI", "target": "PORT-SINGAPORE", "relationship": "TRANSSHIPS_VIA", "product": "Bulk API Powder", "transit_time_days": 5, "shipping_mode": "Maritime", "dependency_weight": 0.65},

    # Inter-Port Maritime Corridors
    {"source": "PORT-SHANGHAI", "target": "PORT-ROTTERDAM", "relationship": "TRANSSHIPS_VIA", "product": "Containerized Cargo", "transit_time_days": 28, "shipping_mode": "Maritime", "dependency_weight": 0.85},
    {"source": "PORT-SINGAPORE", "target": "PORT-ROTTERDAM", "relationship": "TRANSSHIPS_VIA", "product": "Global Cargo Transshipment", "transit_time_days": 21, "shipping_mode": "Maritime", "dependency_weight": 0.80},
    {"source": "PORT-SHANGHAI", "target": "PORT-LA-LONG-BEACH", "relationship": "TRANSSHIPS_VIA", "product": "Trans-Pacific Electronics", "transit_time_days": 16, "shipping_mode": "Maritime", "dependency_weight": 0.90},

    # Ports & Specialists -> Tier 1 & Assemblers
    {"source": "PORT-ROTTERDAM", "target": "MFG-BOSCH-AUTO", "relationship": "SUPPLIES_TO", "product": "Semiconductors & Sensors", "transit_time_days": 2, "shipping_mode": "Rail", "dependency_weight": 0.78},
    {"source": "SUP-CHIP-TSMC", "target": "MFG-FOXCONN-01", "relationship": "SUPPLIES_TO", "product": "Bionic & M-Series SoCs", "transit_time_days": 2, "shipping_mode": "Air Freight", "dependency_weight": 0.95},
    {"source": "PORT-ROTTERDAM", "target": "MFG-NOVARTIS-FORM", "relationship": "SUPPLIES_TO", "product": "Specialty Chemical Drums", "transit_time_days": 3, "shipping_mode": "Rail", "dependency_weight": 0.72},
    {"source": "SUP-API-DIVI", "target": "MFG-NOVARTIS-FORM", "relationship": "SUPPLIES_TO", "product": "Antibiotic Base", "transit_time_days": 6, "shipping_mode": "Air Freight", "dependency_weight": 0.60},

    # Tier 1 -> OEMs
    {"source": "PORT-ROTTERDAM", "target": "OEM-TESLA-GIGA", "relationship": "SUPPLIES_TO", "product": "Imported Battery Cells", "transit_time_days": 3, "shipping_mode": "Rail", "dependency_weight": 0.88},
    {"source": "MFG-BOSCH-AUTO", "target": "OEM-TESLA-GIGA", "relationship": "SUPPLIES_TO", "product": "Braking & Steering Units", "transit_time_days": 2, "shipping_mode": "Trucking", "dependency_weight": 0.75},
    {"source": "MFG-BOSCH-AUTO", "target": "OEM-BMW-MUNICH", "relationship": "SUPPLIES_TO", "product": "Automotive Telematics & ECU", "transit_time_days": 1, "shipping_mode": "Trucking", "dependency_weight": 0.88},
    {"source": "MFG-FOXCONN-01", "target": "OEM-APPLE-GLOBAL", "relationship": "SUPPLIES_TO", "product": "Finished Smart Devices", "transit_time_days": 5, "shipping_mode": "Air Freight", "dependency_weight": 0.96},

    # OEMs & Producers -> Warehouses
    {"source": "OEM-TESLA-GIGA", "target": "WH-DHL-EUROPE", "relationship": "STORES_FOR", "product": "Service Parts & Vehicles", "transit_time_days": 1, "shipping_mode": "Trucking", "dependency_weight": 0.65},
    {"source": "OEM-BMW-MUNICH", "target": "WH-DHL-EUROPE", "relationship": "STORES_FOR", "product": "Finished Automobiles", "transit_time_days": 1, "shipping_mode": "Rail", "dependency_weight": 0.70},
    {"source": "OEM-APPLE-GLOBAL", "target": "WH-FEDEX-MEMPHIS", "relationship": "STORES_FOR", "product": "Consumer Electronics Stock", "transit_time_days": 2, "shipping_mode": "Air Freight", "dependency_weight": 0.90},
    {"source": "MFG-NOVARTIS-FORM", "target": "WH-DHL-EUROPE", "relationship": "STORES_FOR", "product": "Packaged Prescription Drugs", "transit_time_days": 1, "shipping_mode": "Trucking", "dependency_weight": 0.80},
    {"source": "MFG-NOVARTIS-FORM", "target": "DIST-MCKESSON-MED", "relationship": "SUPPLIES_TO", "product": "Bulk Hospital Formulations", "transit_time_days": 8, "shipping_mode": "Air Freight", "dependency_weight": 0.85},

    # Warehouses -> Retail Distributors
    {"source": "WH-DHL-EUROPE", "target": "DIST-AMAZON-EU", "relationship": "DISTRIBUTES_TO", "product": "E-Commerce Prime Parcels", "transit_time_days": 1, "shipping_mode": "Trucking", "dependency_weight": 0.82},
    {"source": "WH-FEDEX-MEMPHIS", "target": "DIST-BESTBUY-NA", "relationship": "DISTRIBUTES_TO", "product": "Retail Store Replenishment", "transit_time_days": 2, "shipping_mode": "Trucking", "dependency_weight": 0.88},
    {"source": "PORT-LA-LONG-BEACH", "target": "DIST-BESTBUY-NA", "relationship": "DISTRIBUTES_TO", "product": "Direct Import Consumer Tech", "transit_time_days": 3, "shipping_mode": "Trucking", "dependency_weight": 0.72}
]

supply_chain_data = {
    "project": "AtmoGraph",
    "version": "1.0",
    "description": "Multi-tier global supply chain network representing semiconductor, automotive, pharmaceutical, and logistics relationships.",
    "total_nodes": len(nodes),
    "total_edges": len(edges),
    "nodes": nodes,
    "edges": edges
}

# 2. Curated Disruption News Articles
news_samples = [
    {
        "id": "NEWS-001",
        "title": "Massive Dockworkers Strike Shuts Down Port of Rotterdam Container Terminals",
        "source": "Global Maritime Logistics Review",
        "published_at": "2026-11-20T08:30:00Z",
        "content": "Port of Rotterdam operations came to an abrupt halt this morning as over 3,000 crane operators and dockworkers launched an open-ended wage strike. More than 45 container vessels are stranded in the North Sea unable to offload critical automotive components, chemical supplies, and high-tech parts destined for German factories including BMW and Tesla Gigafactory Berlin. Logistics analysts predict delays of 25 to 35 days across European supply chains if the labor dispute remains unresolved.",
        "expected_event": "Labor Strike",
        "expected_location": "Port of Rotterdam, Netherlands",
        "expected_entity": "PORT-ROTTERDAM",
        "severity": "High",
        "category": "Transportation Disruption"
    },
    {
        "id": "NEWS-002",
        "title": "Magnitude 6.8 Earthquake Strikes Central Taiwan; TSMC Suspends Cleanroom Operations",
        "source": "Asia Tech Straits Herald",
        "published_at": "2026-11-21T14:15:00Z",
        "content": "A powerful 6.8 magnitude earthquake struck Tainan County in southern Taiwan, triggering automatic safety shutdowns at TSMC Fab 18. Precision ASML EUV lithography machinery experienced minor alignment distortions, and silicon wafer batches were discarded due to micro-vibrations. TSMC stated that safety inspections are underway, but output of 3nm Apple processors and automotive microcontrollers could face a disruption backlog of 3 to 4 weeks.",
        "expected_event": "Natural Disaster",
        "expected_location": "Taiwan, Tainan",
        "expected_entity": "SUP-CHIP-TSMC",
        "severity": "High",
        "category": "Facility & Production Halt"
    },
    {
        "id": "NEWS-003",
        "title": "Severe Drought Forces Water Rationing at Atacama Lithium Evaporation Fields in Chile",
        "source": "Mining & Clean Energy Bulletin",
        "published_at": "2026-11-18T11:00:00Z",
        "content": "Prolonged arid conditions in Northern Chile have forced regional authorities to enforce a 40% reduction in industrial groundwater pumping at Albemarle Salar extraction facilities. Lithium brine processing yields are anticipated to slump by 30% over the next quarter, threatening battery cathode supply schedules for CATL and subsequent European EV manufacturers.",
        "expected_event": "Resource & Environmental Restriction",
        "expected_location": "Chile, Atacama",
        "expected_entity": "SUP-LITHIUM-01",
        "severity": "Medium",
        "category": "Raw Material Shortage"
    },
    {
        "id": "NEWS-004",
        "title": "Cyberattack Knocks Out Dispatch and Telemetry Systems at Bosch Mobility Stuttgart",
        "source": "Automotive Cyber Defense Wire",
        "published_at": "2026-11-22T09:45:00Z",
        "content": "A sophisticated ransomware attack targeted Bosch Mobility's primary logistics integration server in Stuttgart yesterday evening. Automated warehouse robotics and just-in-time shipment dispatches to BMW Munich and Tesla Berlin have been halted as IT engineers isolate affected subnetworks. Plant managers estimate a 12 to 18 day delivery delay for critical vehicle electronic control units (ECU).",
        "expected_event": "Cyberattack",
        "expected_location": "Germany, Stuttgart",
        "expected_entity": "MFG-BOSCH-AUTO",
        "severity": "High",
        "category": "Cyber & Systems Failure"
    },
    {
        "id": "NEWS-005",
        "title": "Chemical Reactor Fire at BASF Ludwigshafen Complex Temporarily Halts Precursor Synthesis",
        "source": "European Chemical Weekly",
        "published_at": "2026-11-19T16:20:00Z",
        "content": "A contained chemical fire in building C-42 at BASF's Ludwigshafen flagship facility has resulted in an emergency shutdown of the organic synthesizer line. The facility provides active precursor chemicals for pharmaceutical manufacturers including Divi's Laboratories and Novartis formulation plants. While no casualties were reported, specialized catalyst replacement will take an estimated 15 days.",
        "expected_event": "Industrial Accident / Fire",
        "expected_location": "Germany, Ludwigshafen",
        "expected_entity": "SUP-CHEM-04",
        "severity": "Medium",
        "category": "Production Halt"
    },
    {
        "id": "NEWS-006",
        "title": "Red Sea Security Crisis Extends Containership Sailing Times Around Cape of Good Hope",
        "source": "Global Shipping Times",
        "published_at": "2026-11-23T07:10:00Z",
        "content": "Commercial container ships traveling between Shanghai, Singapore, and European destinations via the Suez Canal are actively diverting around South Africa's Cape of Good Hope due to regional missile threats. The detour adds 10 to 14 sailing days and escalates bunker fuel surcharges by 35%, causing widespread vessel stacking at Port of Rotterdam and delays in downstream consumer goods fulfillment at Amazon EU.",
        "expected_event": "Geopolitical & Maritime Blockage",
        "expected_location": "Suez Canal / Port of Rotterdam",
        "expected_entity": "PORT-ROTTERDAM",
        "severity": "High",
        "category": "Transportation Disruption"
    }
]

# Write files
with open(os.path.join(DATA_DIR, "supply_chain_dataset.json"), "w", encoding="utf-8") as f:
    json.dump(supply_chain_data, f, indent=2)

with open(os.path.join(DATA_DIR, "news_samples.json"), "w", encoding="utf-8") as f:
    json.dump(news_samples, f, indent=2)

print(f"Successfully generated:")
print(f"- {len(nodes)} nodes and {len(edges)} edges in supply_chain_dataset.json")
print(f"- {len(news_samples)} disruption news articles in news_samples.json")
