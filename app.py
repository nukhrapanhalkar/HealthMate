import streamlit as st
import pandas as pd
from datetime import datetime
import time
import random
import os

# ============ PAGE CONFIGURATION ============
st.set_page_config(
    page_title="HealthMate - Your Health Assistant",
    page_icon="🩺",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============ CUSTOM CSS ============
def load_custom_css():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
    
    @keyframes pulse {
        0% { transform: scale(1); opacity: 1; }
        50% { transform: scale(1.05); opacity: 0.8; }
        100% { transform: scale(1); opacity: 1; }
    }
    
    @keyframes glow {
        0% { box-shadow: 0 0 5px rgba(45, 212, 191, 0.3); }
        50% { box-shadow: 0 0 20px rgba(45, 212, 191, 0.6); }
        100% { box-shadow: 0 0 5px rgba(45, 212, 191, 0.3); }
    }
    
    .stApp {
        background: linear-gradient(135deg, #0a0e1a 0%, #0f172a 100%);
    }
    
    .user-message {
        background: linear-gradient(135deg, #2dd4bf 0%, #14b8a6 100%);
        padding: 12px 18px;
        border-radius: 20px;
        margin: 8px 0;
        max-width: 80%;
        float: right;
        clear: both;
        color: white;
        font-weight: 500;
        box-shadow: 0 2px 8px rgba(0,0,0,0.2);
    }
    
    .bot-message {
        background: #1e293b;
        padding: 12px 18px;
        border-radius: 20px;
        margin: 8px 0;
        max-width: 80%;
        float: left;
        clear: both;
        border-left: 4px solid #2dd4bf;
        color: #e2e8f0;
        box-shadow: 0 2px 8px rgba(0,0,0,0.2);
    }
    
    .stButton > button {
        background: linear-gradient(135deg, #2dd4bf 0%, #14b8a6 100%);
        color: white;
        border: none;
        padding: 8px 16px;
        border-radius: 12px;
        font-weight: 600;
        transition: all 0.3s;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 15px rgba(45, 212, 191, 0.3);
    }
    
    .welcome-banner {
        background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
        padding: 30px;
        border-radius: 20px;
        text-align: center;
        color: white;
        margin-bottom: 20px;
        border: 1px solid #2dd4bf;
        animation: glow 3s infinite;
    }
    
    .footer {
        text-align: center;
        padding: 20px;
        color: #94a3b8;
        font-size: 12px;
        margin-top: 30px;
        border-top: 1px solid #1e293b;
    }
    
    .clearfix::after {
        content: "";
        clear: both;
        display: table;
    }
    
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0f172a 0%, #0a0e1a 100%);
        border-right: 1px solid #2dd4bf20;
    }
    
    [data-testid="stSidebar"] * {
        color: #e2e8f0;
    }
    
    .stTextInput > div > div > input {
        background: #1e293b;
        border: 1px solid #334155;
        color: white;
        border-radius: 12px;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #2dd4bf;
        box-shadow: 0 0 0 2px rgba(45, 212, 191, 0.2);
    }
    </style>
    """, unsafe_allow_html=True)

# ============ LOAD CSV FILES FROM DATA FOLDER ============
@st.cache_data
def load_csv_files():
    """Load all CSV files from data folder"""
    data_folder = "data"
    
    # Check if data folder exists
    if not os.path.exists(data_folder):
        st.error(f"❌ The '{data_folder}' folder does not exist!")
        st.info(f"Please create a '{data_folder}' folder and put your CSV files there.")
        return None, None, None, None
    
    # Load diseases.csv
    try:
        diseases_path = os.path.join(data_folder, "diseases.csv")
        diseases_df = pd.read_csv(diseases_path)
    except Exception as e:
        st.error(f"❌ Error loading diseases.csv: {e}")
        return None, None, None, None
    
    # Load questions.csv
    try:
        questions_path = os.path.join(data_folder, "questions.csv")
        questions_df = pd.read_csv(questions_path)
    except Exception as e:
        st.error(f"❌ Error loading questions.csv: {e}")
        return None, None, None, None
    
    # Load medicines.csv
    try:
        medicines_path = os.path.join(data_folder, "medicines.csv")
        medicines_df = pd.read_csv(medicines_path)
    except Exception as e:
        st.error(f"❌ Error loading medicines.csv: {e}")
        return None, None, None, None
    
    # Load precautions.csv
    try:
        precautions_path = os.path.join(data_folder, "precautions.csv")
        precautions_df = pd.read_csv(precautions_path)
    except Exception as e:
        st.error(f"❌ Error loading precautions.csv: {e}")
        return None, None, None, None
    
    return diseases_df, questions_df, medicines_df, precautions_df

# ============ HELPER FUNCTIONS ============
def find_disease(text, diseases_df):
    """Find which disease the user mentioned"""
    if diseases_df is None:
        return None
    text_lower = text.lower()
    for disease in diseases_df['disease']:
        if disease.lower() in text_lower:
            return disease
    return None

def get_questions(disease, questions_df):
    """Get questions for a specific disease from questions.csv"""
    if questions_df is None:
        return None
    q_data = questions_df[questions_df['disease'] == disease]
    if not q_data.empty:
        questions = []
        if pd.notna(q_data.iloc[0]['question1']):
            questions.append(q_data.iloc[0]['question1'])
        if pd.notna(q_data.iloc[0]['question2']):
            questions.append(q_data.iloc[0]['question2'])
        if pd.notna(q_data.iloc[0]['question3']):
            questions.append(q_data.iloc[0]['question3'])
        return questions
    return None

def get_medicines(disease, medicines_df):
    """Get medicines for a specific disease from medicines.csv"""
    if medicines_df is None:
        return None
    med_data = medicines_df[medicines_df['disease'] == disease]
    if not med_data.empty:
        medicines = []
        if pd.notna(med_data.iloc[0]['medicine1']):
            medicines.append(med_data.iloc[0]['medicine1'])
        if pd.notna(med_data.iloc[0]['medicine2']):
            medicines.append(med_data.iloc[0]['medicine2'])
        if pd.notna(med_data.iloc[0]['medicine3']):
            medicines.append(med_data.iloc[0]['medicine3'])
        return medicines
    return None

def get_precautions(disease, precautions_df):
    """Get precautions for a specific disease from precautions.csv"""
    if precautions_df is None:
        return None
    prec_data = precautions_df[precautions_df['disease'] == disease]
    if not prec_data.empty:
        precautions = []
        if pd.notna(prec_data.iloc[0]['precaution1']):
            precautions.append(prec_data.iloc[0]['precaution1'])
        if pd.notna(prec_data.iloc[0]['precaution2']):
            precautions.append(prec_data.iloc[0]['precaution2'])
        if pd.notna(prec_data.iloc[0]['precaution3']):
            precautions.append(prec_data.iloc[0]['precaution3'])
        return precautions
    return None

def get_disease_info(disease, diseases_df):
    """Get basic disease info from diseases.csv"""
    if diseases_df is None:
        return None
    info = diseases_df[diseases_df['disease'] == disease]
    if not info.empty:
        return info.iloc[0]
    return None

def format_final_advice(disease, answers, diseases_df, medicines_df, precautions_df):
    """Format final advice with medicines and precautions"""
    info = get_disease_info(disease, diseases_df)
    medicines = get_medicines(disease, medicines_df)
    precautions = get_precautions(disease, precautions_df)
    
    text = f"🔍 **DIAGNOSIS: {disease.upper()}**\n\n"
    text += "━" * 50 + "\n\n"
    
    # Severity warning
    if info is not None:
        severity = info['severity']
        if severity == 'Severe':
            text += "⚠️ **SEVERITY: SEVERE - SEEK MEDICAL HELP IMMEDIATELY!** ⚠️\n\n"
        elif severity == 'Moderate':
            text += "📊 **Severity:** Moderate - Monitor closely\n\n"
        else:
            text += "✅ **Severity:** Mild - Self-care recommended\n\n"
    
    # Precautions section
    if precautions:
        text += "🛡️ **Precautions:**\n"
        for prec in precautions:
            text += f"   • {prec}\n"
        text += "\n"
    
    # Medicines section
    if medicines:
        text += "💊 **Suggested Medicines:**\n"
        for med in medicines:
            text += f"   • {med}\n"
        text += "\n"
    
    # Additional advice from CSV
    if info is not None:
        text += f"✅ **What to do:**\n{info['what_to_do']}\n\n"
        text += f"👨‍⚕️ **When to see a doctor:**\n{info['see_doctor']}\n\n"
    
    # Emergency warning
    if info is not None and info['emergency'] == 'Yes':
        text += "🚨 **⚠️ THIS IS A MEDICAL EMERGENCY - SEEK HELP NOW!** ⚠️ 🚨\n\n"
    
    text += "━" * 50 + "\n\n"
    text += "💙 *Remember: This is for educational purposes only. Always consult a healthcare professional.*\n\n"
    text += "✨ **Need help with anything else?** Just tell me your symptoms!"
    
    return text

def get_greeting(text):
    """Handle greetings"""
    text_lower = text.lower()
    greetings = ['hello', 'hi', 'hey', 'good morning', 'good afternoon', 'greetings', 'howdy']
    
    if any(g in text_lower for g in greetings):
        return "Hello! 👋 I'm **HealthMate**, your smart health assistant. Tell me what symptoms you're experiencing."
    
    if 'thank' in text_lower:
        return "You're welcome! 💙 Take care and feel better soon!"
    
    if text_lower in ['bye', 'goodbye', 'exit', 'quit', 'see you']:
        return "Goodbye! 🌟 Stay healthy and take care!"
    
    return None

# ============ LOGIN PAGE ============
def login_page():
    """Display login page with form on right, brand on left, dark theme"""
    st.markdown("""
    <style>
        [data-testid="stSidebar"] {
            display: none;
        }
        [data-testid="stSidebarCollapsedControl"] {
            display: none;
        }
        .main > div {
            padding: 0rem 1rem;
        }
        .stApp {
            background: linear-gradient(135deg, #0a0e1a 0%, #0f172a 100%);
        }
        div[data-testid="stForm"] {
            background: transparent;
        }
        .stTextInput label {
            color: #94a3b8 !important;
        }
    </style>
    """, unsafe_allow_html=True)
    
    load_custom_css()
    
    col_left, col_right = st.columns([1, 1], gap="large")
    
    with col_left:
        st.markdown("""
        <div style="background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%); border-radius: 28px; padding: 32px 28px; color: white; position: relative; overflow: hidden; border: 1px solid #2dd4bf30;">
            <div style="position: relative; z-index: 2;">
                <div style="font-size: 48px; margin-bottom: 16px;">🩺</div>
                <div style="font-size: 42px; font-weight: 800; background: linear-gradient(135deg, #2dd4bf, #14b8a6); -webkit-background-clip: text; background-clip: text; color: transparent; margin-bottom: 12px;">
                    HealthMate
                </div>
                <div style="font-size: 20px; font-weight: 500; color: #2dd4bf; border-left: 4px solid #2dd4bf; padding-left: 16px; margin-bottom: 24px;">
                    your personal AI health assistant
                </div>
                <div style="font-size: 15px; line-height: 1.55; color: #cbd5e1; margin-bottom: 28px;">
                    Your 24/7 intelligent companion for symptom insights, wellness tips, and proactive care. Let's build healthier habits together.
                </div>
                <ul style="list-style: none; padding-left: 0;">
                    <li style="margin-bottom: 12px; display: flex; align-items: center; gap: 14px; font-size: 15px; color: #94a3b8;">
                        <span style="width: 28px; font-size: 20px;">💬</span> AI-powered symptom checker
                    </li>
                    <li style="margin-bottom: 12px; display: flex; align-items: center; gap: 14px; font-size: 15px; color: #94a3b8;">
                        <span style="width: 28px; font-size: 20px;">📊</span> Health tracking & insights
                    </li>
                    <li style="margin-bottom: 12px; display: flex; align-items: center; gap: 14px; font-size: 15px; color: #94a3b8;">
                        <span style="width: 28px; font-size: 20px;">🚨</span> Emergency guidance
                    </li>
                    <li style="margin-bottom: 0; display: flex; align-items: center; gap: 14px; font-size: 15px; color: #94a3b8;">
                        <span style="width: 28px; font-size: 20px;">💊</span> Medicine information
                    </li>
                </ul>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col_right:
        st.markdown("""
        <div style="background: #1e293b; border-radius: 30px; padding: 32px 28px; box-shadow: 0 20px 40px rgba(0,0,0,0.3); height: 100%; border: 1px solid #334155; display: flex; flex-direction: column;">
            <div>
                <h2 style="font-size: 28px; font-weight: 700; color: #f1f5f9; margin-bottom: 4px;">Welcome back</h2>
                <p style="color: #94a3b8; margin-bottom: 20px; font-size: 14px;">Sign in to continue your health journey</p>
            </div>
        """, unsafe_allow_html=True)
        
        with st.form("login_form", clear_on_submit=False):
            username = st.text_input(
                "👤 Username", 
                placeholder="Enter any username", 
                key="login_username"
            )
            password = st.text_input(
                "🔑 Password", 
                type="password", 
                placeholder="Enter any password", 
                key="login_password"
            )
            
            col_btn1, col_btn2 = st.columns(2)
            with col_btn1:
                submit = st.form_submit_button("🔓 Login", use_container_width=True)
            with col_btn2:
                guest = st.form_submit_button("👋 Guest Mode", use_container_width=True)
            
            if submit:
                if username and password:
                    st.session_state.logged_in = True
                    st.session_state.username = username
                    st.session_state.user_name = username.title()
                    st.session_state.show_welcome = True
                    st.rerun()
                else:
                    st.error("❌ Please enter both username and password!")
            
            if guest:
                st.session_state.logged_in = True
                st.session_state.username = "guest"
                st.session_state.user_name = "Guest"
                st.session_state.show_welcome = True
                st.rerun()
        
        st.markdown("""
            <div style="margin-top: auto;">
                <div style="padding-top: 16px; border-top: 1px solid #334155;">
                    <p style="font-size: 13px; color: #94a3b8; margin: 6px 0;"><strong style="color: #2dd4bf;">✨ Features:</strong></p>
                    <p style="font-size: 12px; color: #94a3b8; margin: 6px 0;">🩺 Symptom checker • 💊 Medicine guide</p>
                    <p style="font-size: 12px; color: #94a3b8; margin: 6px 0;">🛡️ Precautions • 🚨 Emergency alerts</p>
                    <p style="font-size: 12px; color: #94a3b8; margin: 6px 0;">💬 24/7 AI support • 📋 Health tips</p>
                </div>
                <div style="margin-top: 16px;">
                    <p style="font-size: 10px; text-align: center; color: #64748b;">⚠️ <strong>Medical Disclaimer:</strong> For educational purposes only. Not a substitute for professional medical advice.</p>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

# ============ SIDEBAR ============
def render_sidebar(diseases_df):
    """Render sidebar with emergency info"""
    with st.sidebar:
        # User Profile
        st.markdown(f"""
        <div style="text-align: center; padding: 20px 0;">
            <div style="background: linear-gradient(135deg, #2dd4bf 0%, #14b8a6 100%);
                        width: 80px;
                        height: 80px;
                        border-radius: 50%;
                        display: flex;
                        align-items: center;
                        justify-content: center;
                        margin: 0 auto;
                        box-shadow: 0 4px 15px rgba(45, 212, 191, 0.3);">
                <span style="font-size: 45px;">👤</span>
            </div>
            <div style="font-size: 18px; font-weight: bold; margin-top: 10px; color: #f1f5f9;">{st.session_state.user_name}</div>
            <div style="font-size: 12px; color: #2dd4bf;">Active Member</div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Emergency Section
        st.markdown("### 🚨 Emergency")
        
        st.markdown("""
        <div style="background: linear-gradient(135deg, #dc2626 0%, #b91c1c 100%);
                    padding: 15px;
                    border-radius: 12px;
                    text-align: center;
                    color: white;
                    margin: 10px 0;
                    animation: pulse 2s infinite;">
            <div style="font-size: 30px;">🚨⚠️🚨</div>
            <div style="font-size: 20px; font-weight: bold;">CALL 911</div>
            <div style="font-size: 12px;">For Medical Emergencies</div>
        </div>
        """, unsafe_allow_html=True)
        
        with st.expander("⚠️ Emergency Symptoms"):
            if diseases_df is not None:
                emergency_list = diseases_df[diseases_df['emergency'] == 'Yes']['disease'].tolist()
                if emergency_list:
                    for disease in emergency_list:
                        st.write(f"• {disease}")
                else:
                    st.markdown("""
                    - Chest pain or pressure
                    - Difficulty breathing
                    - Severe bleeding
                    - Loss of consciousness
                    - Sudden severe headache
                    - Slurred speech
                    - Numbness on one side
                    - Severe allergic reaction
                    """)
            else:
                st.markdown("""
                - Chest pain or pressure
                - Difficulty breathing
                - Severe bleeding
                - Loss of consciousness
                - Sudden severe headache
                - Slurred speech
                - Numbness on one side
                - Severe allergic reaction
                """)
        
        st.markdown("---")
        
        # Quick Actions
        st.markdown("### ⚡ Quick Actions")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🗑️ Clear Chat", use_container_width=True):
                st.session_state.messages = []
                st.session_state.show_welcome = True
                st.session_state.waiting_for_answers = False
                st.session_state.current_disease = None
                st.session_state.questions = []
                st.session_state.question_index = 0
                st.session_state.answers = []
                st.rerun()
        
        with col2:
            if st.button("📤 Export", use_container_width=True):
                if st.session_state.messages:
                    chat_text = "HealthMate Chat\n" + "="*30 + "\n\n"
                    for msg in st.session_state.messages:
                        chat_text += f"{msg['role'].upper()}: {msg['content']}\n\n"
                    st.download_button(
                        "💾 Download",
                        chat_text,
                        f"chat_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                        "text/plain"
                    )
                else:
                    st.warning("No messages")
        
        st.markdown("---")
        
        # App Info & Logout
        st.markdown("""
        <div style="text-align: center; padding: 10px;">
            <div style="font-size: 28px;">🩺</div>
            <div style="font-weight: bold; color: #f1f5f9;">HealthMate v2.0</div>
            <div style="font-size: 10px; color: #94a3b8;">Your AI Health Assistant</div>
            <div style="font-size: 10px; color: #64748b; margin-top: 5px;">⚠️ Educational purpose only</div>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("🚪 Logout", use_container_width=True):
            st.session_state.logged_in = False
            st.rerun()

def get_greeting_message():
    """Return random greeting based on time of day"""
    current_hour = datetime.now().hour
    
    if 5 <= current_hour < 12:
        time_greeting = "Good Morning"
        emoji = "🌅"
    elif 12 <= current_hour < 17:
        time_greeting = "Good Afternoon"
        emoji = "☀️"
    elif 17 <= current_hour < 22:
        time_greeting = "Good Evening"
        emoji = "🌆"
    else:
        time_greeting = "Good Night"
        emoji = "🌙"
    
    random_messages = [
        f"{emoji} {time_greeting}! I'm HealthMate, your personal health assistant. How can I help you feel better today? 🩺",
        f"Hey there! {emoji} Ready to take care of your health? Tell me what's bothering you! 💙",
        f"Welcome back! {emoji} I'm here to help you 24/7. What symptoms are you experiencing? 🤒",
        f"Hi! {emoji} Your health matters to me. Let me know how I can assist you today! 🌟"
    ]
    return random.choice(random_messages)

# ============ MAIN FUNCTION ============
def main():
    # Load CSV files
    diseases_df, questions_df, medicines_df, precautions_df = load_csv_files()
    
    # Check if CSV files loaded successfully
    if diseases_df is None:
        st.error("❌ Failed to load CSV files. Please check the 'data' folder.")
        return
    
    # Initialize session state
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False
    if "show_welcome" not in st.session_state:
        st.session_state.show_welcome = True
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "user_name" not in st.session_state:
        st.session_state.user_name = "Guest"
    if "greeting_shown" not in st.session_state:
        st.session_state.greeting_shown = False
    if "waiting_for_answers" not in st.session_state:
        st.session_state.waiting_for_answers = False
    if "current_disease" not in st.session_state:
        st.session_state.current_disease = None
    if "questions" not in st.session_state:
        st.session_state.questions = []
    if "question_index" not in st.session_state:
        st.session_state.question_index = 0
    if "answers" not in st.session_state:
        st.session_state.answers = []
    
    # Check login status (no auto-login)
    if not st.session_state.logged_in:
        login_page()
        return
    
    # Main app
    load_custom_css()
    
    # Display header
    st.markdown("""
    <div style="text-align: center; margin-bottom: 20px;">
        <h1 style="background: linear-gradient(135deg, #2dd4bf 0%, #14b8a6 100%);
                   -webkit-background-clip: text; -webkit-text-fill-color: transparent;
                   font-size: 36px; margin: 0;">
            🩺 HealthMate Medical Assistant
        </h1>
        <p style="color: #94a3b8;">Your AI-powered health companion</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Render sidebar
    render_sidebar(diseases_df)
    
    # Welcome banner
    if st.session_state.show_welcome and not st.session_state.messages and not st.session_state.greeting_shown:
        greeting = get_greeting_message()
        all_diseases = ", ".join(diseases_df['disease'].head(15).tolist())
        st.markdown(f"""
        <div class="welcome-banner">
            <div style="font-size: 50px; animation: pulse 2s infinite;">👋</div>
            <h2 style="color: white;">Welcome to HealthMate, {st.session_state.user_name}! 🩺</h2>
            <p style="color: #cbd5e1;">{greeting}</p>
            <p style="font-size: 14px; margin-top: 10px; color: #2dd4bf;">💡 I can help with: {all_diseases}</p>
        </div>
        """, unsafe_allow_html=True)
        st.session_state.greeting_shown = True
    
    # Display chat history
    for message in st.session_state.messages:
        if message["role"] == "user":
            st.markdown(f"""
            <div style="display: flex; justify-content: flex-end; margin: 10px 0;">
                <div class="user-message"><strong>🧑 You</strong><br>{message['content']}</div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div style="display: flex; justify-content: flex-start; margin: 10px 0;">
                <div class="bot-message"><strong>🩺 HealthMate</strong><br>{message['content']}</div>
            </div>
            """, unsafe_allow_html=True)
    
    # Chat input
    prompt = st.chat_input("💬 Describe your symptoms...")
    
    if prompt:
        # Add user message
        st.session_state.messages.append({"role": "user", "content": prompt})
        st.session_state.show_welcome = False
        
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Check if waiting for answers
        if st.session_state.waiting_for_answers:
            # Save answer
            st.session_state.answers.append(prompt)
            st.session_state.question_index += 1
            
            # Check if more questions
            if st.session_state.question_index < len(st.session_state.questions):
                # Show next question without numbering
                response = st.session_state.questions[st.session_state.question_index]
            else:
                # All questions answered, give final advice
                disease = st.session_state.current_disease
                response = format_final_advice(disease, st.session_state.answers, diseases_df, medicines_df, precautions_df)
                
                # Reset Q&A state
                st.session_state.waiting_for_answers = False
                st.session_state.current_disease = None
                st.session_state.questions = []
                st.session_state.question_index = 0
                st.session_state.answers = []
        else:
            # Check greeting first
            greeting = get_greeting(prompt)
            
            if greeting:
                response = greeting
            else:
                # Find disease
                disease = find_disease(prompt, diseases_df)
                
                if disease:
                    # Get questions for this disease
                    questions = get_questions(disease, questions_df)
                    
                    if questions and len(questions) > 0:
                        # Start Q&A session
                        st.session_state.waiting_for_answers = True
                        st.session_state.current_disease = disease
                        st.session_state.questions = questions
                        st.session_state.question_index = 0
                        st.session_state.answers = []
                        
                        # Show first question without numbering
                        response = f"I see you're asking about **{disease}**. Let me ask you a few questions to better understand your condition:\n\n---\n{questions[0]}"
                    else:
                        # No questions available, give advice directly
                        response = format_final_advice(disease, [], diseases_df, medicines_df, precautions_df)
                else:
                    # No disease found
                    all_diseases = ", ".join(diseases_df['disease'].head(15).tolist())
                    response = f"🤔 I can help with: {all_diseases}\n\nPlease tell me what symptoms you're experiencing, or ask about a specific condition like 'flu' or 'headache'."
        
        # Add assistant response
        st.session_state.messages.append({"role": "assistant", "content": response})
        with st.chat_message("assistant"):
            st.markdown(response)
        
        st.rerun()
    
    # Footer
    st.markdown("""
    <div class="footer">
        🩺 HealthMate • Your AI Health Assistant • ⚠️ For educational purposes only
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
