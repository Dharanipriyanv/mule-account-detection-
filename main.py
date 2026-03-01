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
# 3. Suspicious Pattern Detection
# ==============================

print("\n--- Suspicious Activity Report ---\n")

risk_score = {node: 0 for node in G.nodes()}

# Rule 1: High Out-degree
for node in G.nodes():
    if G.out_degree(node) >= 2:
        print(f"{node} sends money to multiple accounts")
        risk_score[node] += 20

# Rule 2: Circular transactions
cycles = list(nx.simple_cycles(G))
if cycles:
    print("\nCircular Transaction Cycles Found:")
    for cycle in cycles:
        print(cycle)
        for account in cycle:
            risk_score[account] += 30

# Rule 3: Shared device usage
device_map = {}

for _, row in data.iterrows():
    device_map.setdefault(row['device'], []).append(row['sender'])

for device, users in device_map.items():
    if len(set(users)) > 1:
        print(f"\nMultiple accounts using same device: {device}")
        for user in users:
            risk_score[user] += 25

# ==============================
# 4. Print Risk Levels
# ==============================

print("\n--- Risk Scores ---\n")

for account, score in risk_score.items():
    level = "Low Risk" if score <= 30 else "Medium Risk" if score <= 60 else "High Risk"
    print(f"Account {account}: Score = {score} → {level}")

# ==============================
# 5. NETWORK GRAPH (Saved)
# ==============================

plt.figure(figsize=(8,6))
pos = nx.spring_layout(G, seed=42)
colors = ["red" if risk_score[node] > 50 else "green" for node in G.nodes()]

nx.draw(G, pos,
        with_labels=True,
        node_color=colors,
        node_size=3000,
        font_size=10)

plt.title("Transaction Network Graph")
plt.savefig("output/network_graph.png")
plt.close()


# ==============================
# 6. BAR GRAPH (Total Sent)
# ==============================

total_sent = data.groupby("sender")["amount"].sum()

plt.figure(figsize=(8,6))
total_sent.plot(kind="bar")
plt.title("Total Amount Sent by Each Account")
plt.ylabel("Amount")
plt.xlabel("Account")

plt.savefig("output/transaction_volume.png")
plt.close()

print("\n✅ Graphs saved in output folder!")
