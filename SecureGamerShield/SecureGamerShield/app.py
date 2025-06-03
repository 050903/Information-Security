import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import pandas as pd

# Configure the page
st.set_page_config(
    page_title="SecureGamer - Privacy Education Platform",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state
if 'privacy_score' not in st.session_state:
    st.session_state.privacy_score = 65
if 'modules_completed' not in st.session_state:
    st.session_state.modules_completed = 0
if 'quiz_scores' not in st.session_state:
    st.session_state.quiz_scores = []

def main():
    st.title("🛡️ SecureGamer Privacy Education Platform")
    st.markdown("### Protecting Your Digital Privacy While Gaming")
    
    # Sidebar navigation
    st.sidebar.title("Navigation")
    
    # Main dashboard content
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(
            label="Your Privacy Score", 
            value=f"{st.session_state.privacy_score}/100",
            delta="5 points this week"
        )
    
    with col2:
        st.metric(
            label="Modules Completed", 
            value=f"{st.session_state.modules_completed}/8",
            delta="2 new modules"
        )
    
    with col3:
        st.metric(
            label="Risk Level", 
            value="Medium",
            delta="-1 level improved"
        )
    
    st.markdown("---")
    
    # Quick stats
    st.subheader("📊 Privacy Awareness Dashboard")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Privacy score trend (simulated)
        dates = pd.date_range(start='2024-01-01', periods=30, freq='D')
        scores = [60 + i + (i % 7) * 2 for i in range(30)]
        
        fig = px.line(
            x=dates, 
            y=scores,
            title="Privacy Score Trend",
            labels={'x': 'Date', 'y': 'Privacy Score'}
        )
        fig.update_layout(showlegend=False)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Risk categories
        categories = ['Data Collection', 'Account Security', 'Communication Privacy', 'Device Security']
        scores = [75, 68, 82, 55]
        
        fig = go.Figure(data=go.Scatterpolar(
            r=scores,
            theta=categories,
            fill='toself',
            name='Current Score'
        ))
        fig.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, 100]
                )),
            showlegend=False,
            title="Privacy Risk Assessment"
        )
        st.plotly_chart(fig, use_container_width=True)
    
    # Recent activity
    st.subheader("🎯 Quick Actions")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if st.button("🎮 Start Privacy Assessment", use_container_width=True):
            st.switch_page("pages/privacy_assessment.py")
    
    with col2:
        if st.button("📚 Privacy Education", use_container_width=True):
            st.switch_page("pages/privacy_education.py")
    
    with col3:
        if st.button("📋 Privacy Checklist", use_container_width=True):
            st.switch_page("pages/privacy_checklist.py")
    
    with col4:
        if st.button("🔍 Data Transparency", use_container_width=True):
            st.switch_page("pages/data_transparency.py")
    
    # Add the new secure login demo button
    st.markdown("---")
    st.subheader("🔐 Advanced Security Features")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("🔐 Secure Login & Encryption Demo", use_container_width=True):
            st.switch_page("pages/secure_login_demo.py")
    
    with col2:
        if st.button("🎛️ Privacy Controls Demo", use_container_width=True):
            st.switch_page("pages/privacy_controls_demo.py")
    
    # Add database dashboard
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("🗄️ Database Dashboard", use_container_width=True):
            st.switch_page("pages/database_dashboard.py")
    
    st.markdown("---")
    
    # Tips of the day
    st.subheader("💡 Daily Privacy Tip")
    
    tips = [
        "Always review privacy settings when installing new games",
        "Use strong, unique passwords for each gaming account",
        "Be cautious about sharing personal information in game chats",
        "Regularly check what data your games are collecting",
        "Enable two-factor authentication on all gaming accounts"
    ]
    
    import random
    daily_tip = random.choice(tips)
    
    st.info(f"🎯 **Today's Tip:** {daily_tip}")
    
    # Recent privacy news (placeholder)
    st.subheader("📰 Privacy News for Gamers")
    
    with st.expander("Latest Privacy Updates"):
        st.markdown("""
        - **Gaming Platform Updates**: New privacy controls released for major gaming platforms
        - **Data Protection**: Tips for protecting your gaming data during online play
        - **Security Alert**: Recent gaming security vulnerabilities and how to protect yourself
        """)

if __name__ == "__main__":
    main()
