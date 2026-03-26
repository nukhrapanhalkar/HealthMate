# app.py - HealthMate Medical Assistant
# Uses diseases.csv, questions.csv, medicines.csv, precautions.csv

import streamlit as st
import pandas as pd
from datetime import datetime
import os

# ============ LOAD CSV FILES FROM DATA FOLDER ============

# Define the data folder path
data_folder = "data"

# Check if data folder exists
if not os.path.exists(data_folder):
    st.error(f"❌ The '{data_folder}' folder does not exist!")
    st.info(f"Please create a '{data_folder}' folder and put your CSV files there.")
    st.stop()

# Load diseases.csv
try:
    diseases_path = os.path.join(data_folder, "diseases.csv")
    df = pd.read_csv(diseases_path)
except FileNotFoundError:
    st.error(f"❌ Could not find data/diseases.csv file!")
    st.stop()
except Exception as e:
    st.error(f"❌ Error loading diseases.csv: {e}")
    st.stop()

# Load questions.csv
try:
    questions_path = os.path.join(data_folder, "questions.csv")
    questions_df = pd.read_csv(questions_path)
except FileNotFoundError:
    st.error(f"❌ Could not find data/questions.csv file!")
    st.stop()
except Exception as e:
    st.error(f"❌ Error loading questions.csv: {e}")
    st.stop()

# Load medicines.csv
try:
    medicines_path = os.path.join(data_folder, "medicines.csv")
    medicines_df = pd.read_csv(medicines_path)
except FileNotFoundError:
    st.error(f"❌ Could not find data/medicines.csv file!")
    st.stop()
except Exception as e:
    st.error(f"❌ Error loading medicines.csv: {e}")
    st.stop()

# Load precautions.csv
try:
    precautions_path = os.path.join(data_folder, "precautions.csv")
    precautions_df = pd.read_csv(precautions_path)
except FileNotFoundError:
    st.error(f"❌ Could not find data/precautions.csv file!")
    st.stop()
except Exception as e:
    st.error(f"❌ Error loading precautions.csv: {e}")
    st.stop()

# ============ HELPER FUNCTIONS ============

def find_disease(text):
    """Find which disease the user mentioned"""
    text_lower = text.lower()
    for disease in df['disease']:
        if disease.lower() in text_lower:
            return disease
    return None

def get_questions(disease):
    """Get questions for a specific disease from questions.csv"""
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

def get_medicines(disease):
    """Get medicines for a specific disease from medicines.csv"""
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

def get_precautions(disease):
    """Get precautions for a specific disease from precautions.csv"""
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

def get_disease_info(disease):
    """Get basic disease info from diseases.csv"""
    info = df[df['disease'] == disease]
    if not info.empty:
        return info.iloc[0]
    return None

def format_final_advice(disease, answers):
    """Format final advice with medicines and precautions"""
    info = get_disease_info(disease)
    medicines = get_medicines(disease)
    precautions = get_precautions(disease)
    
    text = f"## 🩺 {disease}\n\n"
    
    # Severity warning
    if info is not None:
        severity = info['severity']
        if severity == 'Severe':
            text += "🚨 **SEVERE - Seek medical help immediately** 🚨\n\n"
        elif severity == 'Moderate':
            text += "⚠️ **Moderate - Monitor closely** ⚠️\n\n"
        else:
            text += "✅ **Mild - Self-care recommended** ✅\n\n"
    
    # Precautions section
    if precautions:
        text += "### 🛡️ PROTECT\n"
        for prec in precautions:
            text += f"• {prec}\n"
        text += "\n"
    
    # Medicines section
    if medicines:
        text += "### 💊 Rx\n"
        for med in medicines:
            text += f"• {med}\n"
        text += "\n"
    
    # Additional advice from CSV
    if info is not None:
        text += f"### 📋 PLAN\n{info['what_to_do']}\n\n"
        text += f"### 🏥 See doctor if:\n{info['see_doctor']}\n\n"
    
    # Emergency warning
    if info is not None and info['emergency'] == 'Yes':
        text += "🚨 **⚠️ THIS IS A MEDICAL EMERGENCY - SEEK HELP NOW!** ⚠️ 🚨\n\n"
    
    # Disclaimer
    text += "---\n⚠️ *Not a doctor. For educational purposes only. In emergencies, call emergency services.*"
    
    return text

