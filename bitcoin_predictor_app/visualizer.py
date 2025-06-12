import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

def plot_closing_prices(df):
    """
    Plot Bitcoin closing prices with a 7-day moving average.
    
    Args:
        df (pd.DataFrame): DataFrame containing Bitcoin price data
    """
    if df is None or df.empty:
        st.error("No data available to plot")
        return
    
    # Calculate 7-day moving average
    df['MA7'] = df['Close'].rolling(window=7).mean()
    
    # Create the plot
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.plot(df['Date'], df['Close'], label='Closing Price', color='blue')
    ax.plot(df['Date'], df['MA7'], label='7-day Moving Average', color='red', linestyle='--')
    
    # Customize the plot
    ax.set_title('Bitcoin Price History')
    ax.set_xlabel('Date')
    ax.set_ylabel('Price (USD)')
    ax.legend()
    ax.grid(True)
    
    # Rotate x-axis labels for better readability
    plt.xticks(rotation=45)
    
    # Adjust layout to prevent label cutoff
    plt.tight_layout()
    
    # Display the plot in Streamlit
    st.pyplot(fig) 