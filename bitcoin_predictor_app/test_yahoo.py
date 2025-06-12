import yfinance as yf
from datetime import datetime, timedelta

def test_yahoo_finance():
    # Get today's date
    end_date = datetime.now().date()
    # Get date from 7 days ago
    start_date = end_date - timedelta(days=7)
    
    print(f"Testing Yahoo Finance data fetch")
    print(f"Start date: {start_date}")
    print(f"End date: {end_date}")
    
    try:
        # Download BTC-USD data
        df = yf.download('BTC-USD', 
                        start=start_date.strftime('%Y-%m-%d'), 
                        end=end_date.strftime('%Y-%m-%d'), 
                        progress=False)
        
        print("\nDataFrame Info:")
        print(f"Shape: {df.shape}")
        print("\nFirst few rows:")
        print(df.head())
        print("\nLast few rows:")
        print(df.tail())
        
        return True
    except Exception as e:
        print(f"\nError occurred: {str(e)}")
        return False

if __name__ == "__main__":
    test_yahoo_finance() 