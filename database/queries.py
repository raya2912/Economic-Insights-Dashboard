import pandas as pd
from database.connection import engine
from sqlalchemy import text
import logging

logger = logging.getLogger("dashboard")

def get_macro_data(start_date=None, end_date=None, regions=None):
    """
    Fetch macroeconomic data based on filters.
    """
    query = "SELECT * FROM macro_indicators WHERE 1=1"
    params = {}
    
    if start_date:
        query += " AND date >= :start_date"
        params['start_date'] = start_date.strftime('%Y-%m-%d') if hasattr(start_date, 'strftime') else start_date
    if end_date:
        query += " AND date <= :end_date"
        params['end_date'] = end_date.strftime('%Y-%m-%d') if hasattr(end_date, 'strftime') else end_date
    if regions:
        # Prevent SQL injection while supporting varying sizes of lists
        placeholders = ', '.join([f":region_{i}" for i in range(len(regions))])
        query += f" AND region IN ({placeholders})"
        for i, region in enumerate(regions):
            params[f'region_{i}'] = region
            
    try:
        # Use SQLAlchemy text construct for cross-dialect compatibility
        df = pd.read_sql(text(query), engine, params=params)
        df['date'] = pd.to_datetime(df['date'])
        return df
    except Exception as e:
        logger.error(f"Error fetching macro data: {e}")
        raise e

def get_consumer_data(start_date=None, end_date=None, regions=None):
    """
    Fetch consumer insight data based on filters.
    """
    query = "SELECT * FROM consumer_insights WHERE 1=1"
    params = {}
    
    if start_date:
        query += " AND date >= :start_date"
        params['start_date'] = start_date.strftime('%Y-%m-%d') if hasattr(start_date, 'strftime') else start_date
    if end_date:
        query += " AND date <= :end_date"
        params['end_date'] = end_date.strftime('%Y-%m-%d') if hasattr(end_date, 'strftime') else end_date
    if regions:
        placeholders = ', '.join([f":region_{i}" for i in range(len(regions))])
        query += f" AND region IN ({placeholders})"
        for i, region in enumerate(regions):
            params[f'region_{i}'] = region
            
    try:
        df = pd.read_sql(text(query), engine, params=params)
        df['date'] = pd.to_datetime(df['date'])
        return df
    except Exception as e:
        logger.error(f"Error fetching consumer data: {e}")
        return pd.DataFrame()

def get_unique_regions():
    query = "SELECT DISTINCT region FROM macro_indicators ORDER BY region"
    try:
        df = pd.read_sql(text(query), engine)
        return df['region'].tolist()
    except Exception as e:
        logger.error(f"Error fetching regions: {e}")
        return []
