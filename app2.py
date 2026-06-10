import streamlit as st
import pandas as pd
import plotly.express as px
import random

st.set_page_config(
    page_title="India e-Governance Portal",
    page_icon="🇮🇳",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
    <style>
    .main-header {
        background: linear-gradient(90deg, #FF9933 0%, #FFFFFF 50%, #138808 100%);
        padding: 20px;
        border-radius: 10px;
        text-align: center;
        margin-bottom: 20px;
    }
    .title-text { font-size: 40px; font-weight: bold; color: #1a1a1a; }
    .feature-card {
        background-color: white;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        height: 100%;
        text-align: center;
    }
    .back-btn {
        background-color: #f0f0f0;
        padding: 10px 20px;
        border-radius: 5px;
        text-decoration: none;
        color: #333;
    }
    </style>
""", unsafe_allow_html=True)

# --- MOCK DATA ---
STATES = ["Maharashtra", "Delhi", "Karnataka", "Tamil Nadu", "Uttar Pradesh"]
GOVT_JOBS = [
    {"post": "UPSC CSE 2024", "last_date": "2024-03-15", "qualification": "Graduate", "vacancies": 1105},
    {"post": "SSC CHSL", "last_date": "2024-04-01", "qualification": "12th Pass", "vacancies": 4500},
    {"post": "Railway NTPC", "last_date": "2024-04-10", "qualification": "Graduate", "vacancies": 3500},
]
SCHEMES = [
    {"name": "PM Kisan", "amount": "₹6000/yr", "category": "Agriculture"},
    {"name": "Ayushman Bharat", "amount": "₹5L", "category": "Health"},
    {"name": "PM Awas Yojana", "amount": "₹1.5L", "category": "Housing"},
]
INDIA_GDP = pd.DataFrame({
    "State": STATES,
    "GDP": [380000, 280000, 240000, 230000, 200000],
    "Literacy": [84.8, 80.1, 75.4, 78.0, 69.7]
})

# --- FIX: GET CURRENT PAGE FROM URL ---
query_params = st.query_params
current_page = query_params.get("page", "Home")

# --- NAVIGATION FUNCTION ---
def go_home():
    st.query_params["page"] = "Home"
    st.rerun()

def navigate_to(page_name):
    st.query_params["page"] = page_name
    st.rerun()

# --- HOME PAGE ---
def show_home():
    st.markdown("""
    <div class="main-header">
        <div class="title-text">🇮🇳 Digital India e-Governance</div>
        <div>One Nation - One Platform - One Solution</div>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Aadhaar Cards", "1.35B +")
    col2.metric("DigiLocker Docs", "650Cr +")
    col3.metric("Govt Schemes", "1500+")
    col4.metric("Digital Payments", "₹8000B")
    
    st.markdown("### 🖥️ Select Service")
    
    # Row 1
    row1 = st.columns(4)
    features = [("💰 Schemes", "Find Benefits", "Schemes"), 
                ("📄 Documents", "Verify GST/PAN", "Utilities"), 
                ("💼 Jobs", "Sarkari Naukri", "Jobs"), 
                ("🧮 Tax", "Tax Calculator", "Tax")]
    
    for i, (icon, desc, key) in enumerate(features):
        with row1[i]:
            st.markdown(f'<div class="feature-card"><h3>{icon}</h3><p>{desc}</p></div>', unsafe_allow_html=True)
            if st.button(f"Go to {key}", key=f"nav_{key}"):
                navigate_to(key)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Row 2
    row2 = st.columns(4)
    features2 = [("🏥 Healthcare", "Hospitals", "Healthcare"), 
                 ("🗳️ Jan Sewa", "Grievances", "Grievance"),
                 ("🎓 Education", "Degrees", "Education"), 
                 ("🚛 Transport", "DL & RC", "Transport")]
    
    for i, (icon, desc, key) in enumerate(features2):
        with row2[i]:
            st.markdown(f'<div class="feature-card"><h3>{icon}</h3><p>{desc}</p></div>', unsafe_allow_html=True)
            if st.button(f"Go to {key}", key=f"nav_{key}"):
                navigate_to(key)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Row 3
    row3 = st.columns(3)
    features3 = [("🗺️ GIS Map", "Map View", "GIS"), 
                ("📁 Locker", "Digital Docs", "Locker"), 
                ("⚠️ Disaster", "Alerts", "Disaster")]
    
    for i, (icon, desc, key) in enumerate(features3):
        with row3[i]:
            st.markdown(f'<div class="feature-card"><h3>{icon}</h3><p>{desc}</p></div>', unsafe_allow_html=True)
            if st.button(f"Go to {key}", key=f"nav_{key}"):
                navigate_to(key)

# --- BACK BUTTON (Common to all pages) ---
def show_back_button():
    st.markdown("---")
    col1, col2 = st.columns([1, 10])
    with col1:
        if st.button("⬅️ Back to Home"):
            go_home()

# --- SCHEMES PAGE ---
def show_schemes():
    st.title("💰 Government Schemes")
    show_back_button()
    
    income = st.number_input("Annual Income (₹)", 0, 5000000, 100000, 5000)
    age = st.number_input("Age", 18, 100, 30)
    
    if st.button("Find Eligible", type="primary"):
        for s in SCHEMES:
            with st.expander(s['name']):
                st.markdown(f"**Benefit:** {s['amount']}")
                st.markdown(f"**Category:** {s['category']}")
                if st.button("Apply Now", key=f"apply_{s['name']}"):
                    st.success("Application Submitted!")

# --- UTILITIES PAGE ---
def show_utilities():
    st.title("📄 Document Verification")
    show_back_button()
    
    tabs = st.tabs(["GSTIN", "PAN", "Aadhaar", "Voter ID"])
    
    with tabs[0]:
        st.subheader("Verify GST Registration")
        gstin = st.text_input("Enter GSTIN", placeholder="27AAAAA1234A1A1")
        if st.button("Verify GST"):
            if len(gstin) == 15:
                st.success("✅ Verified - Active")
            else:
                st.error("Invalid GSTIN")
    
    with tabs[1]:
        st.subheader("Verify PAN Card")
        pan = st.text_input("Enter PAN Number").upper()
        if st.button("Verify PAN"):
            st.success("✅ Valid PAN - Linked to Aadhaar")
    
    with tabs[2]:
        st.subheader("Verify Aadhaar")
        aadhar = st.text_input("Enter Aadhaar Number", max_length=12)
        if st.button("Verify Aadhaar"):
            st.success("✅ Aadhaar Validated Successfully")
    
    with tabs[3]:
        st.subheader("Voter ID Status")
        voter = st.text_input("Enter EPIC No").upper()
        if st.button("Check Voter"):
            st.success("✅ Voter ID Active - Mumbai North")

# --- JOBS PAGE ---
def show_jobs():
    st.title("💼 Sarkari Naukri Portal")
    show_back_button()
    
    col1, col2 = st.columns(2)
    qual = col1.selectbox("Qualification", ["10th", "12th", "Graduate", "Post Graduate"])
    dept = col2.selectbox("Department", ["UPSC", "SSC", "Railway", "Banking"])
    
    for job in GOVT_JOBS:
        with st.expander(f"📌 {job['post']}"):
            col1, col2 = st.columns(2)
            col1.markdown(f"**Qualification:** {job['qualification']}")
            col2.markdown(f"**Vacancies:** {job['vacancies']}")
            col1.markdown(f"**Last Date:** {job['last_date']}")
            if st.button(f"Apply: {job['post']}", key=f"job_{job['post']}"):
                st.success("Applied Successfully!")

# --- TAX PAGE ---
def show_tax():
    st.title("🧮 Income Tax Calculator")
    show_back_button()
    
    col1, col2 = st.columns(2)
    income = col1.number_input("Annual Income (₹)", 0, 100000000, 500000, 10000)
    age = col2.number_input("Age", 18, 100, 30)
    
    # Tax calculation logic
    deduction = 25000 if age < 60 else 50000 if age < 80 else 100000
    taxable = max(0, income - deduction)
    
    if taxable < 250000:
        tax = 0
    elif taxable < 500000:
        tax = (taxable - 250000) * 0.05
    elif taxable < 1000000:
        tax = 12500 + (taxable - 500000) * 0.20
    else:
        tax = 112500 + (taxable - 1000000) * 0.30
    
    if st.button("Calculate Tax", type="primary"):
        st.markdown("---")
        c1, c2, c3 = st.columns(3)
        c1.metric("Gross Income", f"₹{income:,}")
        c2.metric("Standard Deduction", f"₹{deduction:,}")
        c3.metric("Tax Payable", f"₹{int(tax):,}")
        
        st.info("💡 Tip: Invest in NPS/PPF under Section 80C to save tax!")

# --- HEALTHCARE PAGE ---
def show_healthcare():
    st.title("🏥 Healthcare Services")
    show_back_button()
    
    state = st.selectbox("Select State", STATES)
    pin = st.text_input("PIN Code")
    service = st.selectbox("Service Type", ["General", "ICU", "Cardiac", "Cancer"])
    
    if st.button("Search Hospitals"):
        st.success(f"Found 150+ hospitals in {state}")
    
    st.markdown("---")
    st.markdown("### Ayushman Bharat Claim")
    ack = st.text_input("Acknowledgement No")
    if st.button("Check Claim Status"):
        st.success("✅ Claim Sanctioned - ₹2,50,000")

# --- GRIEVANCE PAGE ---
def show_grievance():
    st.title("🗳️ Jan Sewa - File Grievance")
    show_back_button()
    
    col1, col2 = st.columns(2)
    name = col1.text_input("Full Name")
    mobile = col2.text_input("Mobile Number", max_length=10)
    
    category = st.selectbox("Category", ["Land & Revenue", "Police", "Tax & Revenue", "Medical", "Education"])
    desc = st.text_area("Complaint Description")
    
    if st.button("Submit Grievance", type="primary"):
        ref = f"JAN/2024/{random.randint(10000, 99999)}"
        st.success(f"✅ Grievance Submitted! Reference ID: {ref}")

# --- EDUCATION PAGE ---
def show_education():
    st.title("🎓 Education Services")
    show_back_button()
    
    tabs = st.tabs(["University Results", "Degree Verification", "Scholarships"])
    
    with tabs[0]:
        uni = st.selectbox("University", ["University of Delhi", "JNU", "BHU"])
        if st.button("Check Result"):
            st.success("✅ Result Declared")
    
    with tabs[1]:
        uni_name = st.text_input("University Name")
        roll = st.text_input("Roll Number")
        if st.button("Verify Degree"):
            st.success("✅ Degree Verified - Authentic")
    
    with tabs[2]:
        st.info("National Scholarship Portal - Applications Open!")
        if st.button("Apply for Scholarship"):
            st.success("Application Submitted!")

# --- TRANSPORT PAGE ---
def show_transport():
    st.title("🚛 Transport Services")
    show_back_button()
    
    tabs = st.tabs(["DL Status", "RC Status", "e-Challan"])
    
    with tabs[0]:
        st.subheader("Driving License Status")
        dl = st.text_input("License Number")
        dob = st.date_input("Date of Birth")
        if st.button("Check DL"):
            st.success("✅ License Valid - Non-Transport")
    
    with tabs[1]:
        st.subheader("Vehicle RC Status")
        reg = st.text_input("Registration Number")
        if st.button("Check RC"):
            st.success("✅ RC Valid - Tax Paid")
    
    with tabs[2]:
        st.subheader("Pay e-Challan")
        challan = st.text_input("Challan Number")
        if st.button("Pay Challan"):
            st.success("✅ Payment Successful")

# --- GIS PAGE ---
def show_gis():
    st.title("🗺️ GIS & Visualization")
    show_back_button()
    
    opt = st.selectbox("Select Data", ["State GDP Comparison", "Literacy Rate"])
    
    if opt == "State GDP Comparison":
        fig = px.bar(INDIA_GDP, x='State', y='GDP', title="State-wise GDP", color='GDP')
        st.plotly_chart(fig)
    else:
        fig = px.scatter(INDIA_GDP, x='State', y='Literacy', size='Literacy', color='State', title="Literacy Rate")
        st.plotly_chart(fig)
    
    st.markdown("### 🗺️ Interactive Map")
    map_df = pd.DataFrame({
        "City": ["Delhi", "Mumbai", "Bangalore", "Chennai", "Kolkata"],
        "Lat": [28.6, 19.0, 12.9, 13.0, 22.5],
        "Lon": [77.2, 72.8, 77.5, 80.2, 88.3]
    })
    st.map(map_df, latitude='Lat', longitude='Lon', zoom=3)

# --- LOCKER PAGE ---
def show_locker():
    st.title("📁 Digital Locker")
    show_back_button()
    
    col1, col2 = st.columns(2)
    col1.info("📄 Aadhaar Card - Synced")
    col2.info("📄 PAN Card - Synced")
    
    st.markdown("### Upload New Document")
    uploaded = st.file_uploader("Choose PDF file", type=['pdf'])
    if uploaded:
        st.success("File Uploaded Successfully!")

# --- DISASTER PAGE ---
def show_disaster():
    st.title("⚠️ Disaster & Weather Alert")
    show_back_button()
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 🌧️ Monsoon Status")
        st.progress(75)
        st.success("Monsoon Active in: Maharashtra, Gujarat, Goa")
        st.warning("Heavy rainfall expected in Konkan region")
    
    with col2:
        st.markdown("### 🔥 Heatwave Alert")
        st.progress(10)
        st.success("No Heatwave Alert")

# --- MAIN APP ROUTER ---
def main():
    if current_page == "Home":
        show_home()
    elif current_page == "Schemes":
        show_schemes()
    elif current_page == "Utilities":
        show_utilities()
    elif current_page == "Jobs":
        show_jobs()
    elif current_page == "Tax":
        show_tax()
    elif current_page == "Healthcare":
        show_healthcare()
    elif current_page == "Grievance":
        show_grievance()
    elif current_page == "Education":
        show_education()
    elif current_page == "Transport":
        show_transport()
    elif current_page == "GIS":
        show_gis()
    elif current_page == "Locker":
        show_locker()
    elif current_page == "Disaster":
        show_disaster()

if __name__ == "__main__":
    main()
