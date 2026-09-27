import streamlit as st
import pandas as pd
import joblib
from pathlib import Path
# ============================================================
# Page Configuration
# ============================================================

st.set_page_config(
    page_title="Customer Intelligence & Retention Decision Platform",
    page_icon="📊",
    layout="wide"
)

# ============================================================
# Load Model and Preprocessor
# ============================================================

BASE_DIR = Path(__file__).resolve().parent

MODEL_PATH = BASE_DIR / "logistic_model.pkl"
PREPROCESSOR_PATH = BASE_DIR / "preprocessor.pkl"

loaded_model = joblib.load(MODEL_PATH)
loaded_preprocessor = joblib.load(PREPROCESSOR_PATH)

# ============================================================
# Header
# ============================================================

st.title("📊 Customer Intelligence & Retention Decision Platform")

st.markdown(
    """
    ### Predict customer churn risk and support proactive retention decisions.

    This application uses a trained Machine Learning model to estimate
    the likelihood that a customer will churn.
    """
)

st.divider()


# ============================================================
# Application Layout
# ============================================================

col1, col2 = st.columns(2)


# ============================================================
# Customer Information
# ============================================================

with col1:

    st.subheader("👤 Customer Information")

    gender = st.selectbox(
        "Gender",
        ["Female", "Male"]
    )

    senior_citizen = st.selectbox(
        "Senior Citizen",
        [0, 1]
    )

    partner = st.selectbox(
        "Partner",
        ["Yes", "No"]
    )

    dependents = st.selectbox(
        "Dependents",
        ["Yes", "No"]
    )

    tenure = st.number_input(
        "Tenure (months)",
        min_value=0,
        max_value=100,
        value=12
    )


# ============================================================
# Service Information
# ============================================================

with col2:

    st.subheader("🌐 Service Information")

    phone_service = st.selectbox(
        "Phone Service",
        ["Yes", "No"]
    )

    multiple_lines = st.selectbox(
        "Multiple Lines",
        ["Yes", "No", "No phone service"]
    )

    internet_service = st.selectbox(
        "Internet Service",
        ["DSL", "Fiber optic", "No"]
    )

    online_security = st.selectbox(
        "Online Security",
        ["Yes", "No", "No internet service"]
    )

    online_backup = st.selectbox(
        "Online Backup",
        ["Yes", "No", "No internet service"]
    )


st.divider()


# ============================================================
# Additional Services
# ============================================================

st.subheader("🛠️ Additional Services")

col1, col2, col3 = st.columns(3)

with col1:

    device_protection = st.selectbox(
        "Device Protection",
        ["Yes", "No", "No internet service"]
    )

    tech_support = st.selectbox(
        "Tech Support",
        ["Yes", "No", "No internet service"]
    )


with col2:

    streaming_tv = st.selectbox(
        "Streaming TV",
        ["Yes", "No", "No internet service"]
    )

    streaming_movies = st.selectbox(
        "Streaming Movies",
        ["Yes", "No", "No internet service"]
    )


with col3:

    contract = st.selectbox(
        "Contract",
        ["Month-to-month", "One year", "Two year"]
    )

    paperless_billing = st.selectbox(
        "Paperless Billing",
        ["Yes", "No"]
    )


st.divider()


# ============================================================
# Billing Information
# ============================================================

st.subheader("💳 Billing Information")

col1, col2, col3 = st.columns(3)

with col1:

    payment_method = st.selectbox(
        "Payment Method",
        [
            "Electronic check",
            "Mailed check",
            "Bank transfer (automatic)",
            "Credit card (automatic)"
        ]
    )


with col2:

    monthly_charges = st.number_input(
        "Monthly Charges",
        min_value=0.0,
        value=70.0
    )


with col3:

    total_charges = st.number_input(
        "Total Charges",
        min_value=0.0,
        value=840.0
    )


st.divider()

# ============================================================
# Prediction
# ============================================================

if st.button(
    "🔍 Predict Customer Churn",
    use_container_width=True
):

    # --------------------------------------------------------
    # Create DataFrame for New Customer
    # --------------------------------------------------------

    new_customer = pd.DataFrame({
        "gender": [gender],
        "SeniorCitizen": [senior_citizen],
        "Partner": [partner],
        "Dependents": [dependents],
        "tenure": [tenure],
        "PhoneService": [phone_service],
        "MultipleLines": [multiple_lines],
        "InternetService": [internet_service],
        "OnlineSecurity": [online_security],
        "OnlineBackup": [online_backup],
        "DeviceProtection": [device_protection],
        "TechSupport": [tech_support],
        "StreamingTV": [streaming_tv],
        "StreamingMovies": [streaming_movies],
        "Contract": [contract],
        "PaperlessBilling": [paperless_billing],
        "PaymentMethod": [payment_method],
        "MonthlyCharges": [monthly_charges],
        "TotalCharges": [total_charges]
    })

    # --------------------------------------------------------
    # Preprocess New Customer
    # --------------------------------------------------------

    new_customer_processed = loaded_preprocessor.transform(
        new_customer
    )

    # --------------------------------------------------------
    # Make Prediction
    # --------------------------------------------------------

    prediction = loaded_model.predict(
        new_customer_processed
    )

    probability = loaded_model.predict_proba(
        new_customer_processed
    )

    # --------------------------------------------------------
    # Display Result
    # --------------------------------------------------------

    st.subheader("Prediction Result")

    if prediction[0] == "Yes":

        st.error("⚠️ Customer is likely to churn.")

    else:

        st.success("✅ Customer is likely to stay.")

    # --------------------------------------------------------
    # Display Probabilities
    # --------------------------------------------------------

    col1, col2 = st.columns(2)

    with col1:

        st.metric(
            "Probability of Staying",
            f"{probability[0][0]:.2%}"
        )

    with col2:

        st.metric(
            "Probability of Churning",
            f"{probability[0][1]:.2%}"
        )