def get_greeting(text):
    """Handle greetings"""
    text_lower = text.lower()
    greetings = ['hello', 'hi', 'hey', 'good morning', 'good afternoon', 'greetings', 'howdy']
    
    if any(g in text_lower for g in greetings):
        return "Hello! 👋 I'm **🩺 HealthMate**, your smart health assistant. Tell me what symptoms you're experiencing."
    
    if 'thank' in text_lower:
        return "You're welcome! 💙 Take care and feel better soon!"
    
    if text_lower in ['bye', 'goodbye', 'exit', 'quit', 'see you']:
        return "Goodbye! 🌟 Stay healthy and take care!"
    
    return None

# ============ SETUP APP ============
st.set_page_config(
    page_title="HealthMate - Medical Assistant",
    page_icon="🩺",
    layout="wide"
)

# Title with new emojis
st.title("🩺 HealthMate")
st.caption("*Your Smart Health Assistant* 🧑‍⚕️")
st.warning("⚠️ Not a doctor. For educational purposes only. Call emergency services for serious medical issues.")

# Session state
if "messages" not in st.session_state:
    st.session_state.messages = []
    
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

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
prompt = st.chat_input("💬 Describe your symptoms...")

if prompt:
    # Add user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(f"💬 {prompt}")
    
    # Check if waiting for answers
    if st.session_state.waiting_for_answers:
        # Save answer
        st.session_state.answers.append(prompt)
        st.session_state.question_index += 1
        
        # Check if more questions
        if st.session_state.question_index < len(st.session_state.questions):
            response = f"**Question {st.session_state.question_index + 1} of {len(st.session_state.questions)}:**\n\n{st.session_state.questions[st.session_state.question_index]}"
        else:
            # All questions answered, give final advice
            disease = st.session_state.current_disease
            response = format_final_advice(disease, st.session_state.answers)
            
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
            disease = find_disease(prompt)
            
            if disease:
                # Get questions for this disease
                questions = get_questions(disease)
                
                if questions and len(questions) > 0:
                    # Start Q&A session
                    st.session_state.waiting_for_answers = True
                    st.session_state.current_disease = disease
                    st.session_state.questions = questions
                    st.session_state.question_index = 0
                    st.session_state.answers = []
                    
                    response = f"I see you're asking about **{disease}**. Let me ask you a few questions to better understand your condition:\n\n---\n**Question 1 of {len(questions)}:**\n{questions[0]}"
                else:
                    # No questions available, give advice directly
                    response = format_final_advice(disease, [])
            else:
                # No disease found
                all_diseases = ", ".join(df['disease'].head(15).tolist())
                response = f"I can help with: {all_diseases}\n\nPlease tell me what symptoms you're experiencing, or ask about a specific condition."
    
    # Add assistant response
    st.session_state.messages.append({"role": "assistant", "content": response})
    with st.chat_message("assistant"):
        st.markdown(response)
    
    st.rerun()

# ============ SIDEBAR ============
with st.sidebar:
    st.header("🚨 EMERGENCY ALERT")
    
    # Get emergency conditions from database
    emergency_list = df[df['emergency'] == 'Yes']['disease'].tolist()
    
    if emergency_list:
        for disease in emergency_list:
            st.write(f"🚨 **{disease}**")
            st.write("")
    else:
        st.write("🚨 **Emergency Conditions:**")
        st.write("• Chest pain")
        st.write("• Difficulty breathing")
        st.write("• Severe bleeding")
        st.write("• Loss of consciousness")
    
    st.divider()
    
    # Clear Chat button
    if st.button("🗑️ Clear"):
        st.session_state.messages = []
        st.session_state.waiting_for_answers = False
        st.session_state.current_disease = None
        st.session_state.questions = []
        st.session_state.question_index = 0
        st.session_state.answers = []
        st.rerun()
    
    # Export Chat button
    if st.button("📤 Export"):
        if st.session_state.messages:
            data = []
            for msg in st.session_state.messages:
                data.append({
                    "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "role": msg["role"],
                    "message": msg["content"]
                })
            export_df = pd.DataFrame(data)
            csv = export_df.to_csv(index=False)
            st.download_button(
                "💾 Download",
                csv,
                f"chat_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                "text/csv"
            )
        else:
            st.info("No messages to export")
    
    st.caption("🩺 HealthMate v1.0")
    st.caption("🎯 Your Smart Health Assistant")