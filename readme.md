# Electro PI Dashboard

📊 A Streamlit Dashboard for Tracking & Analyzing All Company Projects at Electro PI 🧑🏻‍💻

## Overview

This Streamlit dashboard provides a comprehensive analysis of various aspects of Electro PI projects. It connects to a MySQL database to fetch and visualize data, offering insights into user registrations, subscriptions, bundles, 10k AI initiative, coupons, admins, capstones, and employment grants.

## Getting Started

### Prerequisites

- Python
- Streamlit
- MySQL Server

### Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/ahmedmgelwan/electro-pi-dashboard.git
   ```

2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Set up your MySQL database connection in the `utils.py` file.

## Running the Dashboard

```bash
streamlit run Main.py
```

Open your browser and navigate to [http://localhost:8501](http://localhost:8501/) to view the dashboard.

## Project Structure

### `Main.py`

- The main file containing the Streamlit app setup and layout.

### `utils.py`

- Utility functions for database connection, data loading, and plotting.

### `01_🧑‍🤝‍🧑_Users.py`, `02_📦_bundles.py`, ...

- Files for each specific analysis section, organized by project areas.

## Usage

1. Choose the desired section from the sidebar tabs.
2. Customize date filters and input parameters.
3. Explore visualizations and metrics for user analysis, bundles, 10k AI initiative, coupons, admins, capstones, and employment grants.
