import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, date, timedelta
import plotly.graph_objects as go
from data_loader import get_btc_data
from predictor import train_and_predict
from utils import validate_date_range

# Set page config
st.set_page_config(
    page_title="Bitcoin Price Prediction",
    page_icon="📈",
    layout="wide"
)

# App title and description
st.title("Bitcoin Price Prediction using Linear Regression")
st.markdown("""
This website predicts Bitcoin prices using linear regression. You can:
- Get predictions for the next day and one month ahead
- Adjust the lookback period for predictions
- View 6-year price history
""")

# Sidebar for date selection
st.sidebar.header("Date Range Selection")
start_date = st.sidebar.date_input(
    "Start Date",
    value=datetime.now() - timedelta(days=365*5)  # 5 years ago
)
end_date = st.sidebar.date_input(
    "End Date",
    value=datetime.now()
)

# Validate date range
is_valid, message = validate_date_range(start_date, end_date)
if not is_valid:
    st.error(message)
    st.stop()

# Convert dates to datetime objects for data fetching
start_datetime = datetime.combine(start_date, datetime.min.time())
end_datetime = datetime.combine(end_date, datetime.min.time())

# Model parameters
st.sidebar.header("Model Configuration")
params = {
    'lookback': st.sidebar.slider(
        "Lookback Period (days)",
        min_value=1,
        max_value=30,
        value=7,
        help="Number of past days to consider for prediction"
    )
}

# Fetch data
df = get_btc_data(start_datetime, end_datetime)

if df is not None and not df.empty:
    # Defensive check for 'Close' column
    if 'Close' not in df.columns or df['Close'].dropna().empty:
        st.error("No valid 'Close' price data available.")
        st.stop()
    
    # Display current price metrics
    current_price = df['Close'].dropna().iloc[-1].item()
    price_change = df['Close'].dropna().iloc[-1].item() - df['Close'].dropna().iloc[-2].item()
    price_change_pct = (price_change / df['Close'].dropna().iloc[-2].item()) * 100
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Current Price", f"${current_price:,.2f}")
    with col2:
        st.metric("24h Change", f"${price_change:,.2f}", f"{price_change_pct:.2f}%")
    with col3:
        st.metric("24h Volume", f"${df['Volume'].iloc[-1].item():,.0f}")
    
    # Create tabs for different views
    tab1, tab2, tab3 = st.tabs(["Predictions", "Historical Data", "6-Year Price History"])
    
    # Calculate predictions
    models, predictions, confidence_intervals = train_and_predict(df, params=params)
    
    with tab1:
        # Show prediction
        if predictions and 'linear' in predictions:
            pred_tab1, pred_tab2 = st.tabs(["Next Day Prediction", "One Month Prediction"])
            with pred_tab1:
                st.subheader("Next Day Price Prediction")
                pred = predictions['linear']
                lower, upper = confidence_intervals['linear']
                pred_change = pred - current_price
                pred_change_pct = (pred_change / current_price) * 100
                st.metric(
                    "Predicted Price",
                    f"${pred:,.2f}",
                    f"{pred_change_pct:+.2f}%"
                )
                st.info(f"95% Confidence Interval: ${lower:,.2f} - ${upper:,.2f}")
            with pred_tab2:
                st.subheader("One Month Price Prediction")
                daily_returns = df['Close'].pct_change().dropna()
                monthly_volatility = daily_returns.std() * np.sqrt(30)
                monthly_pred = current_price * (1 + (pred - current_price) / current_price * 30)
                monthly_lower = monthly_pred * (1 - 1.96 * monthly_volatility.item())
                monthly_upper = monthly_pred * (1 + 1.96 * monthly_volatility.item())
                monthly_change = monthly_pred - current_price
                monthly_change_pct = (monthly_change / current_price) * 100
                st.metric(
                    "One Month Prediction",
                    f"${monthly_pred:,.2f}",
                    f"{monthly_change_pct:+.2f}%"
                )
                st.info(f"95% Confidence Interval: ${monthly_lower:,.2f} - ${monthly_upper:,.2f}")
                st.warning("""
                Note: Monthly predictions are based on historical volatility and should be interpreted with caution.
                The cryptocurrency market is highly volatile and past performance is not indicative of future results.
                """)
        else:
            st.info("No prediction available.")
    
    with tab2:
        # Display historical data
        st.subheader("Historical Price Data")
        st.dataframe(
            df.style.format({
                'Open': '${:,.2f}',
                'High': '${:,.2f}',
                'Low': '${:,.2f}',
                'Close': '${:,.2f}',
                'Volume': '{:,.0f}'
            }),
            use_container_width=True
        )
    
    with tab3:
        st.subheader("Bitcoin Price History (6 Years) - Training/Testing Split")
        
        # Fetch 6-year historical data
        six_years_ago = datetime.now() - timedelta(days=365*6)
        
        try:
            # Use yfinance directly for simplicity
            import yfinance as yf
            btc_ticker = yf.Ticker("BTC-USD")
            hist_data = btc_ticker.history(start=six_years_ago, end=datetime.now())
            
            if not hist_data.empty:
                # Calculate 80/20 split
                total_points = len(hist_data)
                split_point = int(total_points * 0.8)
                
                # Split the data
                train_data = hist_data.iloc[:split_point]
                test_data = hist_data.iloc[split_point:]
                
                # Create chart with training and testing data
                fig = go.Figure()
                
                # Add training data (80%)
                fig.add_trace(go.Scatter(
                    x=train_data.index,
                    y=train_data['Close'],
                    mode='lines',
                    name='Training Data (80%)',
                    line=dict(color='#2E86AB', width=2)
                ))
                
                # Add testing data (20%)
                fig.add_trace(go.Scatter(
                    x=test_data.index,
                    y=test_data['Close'],
                    mode='lines',
                    name='Testing Data (20%)',
                    line=dict(color='#F24236', width=2)
                ))
                
                fig.update_layout(
                    title='Bitcoin Price - Training (80%) vs Testing (20%) Data',
                    xaxis_title='Date',
                    yaxis_title='Price (USD)',
                    height=500,
                    showlegend=True,
                    legend=dict(
                        yanchor="top",
                        y=0.99,
                        xanchor="left",
                        x=0.01
                    )
                )
                
                st.plotly_chart(fig, use_container_width=True)
                
                # Display split information
                st.info(f"📊 Data Split: {len(train_data):,} training points | {len(test_data):,} testing points")
                
                # Simple stats
                current_price = hist_data['Close'].iloc[-1]
                max_price = hist_data['High'].max()
                min_price = hist_data['Low'].min()
                
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Current Price", f"${current_price:,.2f}")
                with col2:
                    st.metric("6-Year High", f"${max_price:,.2f}")
                with col3:
                    st.metric("6-Year Low", f"${min_price:,.2f}")
            else:
                st.error("No data available")
                
        except Exception as e:
            st.error(f"Error loading data: {str(e)}")
            st.info("Please check your internet connection and try again.")
    
    # Add disclaimer
    st.markdown("---")
    st.markdown("""
    ### Disclaimer
    This app is for educational purposes only. The predictions are based on historical data and linear regression,
    and should not be used as financial advice. Cryptocurrency markets are highly volatile and unpredictable.
    Always do your own research before making any investment decisions.
    """)
else:
    st.error("Failed to fetch Bitcoin data. Please try again in a few minutes or try a different date range.") 