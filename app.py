import streamlit as st
import pandas as pd
import plotly.express as px
import random

# --- PAGE CONFIG ---
st.set_page_config(
    page_title="India e-Governance Portal",
    page_icon="🇮🇳",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- CSS STYLES ---
st.markdown("""
    <style>
    .main-header {
        background: linear-gradient(90deg, #FF9933 0%, #FFFFFF 50%, #138808 100%);
        padding: 20px;
        border-radius: 10px;
        text-align: center;
        margin-bottom: 20px;
    }
    .title-text {
        font-size: 40px;
        font-weight: bold;
        color: #1a1a1a;
    }
    .feature-card {
        background-color: white;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        height: 100%;
    }
    .success-box {
        padding: 15px;
        background-color: #d4edda;
        color: #155724;
        border-radius: 5px;
        border-left: 5px solid #28a745;
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
UNIVERSITIES = [
    {"name": "University of Delhi", "result_status": "Declared"},
    {"name": "JNU", "result_status": "Pending"},
]
INDIA_GDP = pd.DataFrame({
    "State": STATES,
    "GDP": [380000, 280000, 240000, 230000, 200000],
    "Literacy": [84.8, 80.1, 75.4, 78.0, 69.7]
})

# --- SESSION STATE ---
if 'active_tab' not in st.session_state:
    st.session_state['active_tab'] = 'Home'

# --- NAVIGATION FUNCTION ---
def nav_to(tab_name):
    st.session_state['active_tab'] = tab_name
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
    
    row1 = st.columns(4)
    features = [("💰 Schemes", "Find Benefits", "Schemes"), ("📄 Documents", "Verify GST/PAN", "Utilities"), 
                ("💼 Jobs", "Sarkari Naukri", "Jobs"), ("🧮 Tax", "Tax Calculator", "Tax")]
    
    for i, (icon, desc, key) in enumerate(features):
        with row1[i]:
            st.markdown(f'<div class="feature-card"><h3>{icon}</h3><p>{desc}</p></div>', unsafe_allow_html=True)
            if st.button(f"Go", key=f"nav_{key}"): nav_to(key)
    
    row2 = st.columns(4)
    features2 = [("🏥 Healthcare", "Hospitals", "Healthcare"), ("🗳️ Jan Sewa", "Grievances", "Grievance"),
                 ("🎓 Education", "Degrees", "Education"), ("🚛 Transport", "DL & RC", "Transport")]
    
    for i, (icon, desc, key) in enumerate(features2):
        with row2[i]:
            st.markdown(f'<div class="feature-card"><h3>{icon}</h3><p>{desc}</p></div>', unsafe_allow_html=True)
            if st.button(f"Go", key=f"nav_{key}"): nav_to(key)
    
    row3 = st.columns(3)
    features3 = [("🗺️ GIS Map", "Map View", "GIS"), ("📁 Locker", "Digital Docs", "Locker"), 
                ("⚠️ Disaster", "Alerts", "Disaster")]
    
    for i, (icon, desc, key) in enumerate(features3):
        with row3[i]:
            st.markdown(f'<div class="feature-card"><h3>{icon}</h3><p>{desc}</p></div>', unsafe_allow_html=True)
            if st.button(f"Go", key=f"nav_{key}"): nav_to(key)

# --- SCHEMES ---
def show_schemes():
    st.title("💰 Government Schemes")
    income = st.number_input("Annual Income (₹)", 0, 5000000, 100000, 5000)
    age = st.number_input("Age", 18, 100, 30)
    
    if st.button("Find Eligible", type="primary"):
        for s in SCHEMES:
            with st.expander(s['name']):
                st.markdown(f"**Benefit:** {s['amount']}")
                if st.button("Apply", key=f"apply_{s['name']}"): st.success("Applied!")

# --- UTILITIES ---
def show_utilities():
    st.title("📄 Document Verification")
    tabs = st.tabs(["GSTIN", "PAN", "Aadhaar", "Voter ID"])
    
    with tabs[0]:
        gstin = st.text_input("GSTIN")
        if st.button("Verify GST"): st.success("✅ Verified - Active")
    
    with tabs[1]:
        pan = st.text_input("PAN").upper()
        if st.button("Verify PAN"): st.success("✅ Valid")
    
    with tabs[2]:
        aadhar = st.text_input("Aadhaar", max_length=12)
        if st.button("Verify Aadhaar"): st.success("✅ Valid")
    
    with tabs[3]:
        voter = st.text_input("EPIC No").upper()
        if st.button("Check Voter"): st.success("✅ Active")

# --- JOBS ---
def show_jobs():
    st.title("💼 Sarkari Naukri")
    for job in GOVT_JOBS:
        with st.expander(job['post']):
            st.markdown(f"**Qualification:** {job['qualification']}")
            st.markdown(f"**Vacancies:** {job['vacancies']}")
            if st.button("Apply", key=f"job_{job['post']}"): st.success("Applied!")

# --- TAX ---
def show_tax():
    st.title("🧮 Income Tax Calculator")
    income = st.number_input("Income (₹)", 0, 100000000, 500000, 10000)
    age = st.number_input("Age", 18, 100, 30)
    
    deduction = 25000 if age < 60 else 50000
    taxable = max(0, income - deduction)
    
    if taxable < 250000: tax = 0
    elif taxable < 500000: tax = (taxable - 250000) * 0.05
    elif taxable < 1000000: tax = 12500 + (taxable - 500000) * 0.20
    else: tax = 112500 + (taxable - 1000000) * 0.30
    
    if st.button("Calculate"):
        c1, c2, c3 = st.columns(3)
        c1.metric("Income", f"₹{income:,}")
        c2.metric("Deduction", f"₹{deduction:,}")
        c3.metric("Tax", f"₹{int(tax):,}")

# --- HEALTHCARE ---
def show_healthcare():
    st.title("🏥 Healthcare")
    state = st.selectbox("State", STATES)
    if st.button("Find Hospital"): st.success(f"Found 100+ hospitals")
    st.markdown("### Ayushman Claim")
    ack = st.text_input("Ack No")
    if st.button("Check"): st.success("✅ Sanctioned ₹2.5L")

# --- GRIEVANCE ---
def show_grievance():
    st.title("🗳️ Jan Sewa")
    name = st.text_input("Name")
    mobile = st.text_input("Mobile", max_length=10)
    desc = st.text_area("Complaint")
    if st.button("Submit"):
        st.success(f"✅ Submitted - Ref: JAN/{random.randint(10000,99999)}")

# --- EDUCATION ---
def show_education():
    st.title("🎓 Education")
    tabs = st.tabs(["Results", "Verify Degree", "Scholarships"])
    
    with tabs[0]:
        uni = st.selectbox("University", [u['name'] for u in UNIVERSITIES])
        if st.button("Check"): st.success("Status: Declared")
    
    with tabs[1]:
        if st.button("Verify"): st.success("✅ Authentic")
    
    with tabs[2]:
        st.info("Scholarship applications open!")
        if st.button("Apply"): st.success("Applied!")

# --- TRANSPORT ---
def show_transport():
    st.title("🚛 Transport")
    tabs = st.tabs(["DL", "RC", "e-Challan"])
    
    with tabs[0]:
        dl = st.text_input("License No")
        if st.button("Check DL"): st.success("✅ Valid")
    
    with tabs[1]:
        rc = st.text_input("Vehicle No")
        if st.button("Check RC"): st.success("✅ Valid")
    
    with tabs[2]:
        if st.button("Pay"): st.success("✅ Paid")

# --- GIS ---
def show_gis():
    st.title("🗺️ GIS Map")
    opt = st.selectbox("Data", ["GDP", "Literacy"])
    
    if opt == "GDP":
        fig = px.bar(INDIA_GDP, x='State', y='GDP', color='GDP')
        st.plotly_chart(fig)
    else:
        fig = px.scatter(INDIA_GDP, x='State', y='Literacy', size='Literacy', color='State')
        st.plotly_chart(fig)
    
    map_df = pd.DataFrame({"City": STATES, "Lat": [19, 28.6, 12.9, 13.0, 22.5], 
                          "Lon": [72.8, 77.2, 77.5, 80.2, 88.3]})
    st.map(map_df, latitude='Lat', longitude='Lon', zoom=3)

# --- LOCKER ---
def show_locker():
    st.title("📁 Digital Locker")
    c1, c2 = st.columns(2)
    c1.info("📄 Aadhaar - Synced")
    c2.info("📄 PAN - Synced")
    
    st.markdown("### Upload")
    uploaded = st.file_uploader("Choose PDF", type=['pdf'])
    if uploaded: st.success("Uploaded!")

# --- DISASTER ---
def show_disaster():
    st.title("⚠️ Disaster Alert")
    c1, c2 = st.columns(2)
    c1.markdown("### 🌧️ Monsoon")
    c1.progress(75)
    c1.success("Active in Konkan")
    
    c2.markdown("### 🔥 Heatwave")
    c2.progress(10)
    c2.success("No Alert")

# --- MAIN APP ---
def main():
    tab = st.session_state['active_tab']
    
    if tab == 'Home': show_home()
    elif tab == 'Schemes': show_schemes()
    elif tab == 'Utilities': show_utilities()
    elif tab == 'Jobs': show_jobs()
    elif tab == 'Tax': show_tax()
    elif tab == 'Healthcare': show_healthcare()
    elif tab == 'Grievance': show_grievance()
    elif tab == 'Education': show_education()
    elif tab == 'Transport': show_transport()
    elif tab == 'GIS': show_gis()
    elif tab == 'Locker': show_locker()
    elif tab == 'Disaster': show_disaster()

if __name__ == "__main__":
    main()
