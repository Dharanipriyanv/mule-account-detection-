import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt

# ==============================
# 1. Load Data
# ==============================

data = pd.read_csv("transactions.csv")
print("\nTransaction Data:\n")
print(data)

# ==============================
# 2. Create Graph
# ==============================

G = nx.DiGraph()

for index, row in data.iterrows():
    G.add_edge(row['sender'], row['receiver'], amount=row['amount'])

# ==============================
# 3. Suspicious Pattern Detection
# ==============================

print("\n--- Suspicious Activity Report ---\n")

risk_score = {}

# Initialize risk score
for node in G.nodes():
    risk_score[node] = 0

# Rule 1: Multiple outgoing transfers
for node in G.nodes():
    if G.out_degree(node) >= 2:
        print(f"{node} sends money to multiple accounts")
        risk_score[node] += 20

# Rule 2: Circular money flow
cycles = list(nx.simple_cycles(G))

if cycles:
    print("\nCircular Transaction Cycles Found:")
    for cycle in cycles:
        print(cycle)
        for account in cycle:
            risk_score[account] += 30

# Rule 3: Shared devices
device_map = {}

for index, row in data.iterrows():
    device = row['device']
    sender = row['sender']
    
    if device not in device_map:
        device_map[device] = []
    
    device_map[device].append(sender)

for device, users in device_map.items():
    if len(set(users)) > 1:
        print(f"\nMultiple accounts using same device: {device}")
        for user in users:
            risk_score[user] += 25

# ==============================
# 4. Risk Classification
# ==============================

print("\n--- Risk Scores ---\n")

results = []

for account, score in risk_score.items():
    if score <= 30:
        level = "Low Risk"
    elif score <= 60:
        level = "Medium Risk"
    else:
        level = "High Risk"

    print(f"Account {account}: Score = {score} → {level}")

    results.append([account, score, level])

# ==============================
# 5. Save Report to Excel
# ==============================

report = pd.DataFrame(results, columns=["Account", "Risk Score", "Risk Level"])
report.to_excel("fraud_report.xlsx", index=False)

print("\n✅ Fraud report saved as fraud_report.xlsx")

# ==============================
# 6. Graph Visualization with Colors
# ==============================

color_map = []

for node in G.nodes():
    if risk_score[node] > 60:
        color_map.append("red")        # High risk
    elif risk_score[node] > 30:
        color_map.append("orange")     # Medium risk
    else:
        color_map.append("lightgreen") # Low risk

plt.figure(figsize=(8,6))
pos = nx.spring_layout(G)

nx.draw(
    G,
    pos,
    with_labels=True,
    node_size=3000,
    node_color=color_map,
    arrows=True
)

plt.title("Transaction Network (Red = High Risk)")
plt.show()

# ==============================
# 7. Fraud Alert Summary
# ==============================

high_risk = [acc for acc, score in risk_score.items() if score > 60]

if high_risk:
    print("\n🚨 HIGH RISK ACCOUNTS DETECTED 🚨")
    for acc in high_risk:
        print(">>", acc)
else:
    print("\nNo high-risk accounts detected.")
