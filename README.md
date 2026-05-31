# Economic Insights Dashboard

A professional interactive analytics dashboard that visualizes macroeconomic and consumer-related trends using Streamlit, Plotly, Pandas, and SQL.

## Features

* **Interactive UI**: Modern fintech-style dashboard with sidebar filters
* **Macro Trends**: Analysis of Inflation trends, GDP growth, and Unemployment rates
* **Consumer Insights**: Consumer spending patterns and digital payment adoption trends
* **Regional Comparison**: Choropleth maps and cross-country comparisons
* **Export**: Downloadable CSV and PDF reports

## Setup Instructions

### 1. Prerequisites
- Python 3.9+
- pip

### 2. Installation
Navigate to the project directory and run:

```bash
pip install -r requirements.txt
```

### 3. Database Configuration

The application uses SQLAlchemy, meaning it supports multiple SQL dialects (SQLite, PostgreSQL, MySQL).

1. Copy `.env.example` to `.env`:
   ```bash
   cp .env.example .env
   ```

2. Open `.env` and set your `DATABASE_URL`. By default, it uses a local SQLite database (`sqlite:///./economic_data.db`) which requires zero setup.
   - For PostgreSQL: `postgresql+psycopg2://user:password@localhost/dbname`
   - For MySQL: `mysql+pymysql://user:password@localhost/dbname`

### 4. Generate Data

Since this project requires data, a data generator script is included to generate realistic macroeconomic and consumer data and populate the database.

Run the data generator:
```bash
python data/data_generator.py
```

### 5. Run the Application

Start the Streamlit server:
```bash
streamlit run app.py
```

## Architecture

- `app.py`: Main Streamlit application
- `pages/`: Individual dashboard views
- `components/`: Reusable UI elements (charts, KPI cards, sidebar)
- `database/`: SQLAlchemy models, connection, and query abstractions
- `data/`: Mock data generation scripts
- `utils/`: Helpers for logging and data export
