import sys
import os
import random
from datetime import timedelta
import pandas as pd
import numpy as np

# Add parent directory to path to import database modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database.connection import engine, SessionLocal, Base
from database.models import MacroIndicator, ConsumerInsight

def generate_data():
    print("Initializing database schema...")
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    
    print("Generating mock dataset...")
    
    regions = {
        'North America': ['USA', 'Canada'],
        'Europe': ['UK', 'Germany', 'France'],
        'Asia': ['Japan', 'China', 'India'],
        'South America': ['Brazil', 'Argentina']
    }
    
    dates = pd.date_range(start='2018-01-01', end='2024-12-01', freq='MS')
    
    macro_records = []
    consumer_records = []
    
    for region, countries in regions.items():
        for country in countries:
            # Base values
            inflation = random.uniform(1.0, 3.0)
            gdp_growth = random.uniform(1.5, 4.0)
            unemp_rate = random.uniform(3.5, 7.0)
            csi = random.uniform(90.0, 110.0)
            digital_pay = random.uniform(20.0, 40.0)
            
            for date in dates:
                # Add some random walk / shock dynamics
                # 2020 COVID shock
                if date.year == 2020 and date.month in [3, 4, 5]:
                    gdp_growth -= random.uniform(1.0, 3.0)
                    unemp_rate += random.uniform(0.5, 2.0)
                    csi -= random.uniform(5.0, 15.0)
                    digital_pay += random.uniform(1.0, 3.0) # digital adoption spiked
                elif date.year == 2021 and date.month > 6:
                    inflation += random.uniform(0.2, 0.8) # Post-covid inflation
                elif date.year == 2022:
                    inflation += random.uniform(0.1, 0.5)
                    gdp_growth -= random.uniform(0.1, 0.3)
                else:
                    # Normal random walk
                    inflation = max(0.1, inflation + random.uniform(-0.3, 0.3))
                    gdp_growth = gdp_growth + random.uniform(-0.5, 0.5)
                    unemp_rate = max(1.0, unemp_rate + random.uniform(-0.2, 0.2))
                    csi = csi + random.uniform(-2.0, 2.0)
                    digital_pay = min(95.0, digital_pay + random.uniform(0.1, 1.0))
                
                macro_records.append({
                    'date': date.date(),
                    'country': country,
                    'region': region,
                    'inflation_rate': round(inflation, 2),
                    'gdp_growth': round(gdp_growth, 2),
                    'unemployment_rate': round(unemp_rate, 2)
                })
                
                consumer_records.append({
                    'date': date.date(),
                    'country': country,
                    'region': region,
                    'consumer_spending_index': round(csi, 2),
                    'digital_payment_adoption': round(digital_pay, 2)
                })

    df_macro = pd.DataFrame(macro_records)
    df_consumer = pd.DataFrame(consumer_records)
    
    print("Inserting data into database...")
    df_macro.to_sql('macro_indicators', con=engine, if_exists='append', index=False)
    df_consumer.to_sql('consumer_insights', con=engine, if_exists='append', index=False)
    
    print(f"Inserted {len(df_macro)} macro records and {len(df_consumer)} consumer records successfully!")

if __name__ == "__main__":
    generate_data()
