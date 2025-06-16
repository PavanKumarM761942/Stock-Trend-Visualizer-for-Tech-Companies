# Stock-Trend-Visualizer-for-Tech-Companies

# 📊 Inventory Analysis Dashboard

A Flask-based web application that allows users to visualize and analyze inventory data for various companies over selected months and years. It provides dynamic graphs and summary tables based on filtered inventory inputs.

---

## 🚀 Features

- 📁 Load inventory data from a CSV file
- 🏢 Filter by company, month, and year
- 📊 View:
  - Stock by Product
  - Average Price by Product
  - Total Stock & Price by Product
- 📈 Interactive graphs using Plotly
- 📋 Tabular summary with average and total statistics

---

## 🛠 Tech Stack

- **Backend:** Python (Flask)
- **Data Processing:** Pandas, NumPy, RegEx
- **Visualization:** Plotly Express
- **Frontend:** HTML with Jinja2 Templates, Bootstrap (via CDN)

---

## 📁 Project Structure

project/
│
├── app.py # Main Flask Application
├── static/
│ └── inventory.csv # Inventory dataset (required)
├── templates/
│ └── index.html # Main HTML template
└── README.md # Project Documentation


---

## ⚙️ Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/PavanKumarM761942/Stock-Trend-Visualizer-for-Tech-Companies****
cd inventory-dashboard


2. Create & Activate a Virtual Environment (Recommended)
Windows:
bash
python -m venv venv
venv\Scripts\activate


macOS/Linux:

bash
python3 -m venv venv
source venv/bin/activate

3. Install Dependencies
bash
pip install flask pandas plotly numpy

4. Run the App
python app.py

Then open your browser and go to:
http://localhost:5000
