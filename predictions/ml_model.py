"""
ML Model Loader - Loads the Random Forest model trained in Google Colab
Place your 5 files in the 'ml_model' folder:
- churn_model.pkl
- scaler.pkl
- feature_columns.json
- label_encoders.pkl
- model_info.json
"""

import joblib
import json
import pandas as pd
import numpy as np
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')

BASE_DIR = Path(__file__).resolve().parent.parent.parent

# Paths to ML files
MODEL_PATH = BASE_DIR / 'ml_model' / 'churn_model.pkl'
SCALER_PATH = BASE_DIR / 'ml_model' / 'scaler.pkl'
FEATURES_PATH = BASE_DIR / 'ml_model' / 'feature_columns.json'
ENCODERS_PATH = BASE_DIR / 'ml_model' / 'label_encoders.pkl'

# Global variables
model = None
scaler = None
feature_columns = []
encoders = {}

def load_ml_model():
    """Load the trained ML model from Google Colab files"""
    global model, scaler, feature_columns, encoders
    
    try:
        if MODEL_PATH.exists():
            model = joblib.load(MODEL_PATH)
            print("✅ ML Model loaded")
        if SCALER_PATH.exists():
            scaler = joblib.load(SCALER_PATH)
            print("✅ Scaler loaded")
        if FEATURES_PATH.exists():
            with open(FEATURES_PATH, 'r') as f:
                feature_columns = json.load(f)
            print(f"✅ Features loaded: {len(feature_columns)}")
        if ENCODERS_PATH.exists():
            encoders = joblib.load(ENCODERS_PATH)
            print("✅ Encoders loaded")
        return model is not None
    except Exception as e:
        print(f"⚠️ Error loading ML files: {e}")
        return False

def predict_single_customer(customer_data):
    """
    Predict churn for a single customer
    Returns: (prediction, probability)
    """
    global model, scaler, feature_columns
    
    # Check if ML model is available
    if model is None:
        loaded = load_ml_model()
        if not loaded:
            # FALLBACK: Rule-based prediction
            return fallback_prediction(customer_data)
    
    try:
        # Convert to DataFrame
        input_df = pd.DataFrame([customer_data])
        
        # Handle categorical columns if encoders exist
        for col, le in encoders.items():
            if col in input_df.columns:
                try:
                    input_df[col] = le.transform(input_df[col])
                except:
                    input_df[col] = 0
        
        # Ensure all feature columns exist
        for col in feature_columns:
            if col not in input_df.columns:
                input_df[col] = 0
        
        # Select only feature columns
        input_df = input_df[feature_columns]
        input_df = input_df.fillna(0)
        
        # Scale features
        input_scaled = scaler.transform(input_df)
        
        # Predict
        prediction = model.predict(input_scaled)[0]
        probability = model.predict_proba(input_scaled)[0][1]
        
        return int(prediction), float(probability)
        
    except Exception as e:
        print(f"Prediction error: {e}")
        return fallback_prediction(customer_data)

def fallback_prediction(customer_data):
    """Rule-based fallback when ML model is not available"""
    prob = 0.2  # Start with low risk
    
    days = customer_data.get('days_since_last_order', 0)
    orders = customer_data.get('total_orders', 0)
    complaints = customer_data.get('complaint_count', 0)
    
    if days > 30 and orders < 5:
        prob = 0.85
    elif days > 15 and orders < 10:
        prob = 0.55
    elif complaints > 2:
        prob = 0.70
    elif days > 60:
        prob = 0.90
    elif orders > 20:
        prob = 0.15
    
    return 1 if prob > 0.5 else 0, prob

def predict_bulk(customers_queryset):
    """Predict churn for multiple customers"""
    results = []
    
    for customer in customers_queryset:
        customer_dict = {
            'total_orders': customer.total_orders,
            'total_spent': customer.total_spent,
            'days_since_last_order': customer.days_since_last_order,
            'complaint_count': customer.complaint_count,
            'tenure': customer.tenure,
            'city_tier': customer.city_tier,
            'hour_spend_on_app': customer.hour_spend_on_app,
            'number_of_device_registered': customer.number_of_device_registered,
            'satisfaction_score': customer.satisfaction_score,
            'coupon_used': customer.coupon_used,
            'cashback_amount': customer.cashback_amount,
        }
        
        pred, prob = predict_single_customer(customer_dict)
        
        if prob > 0.7:
            risk = 'High'
        elif prob > 0.4:
            risk = 'Medium'
        else:
            risk = 'Low'
        
        results.append({
            'customer_id': customer.id,
            'prediction': pred,
            'probability': prob * 100,
            'risk_level': risk
        })
    
    return results