import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from datetime import datetime, timedelta
from utils.privacy_calculator import calculate_comprehensive_score

st.set_page_config(
    page_title="Privacy Score Tracker",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Your Privacy Score Dashboard")
st.markdown("### Track and improve your gaming privacy protection")

# Initialize session state for score history
if 'privacy_history' not in st.session_state:
    # Generate sample history data
    dates = []
    scores = []
    base_date = datetime.now() - timedelta(days=30)
    
    for i in range(31):
        date = base_date + timedelta(days=i)
        # Simulate gradual improvement with some variation
        score = 45 + (i * 0.8) + (i % 7) * 2
        scores.append(min(100, score))
        dates.append(date)
    
    st.session_state.privacy_history = pd.DataFrame({
        'date': dates,
        'score': scores
    })

if 'current_score_components' not in st.session_state:
    st.session_state.current_score_components = {
        'Account Security': 75,
        'Data Collection Control': 60,
        'Communication Privacy': 80,
        'Social Media Integration': 45,
        'Device Security': 70,
        'Gaming Platform Settings': 55,
        'Third-party Apps': 65,
        'Privacy Knowledge': 85
    }

# Current overall score calculation
current_overall_score = sum(st.session_state.current_score_components.values()) // len(st.session_state.current_score_components)

# Score overview
st.subheader("🎯 Current Privacy Score")

col1, col2, col3, col4 = st.columns(4)

with col1:
    if current_overall_score >= 80:
        st.success(f"**{current_overall_score}/100**")
        st.markdown("🛡️ **Excellent Protection**")
    elif current_overall_score >= 60:
        st.warning(f"**{current_overall_score}/100**")
        st.markdown("⚠️ **Good Protection**")
    else:
        st.error(f"**{current_overall_score}/100**")
        st.markdown("🚨 **Needs Improvement**")

with col2:
    # Calculate trend
    recent_scores = st.session_state.privacy_history.tail(7)['score']
    older_scores = st.session_state.privacy_history.head(7)['score']
    trend = recent_scores.mean() - older_scores.mean()
    
    st.metric(
        "7-Day Trend",
        f"{trend:+.1f} points",
        delta=f"{trend:+.1f}"
    )

with col3:
    # Risk level
    if current_overall_score >= 80:
        risk_level = "Low"
        st.success("🟢 Low Risk")
    elif current_overall_score >= 60:
        risk_level = "Medium"
        st.warning("🟡 Medium Risk")
    else:
        risk_level = "High"
        st.error("🔴 High Risk")

with col4:
    # Next milestone
    if current_overall_score < 60:
        next_milestone = 60
        st.info(f"🎯 Next: {next_milestone - current_overall_score} pts to Good")
    elif current_overall_score < 80:
        next_milestone = 80
        st.info(f"🎯 Next: {next_milestone - current_overall_score} pts to Excellent")
    else:
        st.success("🏆 Maximum Level!")

st.markdown("---")

# Score breakdown
col1, col2 = st.columns(2)

with col1:
    st.subheader("📈 Score History")
    
    fig = px.line(
        st.session_state.privacy_history,
        x='date',
        y='score',
        title='Privacy Score Over Time'
    )
    fig.add_hline(y=80, line_dash="dash", line_color="green", annotation_text="Excellent (80+)")
    fig.add_hline(y=60, line_dash="dash", line_color="orange", annotation_text="Good (60+)")
    fig.add_hline(y=40, line_dash="dash", line_color="red", annotation_text="Needs Improvement (<60)")
    fig.update_layout(yaxis_range=[0, 100])
    
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.subheader("🎯 Score Breakdown")
    
    # Radar chart for current components
    categories = list(st.session_state.current_score_components.keys())
    values = list(st.session_state.current_score_components.values())
    
    fig = go.Figure(data=go.Scatterpolar(
        r=values,
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
        title="Privacy Protection by Category"
    )
    
    st.plotly_chart(fig, use_container_width=True)

# Detailed breakdown
st.subheader("🔍 Detailed Category Analysis")

for category, score in st.session_state.current_score_components.items():
    with st.expander(f"{category}: {score}/100"):
        
        # Progress bar
        progress_color = "green" if score >= 80 else "orange" if score >= 60 else "red"
        st.markdown(f"**Current Score: {score}/100**")
        
        progress_bar = st.progress(score / 100)
        
        # Category-specific recommendations
        if category == "Account Security":
            if score < 80:
                st.markdown("**🛡️ Recommendations to improve:**")
                st.markdown("- Enable two-factor authentication on all gaming accounts")
                st.markdown("- Use unique, strong passwords for each account")
                st.markdown("- Regularly review account login activity")
                st.markdown("- Update recovery information")
        
        elif category == "Data Collection Control":
            if score < 80:
                st.markdown("**📊 Recommendations to improve:**")
                st.markdown("- Review and adjust privacy settings in all games")
                st.markdown("- Limit data sharing with third parties")
                st.markdown("- Disable unnecessary analytics and telemetry")
                st.markdown("- Regular privacy settings audits")
        
        elif category == "Communication Privacy":
            if score < 80:
                st.markdown("**💬 Recommendations to improve:**")
                st.markdown("- Be cautious about sharing personal information in chat")
                st.markdown("- Use voice chat privacy settings")
                st.markdown("- Limit friend requests from strangers")
                st.markdown("- Review message and call history settings")
        
        elif category == "Social Media Integration":
            if score < 80:
                st.markdown("**🔗 Recommendations to improve:**")
                st.markdown("- Limit connections between gaming and social accounts")
                st.markdown("- Review sharing settings for achievements and progress")
                st.markdown("- Control what information is visible to friends")
                st.markdown("- Regularly audit connected applications")
        
        elif category == "Device Security":
            if score < 80:
                st.markdown("**📱 Recommendations to improve:**")
                st.markdown("- Keep gaming apps and OS updated")
                st.markdown("- Use device lock screens and biometrics")
                st.markdown("- Install apps only from official stores")
                st.markdown("- Regular security scans and maintenance")
        
        elif category == "Gaming Platform Settings":
            if score < 80:
                st.markdown("**🎮 Recommendations to improve:**")
                st.markdown("- Configure platform privacy settings")
                st.markdown("- Control profile visibility and information sharing")
                st.markdown("- Manage friend and follower permissions")
                st.markdown("- Review purchase and payment privacy")
        
        elif category == "Third-party Apps":
            if score < 80:
                st.markdown("**🔌 Recommendations to improve:**")
                st.markdown("- Audit connected third-party applications")
                st.markdown("- Remove unnecessary app permissions")
                st.markdown("- Limit data sharing with external services")
                st.markdown("- Regular review of authorized applications")
        
        elif category == "Privacy Knowledge":
            if score < 80:
                st.markdown("**📚 Recommendations to improve:**")
                st.markdown("- Complete privacy education modules")
                st.markdown("- Stay updated on privacy best practices")
                st.markdown("- Learn about new privacy threats")
                st.markdown("- Practice privacy-conscious gaming habits")
        
        # Quick action buttons
        col1, col2 = st.columns(2)
        with col1:
            if st.button(f"📚 Learn More", key=f"learn_{category}"):
                st.switch_page("pages/privacy_education.py")
        with col2:
            if st.button(f"⚙️ Quick Improve", key=f"improve_{category}"):
                # Simulate small improvement
                st.session_state.current_score_components[category] = min(100, score + 5)
                st.success("Progress made! +5 points")
                st.rerun()

# Score improvement suggestions
st.subheader("🚀 Quick Wins to Improve Your Score")

# Find lowest scoring categories
sorted_categories = sorted(st.session_state.current_score_components.items(), key=lambda x: x[1])
lowest_three = sorted_categories[:3]

col1, col2, col3 = st.columns(3)

for i, (category, score) in enumerate(lowest_three):
    with [col1, col2, col3][i]:
        st.markdown(f"**{category}**")
        st.markdown(f"Current: {score}/100")
        
        if category == "Social Media Integration":
            action = "Disconnect unused social accounts"
            potential_gain = 15
        elif category == "Gaming Platform Settings":
            action = "Review platform privacy settings"
            potential_gain = 12
        elif category == "Data Collection Control":
            action = "Opt out of analytics"
            potential_gain = 10
        else:
            action = "Follow category recommendations"
            potential_gain = 8
        
        st.info(f"💡 {action}")
        st.success(f"Potential: +{potential_gain} points")

# Achievements and milestones
st.subheader("🏆 Privacy Achievements")

achievements = []
if current_overall_score >= 50:
    achievements.append("🎯 Privacy Aware - Reached 50+ score")
if current_overall_score >= 70:
    achievements.append("🛡️ Privacy Conscious - Reached 70+ score")
if current_overall_score >= 85:
    achievements.append("🏆 Privacy Expert - Reached 85+ score")
if all(score >= 60 for score in st.session_state.current_score_components.values()):
    achievements.append("⚖️ Well Balanced - All categories 60+")
if any(score >= 90 for score in st.session_state.current_score_components.values()):
    achievements.append("🌟 Category Master - One category 90+")

if achievements:
    for achievement in achievements:
        st.success(achievement)
else:
    st.info("Keep improving to unlock achievements!")

# Action buttons
st.markdown("---")
col1, col2, col3 = st.columns(3)

with col1:
    if st.button("🔍 Take Privacy Assessment", use_container_width=True):
        st.switch_page("pages/privacy_assessment.py")

with col2:
    if st.button("📚 Learn Privacy Basics", use_container_width=True):
        st.switch_page("pages/privacy_education.py")

with col3:
    if st.button("📋 Check Privacy List", use_container_width=True):
        st.switch_page("pages/privacy_checklist.py")

# Back to dashboard
if st.button("🏠 Back to Dashboard"):
    st.switch_page("app.py")
