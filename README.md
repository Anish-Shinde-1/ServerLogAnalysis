# Web Log Analytics Suite

A modular Python-based pipeline for generating, parsing, and visualizing web server logs. This tool is designed to identify traffic patterns, monitor server performance, and detect security threats like brute-force attacks and path traversal.

---

## Features

* **Log Generation:** Create realistic synthetic Nginx-style logs with customizable distributions (Normal, Bot, and Attacker traffic).
* **Modular Pipeline:** Decoupled architecture with dedicated modules for Parsing, Analysis, and Visualization.
* **Security Insights:** Automatic detection of suspicious IPs, high-failure rates, and burst-attack patterns.
* **Interactive Dashboard:** A high-performance Streamlit interface featuring real-time metrics, Plotly charts, and exportable reports.

## Project Structure

* `generateLogs.py`: Script to generate synthetic `.log` files.
* `parser.py`: Extracting structured data from raw log strings.
* `analyser.py`: Aggregating metrics and detecting anomalies.
* `visualizer.py`: Streamlit-based dashboard logic.
* `models.py`: Core data classes (`Event`, `AggregateData`, `AnalysedReport`).
* `main.py`: The primary entry point connecting the pipeline.

## Installation & Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/Anish-Shinde-1/ServerLogAnalysis.git
   cd ServerLogAnalysis
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirement.txt
   ```

3. **Generate sample data:**
   ```bash
   python generateLogs.py
   ```

4. **Launch the Dashboard:**
   ```bash
   streamlit run main.py
   ```

## Analytics Coverage
* **Traffic:** Total requests, peak hours, and peak minutes.
* **Endpoints:** Most visited pages and success/failure rates per route.
* **Security:** Failed request counts by IP and identification of suspicious actors.
* **Performance:** Global error rates and response size distribution.
