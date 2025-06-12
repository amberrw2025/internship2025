import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler
import streamlit as st

def prepare_features(df, lookback=7):
    """Prepare features for linear regression model."""
    # Calculate returns
    df['Returns'] = df['Close'].pct_change()
    
    # Drop NaN values
    df = df.dropna()
    
    # Prepare features
    X = []
    y = []
    
    for i in range(lookback, len(df)):
        # Create feature vector using past prices
        features = df['Close'].iloc[i-lookback:i].values
        X.append(features)
        y.append(df['Close'].iloc[i])
    
    # Convert to numpy arrays and ensure correct shape
    X = np.array(X).reshape(-1, lookback)  # Reshape to (n_samples, n_features)
    y = np.array(y)
    
    return X, y, df

def train_and_predict(df, model_type=None, params=None):
    """
    Train linear regression model and predict the next day's price.
    
    Args:
        df (pd.DataFrame): DataFrame containing Bitcoin price data
        model_type (str): Not used, kept for compatibility
        params (dict): Model parameters
        
    Returns:
        tuple: (models, predictions, confidence_intervals)
    """
    if df is None or len(df) < 30:
        return None, None, None
    
    # Default parameters
    default_params = {
        'lookback': 7
    }
    
    # Update parameters if provided
    if params:
        default_params.update(params)
    
    # Prepare features
    X, y, df = prepare_features(df, default_params['lookback'])
    
    # Scale the features
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    
    # Train Linear Regression
    model = LinearRegression()
    model.fit(X_scaled, y)
    
    # Make prediction for next day
    last_data = X_scaled[-1].reshape(1, -1)
    prediction = model.predict(last_data)[0].item()
    
    # Calculate confidence interval
    y_pred = model.predict(X_scaled)
    mse = np.mean((y - y_pred) ** 2)
    std = np.sqrt(mse)
    confidence_interval = (prediction - 1.96*std.item(), prediction + 1.96*std.item())
    
    return {'linear': model}, {'linear': prediction}, {'linear': confidence_interval} 