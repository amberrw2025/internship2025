from datetime import datetime, timedelta, date
import streamlit as st

def format_price(price):
    """
    Format price with 2 decimal places and dollar sign.
    
    Args:
        price (float): Price to format
        
    Returns:
        str: Formatted price string
    """
    if price is None:
        return "N/A"
    return f"${price:,.2f}"

def handle_errors(error_message):
    """
    Display error message in Streamlit.
    
    Args:
        error_message (str): Error message to display
    """
    st.error(error_message)

def validate_date_range(start_date, end_date):
    """
    Validate the date range for Bitcoin data.
    Returns (is_valid, message).
    """
    if not isinstance(start_date, (date, datetime)) or not isinstance(end_date, (date, datetime)):
        return False, "Invalid date objects provided."

    # Convert date objects to datetime objects for comparison
    if not isinstance(start_date, datetime):
        start_date = datetime.combine(start_date, datetime.min.time())
    if not isinstance(end_date, datetime):
        end_date = datetime.combine(end_date, datetime.min.time())

    if start_date >= end_date:
        return False, "Start date must be before end date"
    if end_date > datetime.now():
        return False, "End date cannot be in the future"
    if start_date < datetime(2009, 1, 3):
        return False, "Start date cannot be before Bitcoin's creation (January 3, 2009)"
    return True, "" 