import streamlit as st
from supabase import create_client
from grammar_parser import parse_order, extract_order
from dotenv import load_dotenv
import os

# Load Supabase credentials
load_dotenv()
SUPABASE_URL = os.getenv("SUPABASE_URL", "")
SUPABASE_KEY = os.getenv("SUPABASE_KEY", "")

# Initialize Supabase client with error handling
supabase = None
if SUPABASE_URL and SUPABASE_KEY:
    try:
        supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
    except Exception as e:
        print(f"Supabase connection error: {e}")

# Page config
st.set_page_config(
    page_title="Coffee Order Parser",
    page_icon="☕",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for modern dashboard aesthetic
st.markdown("""
<style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    /* Global Styles */
    * {
        font-family: 'Inter', sans-serif;
    }
    
    /* Main container */
    .main {
        background: linear-gradient(135deg, #f5f7fa 0%, #e8ecf1 100%);
        padding: 2rem;
    }
    
    /* Sidebar styling */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1a1d29 0%, #2d3142 100%);
    }
    
    [data-testid="stSidebar"] > div:first-child {
        background: transparent;
    }
    
    /* Sidebar text */
    [data-testid="stSidebar"] p, [data-testid="stSidebar"] label {
        color: #e0e0e0 !important;
    }
    
    /* Header styling */
    .header-container {
        background: white;
        padding: 2rem;
        border-radius: 20px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.07);
        margin-bottom: 2rem;
    }
    
    .greeting {
        font-size: 2rem;
        font-weight: 700;
        color: #1a1d29;
        margin-bottom: 0.5rem;
    }
    
    .subtext {
        color: #6b7280;
        font-size: 0.95rem;
        line-height: 1.6;
    }
    
    /* Card styling */
    .info-card {
        background: linear-gradient(135deg, #fef3c7 0%, #fde68a 100%);
        padding: 1.5rem;
        border-radius: 16px;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
        margin-bottom: 1.5rem;
        border: 1px solid rgba(251, 191, 36, 0.2);
    }
    
    .info-card.pink {
        background: linear-gradient(135deg, #fce7f3 0%, #fbcfe8 100%);
        border: 1px solid rgba(236, 72, 153, 0.2);
    }
    
    .info-card.green {
        background: linear-gradient(135deg, #d9f99d 0%, #bef264 100%);
        border: 1px solid rgba(132, 204, 22, 0.2);
    }
    
    .info-card.blue {
        background: linear-gradient(135deg, #dbeafe 0%, #bfdbfe 100%);
        border: 1px solid rgba(59, 130, 246, 0.2);
    }
    
    .card-title {
        font-size: 1.1rem;
        font-weight: 600;
        margin-bottom: 0.8rem;
        color: #1a1d29;
    }
    
    .card-content {
        color: #374151;
        font-size: 0.9rem;
        line-height: 1.8;
    }
    
    /* Input styling */
    .stTextInput > div > div > input {
        border-radius: 12px;
        border: 2px solid #e5e7eb;
        padding: 0.75rem 1rem;
        font-size: 1rem;
        transition: all 0.3s ease;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #6366f1;
        box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.1);
    }
    
    /* Button styling */
    .stButton > button {
        background: linear-gradient(135deg, #1a1d29 0%, #2d3142 100%);
        color: white;
        border-radius: 12px;
        padding: 0.75rem 2rem;
        font-weight: 600;
        border: none;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        transition: all 0.3s ease;
        width: 100%;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 12px rgba(0, 0, 0, 0.15);
    }
    
    /* Order card styling */
    .order-card {
        background: white;
        padding: 1.5rem;
        border-radius: 16px;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
        margin-bottom: 1rem;
        border-left: 4px solid #6366f1;
    }
    
    .order-item {
        display: flex;
        justify-content: space-between;
        margin-bottom: 0.5rem;
    }
    
    .order-label {
        font-weight: 600;
        color: #6b7280;
        font-size: 0.85rem;
    }
    
    .order-value {
        color: #1a1d29;
        font-weight: 500;
    }
    
    /* Success/Error messages */
    .stSuccess, .stError, .stWarning, .stInfo {
        border-radius: 12px;
        padding: 1rem;
    }
    
    /* Sidebar branding */
    .sidebar-logo {
        text-align: center;
        padding: 2rem 1rem;
        border-bottom: 1px solid rgba(255, 255, 255, 0.1);
        margin-bottom: 2rem;
    }
    
    .logo-text {
        font-size: 1.2rem;
        font-weight: 700;
        color: white;
        letter-spacing: -0.5px;
        line-height: 1.4;
    }
    
    .logo-subtext {
        font-size: 0.75rem;
        color: #9ca3af;
        margin-top: 0.25rem;
    }
    
    /* Section headers */
    .section-header {
        font-size: 1.3rem;
        font-weight: 700;
        color: #2d3142;
        margin-bottom: 1rem;
        margin-top: 2rem;
        background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    /* Dataframe styling */
    .dataframe {
        border-radius: 12px;
        overflow: hidden;
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Spacing utilities */
    .spacer {
        margin-bottom: 2rem;
    }
</style>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.markdown("""
    <div class="sidebar-logo">
        <div class="logo-text">Automata Theory and Formal Languages</div>
        <div class="logo-subtext">Coffee Order System</div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("### 📚 About")
    st.markdown("""
    <div style="color: #9ca3af; font-size: 0.85rem; line-height: 1.6;">
    A natural language coffee order parser using grammar validation and Supabase storage.
    </div>
    """, unsafe_allow_html=True)

    st.markdown("### 👥 Team Members")
    st.markdown("""
    <div style="color: #9ca3af; font-size: 0.85rem; line-height: 1.6;">
    • Rafael Bisnar<br>
    • Paul Edwin Guevarra Iglesia<br>
    • Jon Lemmual Ruta<br>
    • Yrvin John Tabucol<br>
    • Ma. Jarhen Louise P. Valencia
    </div>
    """, unsafe_allow_html=True)


# Main content
st.markdown("""
<div class="header-container">
    <div class="greeting">Good morning, Coffee Lover ☕</div>
    <div class="subtext">Welcome to your intelligent coffee ordering system. Place your orders naturally and let our parser handle the rest!</div>
</div>
""", unsafe_allow_html=True)

# Info cards row
col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    <div class="info-card">
        <div class="card-title">☕ Available Drinks</div>
        <div class="card-content">
            <strong>Coffee</strong> • <strong>Latte</strong> • <strong>Espresso</strong><br>
            <strong>Cappuccino</strong> • <strong>Americano</strong>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="info-card green">
        <div class="card-title">✨ Examples</div>
        <div class="card-content">
            • "Order 2 latte with sugar"<br>
            • "I want a coffee"<br>
            • "Make an espresso please"<br>
            • "Get 3 cappuccino with cream"
        </div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="info-card pink">
        <div class="card-title">🎨 Modifiers & Sizes</div>
        <div class="card-content">
            <strong>Modifiers:</strong> Sugar, Milk, Cream, Syrup, Ice, Ice Cream<br>
            <strong>Sizes:</strong> Small, Medium, Large
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="info-card blue">
        <div class="card-title">📝 How It Works</div>
        <div class="card-content">
            Type your order naturally, click "Save Order", and watch the magic happen! Orders are validated and saved automatically.
        </div>
    </div>
    """, unsafe_allow_html=True)

st.markdown('<div class="spacer"></div>', unsafe_allow_html=True)

# Order input section
st.markdown('<div class="section-header">📋 Place Your Order</div>', unsafe_allow_html=True)

with st.form(key='order_form'):
    col_input, col_button = st.columns([3, 1])
    with col_input:
        user_input = st.text_input(
            "What would you like to order?",
            placeholder="e.g., 'Order 2 latte with sugar'",
            label_visibility="collapsed"
        )
    with col_button:
        parse_button = st.form_submit_button("Save Order", use_container_width=True)

    if parse_button:
        if user_input.strip():
            valid = parse_order(user_input)
            if valid:
                st.success("✅ Grammar accepted! Order validated successfully.")
                order_data = extract_order(user_input)
                
                # Display parsed order in a beautiful card
                st.markdown(f"""
                <div class="order-card">
                    <div class="card-title">📦 Parsed Order Details</div>
                    <div class="order-item">
                        <span class="order-label">QUANTITY:</span>
                        <span class="order-value">{order_data['quantity']}</span>
                    </div>
                    <div class="order-item">
                        <span class="order-label">DRINK:</span>
                        <span class="order-value">{order_data['drink']}</span>
                    </div>
                    <div class="order-item">
                        <span class="order-label">SIZE:</span>
                        <span class="order-value">{order_data['size'] if order_data['size'] else 'Not specified'}</span>
                    </div>
                    <div class="order-item">
                        <span class="order-label">MODIFIERS:</span>
                        <span class="order-value">{order_data['modifiers']}</span>
                    </div>
                </div>
                """, unsafe_allow_html=True)

                # Save to Supabase
                if supabase:
                    try:
                        data, _ = supabase.table("Orders").insert(order_data).execute()
                        st.info("💾 Order saved to database successfully!")
                    except Exception as e:
                        st.error(f"❌ Database error: {str(e)}")
                else:
                    st.warning("⚠️ Database not connected. Please check your Supabase credentials.")
            else:
                st.error("❌ Invalid grammar. Please use a proper structure (e.g., 'Order 2 latte with sugar')")
        else:
            st.warning("⚠️ Please enter an order first.")

# View all orders section
st.markdown('<div class="section-header">📊 All Orders</div>', unsafe_allow_html=True)

load_button = st.button("🔄 Load All Orders", use_container_width=True)

if load_button:
    if supabase:
        try:
            data = supabase.table("Orders").select("*").execute()
            if data.data:
                st.dataframe(data.data)
            else:
                st.write("No orders found.")
        except Exception as e:
            st.error(f"❌ Error loading orders: {str(e)}")
    else:
        st.warning("⚠️ Database not connected. Please check your Supabase credentials.")

st.markdown('<div class="spacer"></div>', unsafe_allow_html=True)
