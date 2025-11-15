import streamlit as st
st.set_page_config(
    page_title="Olympics Dashboard",
    page_icon="🏅",
    layout="centered",
    initial_sidebar_state="collapsed"
)

st.markdown("""
    <style>
    [data-testid="stSidebar"], [data-testid="stHeader"], [data-testid="stToolbar"] {
        display: none;
    }
    
    .main {
        background-color: #f4f6f8;
        font-family: 'Poppins', sans-serif;
    }
    div[data-testid="stAppViewContainer"] h1 {
        text-align: center;
        color: #27B4F5 !important;
        font-size: 2.6rem !important;
        font-weight: 700;
        margin-bottom: 0.4rem;
    }

    h2 {
        text-align: center;
        color: #457b9d;
        font-size: 1.1rem;
        margin-bottom: 2.5rem;
    }

    [data-testid="stPageLink"] a {
        display: block; 
        text-align: center; 
        background-color: white !important;
        color: #1d3557 !important;
        border: 2px solid #27B4F5 !important; 
        border-radius: 12px !important;
        font-weight: 600 !important;
        font-size: 1rem !important;
        padding: 0.9rem 1rem !important;
        transition: all 0.25s ease-in-out;
        box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.1);
        text-decoration: none !important;
    }

    [data-testid="stPageLink"] a:hover {
        background-color: #27B4F5 !important;   
        color: white !important;
        transform: translateY(-3px);
        box-shadow: 0px 6px 18px rgba(39, 180, 245, 0.4);
        text-decoration: none !important;
    }

    footer {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

st.markdown("<h1>🏅 Olympics Data Analysis</h1>", unsafe_allow_html=True)
st.markdown("<h2>Explore Historical Insights & Predict Athlete Performance</h2>", unsafe_allow_html=True)

col1, col2, col3 = st.columns(3, gap="large")

with col1:
    st.page_link("pages/summer.py", label="☀️ Summer Olympics", use_container_width=True)

with col2:
    st.page_link("pages/winter.py", label="❄️ Winter Olympics", use_container_width=True)

with col3:
    st.page_link("pages/performance_model.py", label="🤖 Performance Model", use_container_width=True)