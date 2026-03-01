# Mule Account Detection System 🚨

## 📌 Project Overview

This project detects suspicious mule accounts in a transaction network using graph analysis and rule-based risk scoring.

It analyzes transaction patterns to identify:

- Circular money flow  
- Accounts sending money to multiple users  
- Shared device usage  
- High-risk transaction behavior  

---

## 🧠 Technologies Used

- Python  
- pandas  
- networkx  
- matplotlib  

---

## ⚙️ How It Works

1. Loads transaction dataset  
2. Builds a directed transaction graph  
3. Detects suspicious patterns:
   - Circular transaction cycles  
   - High outgoing transactions  
   - Shared device usage  
4. Assigns risk scores to accounts  
5. Visualizes transaction network and risk levels  

---

## 📊 Features

✔ Transaction Network Graph  
✔ Circular Transaction Detection  
✔ Risk Scoring System  
✔ Suspicious Account Highlighting  
✔ Transaction Volume Analysis  
✔ Time-based Transaction Analysis  
