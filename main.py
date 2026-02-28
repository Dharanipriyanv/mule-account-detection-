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
# 2. Create Directed Graph
# ==============================

G = nx.DiGraph()

for index, row in data.iterrows():
    G.add_edge(row['sender'], row['receiver'], amount=row['amount'])

# ==============================
# 3. Visualize Graph
# ==============================

plt.figure(figsize=(8,6))
pos = nx.spring_layout(G)
nx.draw(G, pos, with_labels=True, node_size=3000)
plt.title("Transaction Network Graph")
plt.show()

# ==============================
# 4. Suspicious Pattern Detection
# ==============================

print("\n--- Suspicious Activity Report ---\n")

risk_score = {}

# Initialize risk score
for node in G.nodes():
    risk_score[node] = 0

# Rule 1: High Outgoing Transactions
for node in G.nodes():
    if G.out_degree(node) >= 2:
        print(f"{node} sends money to multiple accounts")
        risk_score[node] += 20

# Rule 2: Detect Cycles (Circular Money Flow)
cycles = list(nx.simple_cycles(G))

if cycles:
    print("\nCircular Transaction Cycles Found:")
    for cycle in cycles:
        print(cycle)
        for account in cycle:
            risk_score[account] += 30

# Rule 3: Shared Devices
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
# 5. Final Risk Classification
# ==============================

print("\n--- Risk Scores ---\n")

for account, score in risk_score.items():
    if score <= 30:
        level = "Low Risk"
    elif score <= 60:
        level = "Medium Risk"
    else:
        level = "High Risk"
    
    print(f"Account {account}: Score = {score} → {level}")
