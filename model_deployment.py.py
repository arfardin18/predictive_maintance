# -*- coding: utf-8 -*-
"""model_deployment.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1e62dPA4Ikxv58nfZ4DPFpn65cVkcrwt4
"""

import pickle
import pandas as pd
import streamlit as st
from sklearn.preprocessing import StandardScaler,LabelEncoder
from sklearn.linear_model import LogisticRegression

#loaded the saved model
loaded_model = pickle.load(open('C:/Users/SHAIK/Downloads/deployment1/trained_model.pkl', 'rb'))

# Load the scaler
scaler_path = 'C:/Users/SHAIK/Downloads/deployment1/scaler.pkl'
with open(scaler_path, 'rb') as file:
    scaler = pickle.load(file)

# Load the encoder
encoder_path = 'C:/Users/SHAIK/Downloads/deployment1/encoder.pkl'
with open(encoder_path, 'rb') as file:
    encoder = pickle.load(file)

# Streamlit app title
st.title("Machine Failure Prediction")

# Sidebar for user input
st.sidebar.header('Input Parameters')

# Function to collect user input
def user_input_features():
    Type = st.sidebar.selectbox("Type", ['L', 'M', 'H'])
    air_temperature = st.sidebar.number_input("Air temperature [K]", value=300.0, min_value=200.0, max_value=400.0)
    process_temperature = st.sidebar.number_input("Process temperature [K]", value=310.0, min_value=200.0, max_value=500.0)
    rotational_speed = st.sidebar.number_input("Rotational speed [rpm]", value=1500.0, min_value=500.0, max_value=3000.0)
    torque = st.sidebar.number_input("Torque [Nm]", value=40.0, min_value=10.0, max_value=100.0)
    tool_wear = st.sidebar.number_input("Tool wear [min]", value=100.0, min_value=0.0, max_value=500.0)
    twf = st.sidebar.selectbox("TWF (Tool Wear Failure)", [0, 1])
    hdf = st.sidebar.selectbox("HDF (Heat Dissipation Failure)", [0, 1])
    pwf = st.sidebar.selectbox("PWF (Power Failure)", [0, 1])
    osf = st.sidebar.selectbox("OSF (Overstrain Failure)", [0, 1])
    rnf = st.sidebar.selectbox("RNF (Random Failure)", [0, 1])

    # Create a DataFrame with user inputs
    data = {
        'Type': Type,
        'Air temperature [K]': air_temperature,
        'Process temperature [K]': process_temperature,
        'Rotational speed [rpm]': rotational_speed,
        'Torque [Nm]': torque,
        'Tool wear [min]': tool_wear,
        'TWF': twf,
        'HDF': hdf,
        'PWF': pwf,
        'OSF': osf,
        'RNF': rnf
    }
    return pd.DataFrame(data, index=[0])

# Collect user inputs
df = user_input_features()

# Display user inputs
st.subheader("User Input Parameters")
st.write(df)

# Preprocess input data
numerical_features = ['Air temperature [K]', 'Process temperature [K]',
                      'Rotational speed [rpm]', 'Torque [Nm]', 'Tool wear [min]']
df[numerical_features] = scaler.transform(df[numerical_features])

# Map 'Type' to integers if the encoder expects integers
type_mapping = {'L': 0, 'M': 1, 'H': 2}
df['Type'] = df['Type'].map(type_mapping)

# Predict using the model
prediction = loaded_model.predict(df)
prediction_proba = loaded_model.predict_proba(df)

# Display prediction results
st.subheader("Prediction Result")
if prediction[0] == 1:
    st.write("**Prediction: Machine Failure**")
else:
    st.write("**Prediction: No Machine Failure**")

# Display prediction probabilities
st.subheader("Prediction Probabilities")
st.write(f"Probability of Machine Failure: {prediction_proba[0][1]:.2f}")
st.write(f"Probability of No Machine Failure: {prediction_proba[0][0]:.2f}")






