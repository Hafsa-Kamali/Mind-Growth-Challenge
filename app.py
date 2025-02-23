import streamlit as st
import pandas as pd
from datetime import datetime
import plotly.express as px
import json
import os

# Set page configuration
st.set_page_config(
    page_title="Growth Mindset Tracker",
    page_icon="🌱",
    layout="wide"
)

# Custom CSS - All styles in one place
st.markdown("""
    <style>
        /* Main Content Styling */
        .main {
            padding: 2rem;
            background-color: #f8f9fa;
        }
        
        /* Button Styling */
        .stButton>button {
            width: 100%;
            border-radius: 8px;
            height: 3em;
            background-color: #3b82f6;
            color: white;
            font-weight: bold;
            transition: all 0.3s ease;
        }
        
        /* Card Styling */
        .reflection-card {
            background-color: #ffffff;
            padding: 25px;
            border-radius: 12px;
            margin: 15px 0;
            box-shadow: 0 4px 6px rgba(0,0,0,0.05);
        }
        
        .metric-card {
            background-color: #ffffff;
            padding: 25px;
            border-radius: 12px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.05);
            margin: 15px 0;
            border-left: 4px solid #3b82f6;
        }
        
        /* Sidebar Styling */
        [data-testid="stSidebar"] {
            background-color: #1a1f2d;
            padding: 2rem 1rem;
        }
        
        [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] {
            color: white;
        }
        
        /* Sidebar Navigation */
        [data-testid="stSidebar"] .st-emotion-cache-1cypcdb {
            background-color: transparent;
            padding: 0;
        }
        
        [data-testid="stSidebar"] .st-emotion-cache-1cypcdb > div {
            background-color: #2d3748;
            margin: 0.5rem 0;
            padding: 1rem;
            border-radius: 10px;
            transition: all 0.3s ease;
        }
        
        [data-testid="stSidebar"] .st-emotion-cache-1cypcdb > div:hover {
            background-color: #3182ce;
            transform: translateX(5px);
        }
        
        /* Hide default radio button */
        [data-testid="stSidebar"] .st-emotion-cache-1cypcdb input[type="radio"] {
            display: none;
        }
        
        /* Footer Styling */
        .stMarkdown {
            color: white;
        }
    </style>
""", unsafe_allow_html=True)

# Initialize session state
if 'reflections' not in st.session_state:
    st.session_state.reflections = []
if 'goals' not in st.session_state:
    st.session_state.goals = []
if 'achievements' not in st.session_state:
    st.session_state.achievements = []

# Sidebar Content
st.sidebar.markdown("""
    <div style='text-align: center; padding: 1rem; margin-bottom: 2rem; border-bottom: 2px solid #3182ce;'>
        <div style='font-size: 2rem; margin-bottom: 0.5rem;'>🌱</div>
        <div style='font-size: 1.2rem; font-weight: bold;'>Growth Mindset</div>
    </div>
""", unsafe_allow_html=True)

# Navigation items
pages = {
    "Dashboard": "📊",
    "Daily Reflection": "📝",
    "Goal Setting": "🎯",
    "Resources": "📚"
}

selected_page = st.sidebar.radio(
    "Navigation",
    list(pages.keys()),
    format_func=lambda x: f"{pages[x]} {x}"
)

# Sidebar Footer
st.sidebar.markdown("""
    <div style='position: fixed; bottom: 0; left: 0; width: 100%; text-align: center; 
                padding: 1rem; background-color: #1a1f2d; border-top: 1px solid #2d3748;'>
        <div style='margin-bottom: 0.5rem;'>🌟 Stay Motivated</div>
        <div style='font-size: 0.8rem; color: #718096;'>Version 2.0</div>
    </div>
""", unsafe_allow_html=True)

# Main title
st.title("🌱 Growth Mindset Journey")
st.markdown("### Transform Your Learning Experience")

# Rest of your page content based on selection
if selected_page == "Dashboard":
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 📊 Your Growth Journey")
        if st.session_state.reflections:
            df = pd.DataFrame(st.session_state.reflections)
            fig = px.line(df, x='date', y='mindset_score', 
                title='Your Mindset Progress Over Time')
            st.plotly_chart(fig)
        else:
            st.info("Start adding daily reflections to see your progress!")
    
    with col2:
        st.markdown("### 🎯 Active Goals")
        if st.session_state.goals:
            for goal in st.session_state.goals:
                with st.expander(goal['title']):
                    st.write(f"Target Date: {goal['target_date']}")
                    st.write(f"Progress: {goal['progress']}%")
                    st.progress(goal['progress'] / 100)
        else:
            st.info("Set your first goal in the Goal Setting section!")

elif selected_page == "Daily Reflection":
    st.markdown("### 📝 Daily Reflection")
    
    with st.form("reflection_form"):
        date = st.date_input("Date", datetime.now())
        
        st.markdown("#### Rate your mindset today (1-10):")
        mindset_score = st.slider("", 1, 10, 5)
        
        challenges = st.text_area("What challenges did you face today?")
        learnings = st.text_area("What did you learn from these challenges?")
        
        if st.form_submit_button("Save Reflection"):
            reflection = {
                'date': date.strftime("%Y-%m-%d"),
                'mindset_score': mindset_score,
                'challenges': challenges,
                'learnings': learnings
            }
            st.session_state.reflections.append(reflection)
            st.success("Reflection saved successfully!")

elif selected_page == "Goal Setting":
    st.markdown("### 🎯 Set New Goals")
    
    with st.form("goal_form"):
        goal_title = st.text_input("Goal Title")
        goal_description = st.text_area("Goal Description")
        target_date = st.date_input("Target Date")
        
        if st.form_submit_button("Add Goal"):
            new_goal = {
                'title': goal_title,
                'description': goal_description,
                'target_date': target_date.strftime("%Y-%m-%d"),
                'progress': 0
            }
            st.session_state.goals.append(new_goal)
            st.success("Goal added successfully!")
    
    st.markdown("### Current Goals")
    for i, goal in enumerate(st.session_state.goals):
        with st.expander(goal['title']):
            new_progress = st.slider("Update Progress", 0, 100, 
                int(goal['progress']), key=f"progress_{i}")
            st.session_state.goals[i]['progress'] = new_progress

elif selected_page == "Resources":
    st.markdown("### 📚 Growth Mindset Resources")
    
    st.markdown("""
    #### Key Concepts of Growth Mindset
    
    1. **Embrace Challenges**
       - Challenges are opportunities for growth
       - Each obstacle makes you stronger
    
    2. **Learn from Mistakes**
       - Mistakes are valuable learning experiences
       - Failed attempts provide insights for improvement
    
    3. **Effort Leads to Mastery**
       - Hard work and dedication drive improvement
       - Practice and persistence are key to success
    
    #### Recommended Reading
    - "Mindset: The New Psychology of Success" by Carol Dweck
    - "Grit: The Power of Passion and Perseverance" by Angela Duckworth
    - "Peak: Secrets from the New Science of Expertise" by Anders Ericsson
    """)
    
    # Quick Tips Section
    st.markdown("### 💡 Quick Tips for Maintaining a Growth Mindset")
    tips = [
        "Replace 'I can't' with 'I can't yet'",
        "Focus on the process, not just the outcome",
        "Celebrate small improvements",
        "Seek feedback and learn from criticism",
        "View challenges as opportunities"
    ]
    
    for tip in tips:
        st.markdown(f"- {tip}")

# Footer
st.markdown("---")
st.markdown("Built with 💚 to support your growth journey")