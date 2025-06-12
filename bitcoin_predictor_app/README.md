# Bitcoin Price Predictor

A Streamlit web application that predicts Bitcoin prices using linear regression. The app provides historical price visualization, price predictions, and training/testing data split analysis.

## Features

- Real-time Bitcoin price data from Yahoo Finance
- Next day and monthly price predictions
- Interactive 6-year price history visualization
- 80/20 training/testing data split visualization
- Current price metrics and statistics

## Installation

1. Clone this repository
2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

Run the app locally:
```bash
streamlit run app.py
```

## Data Sources

- Bitcoin price data: Yahoo Finance (BTC-USD)
- Historical data range: 6 years
- Update frequency: Real-time

## Model

- Algorithm: Linear Regression
- Training data: 80% of historical data
- Testing data: 20% of historical data (most recent)
- Features: Previous day's closing prices

## Files

- `app.py`: Main Streamlit application
- `predictor.py`: Price prediction model
- `data_loader.py`: Data fetching and processing
- `utils.py`: Utility functions
- `visualizer.py`: Data visualization functions

## Deployment

This app is ready for deployment on Streamlit Cloud. Simply connect your GitHub repository to Streamlit Cloud and deploy. 