import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
from utils.privacy_calculator import calculate_risk_score, get_risk_recommendations

st.set_page_config(
    page_title="Privacy Risk Assessment",
    page_icon="🎮",
    layout="wide"
)

st.title("🎮 Gaming Privacy Risk Assessment")
st.markdown("### Evaluate your current privacy risks while gaming")

# Assessment form
st.subheader("📋 Privacy Assessment Questionnaire")

with st.form("privacy_assessment"):
    st.markdown("**Gaming Habits**")
    
    col1, col2 = st.columns(2)
    
    with col1:
        gaming_frequency = st.select_slider(
            "How often do you play online games?",
            options=["Rarely", "Weekly", "Daily", "Multiple times daily"],
            value="Weekly"
        )
        
        multiplayer_gaming = st.selectbox(
            "Do you play multiplayer games?",
            ["Never", "Occasionally", "Frequently", "Always"]
        )
        
        voice_chat = st.selectbox(
            "Do you use voice chat while gaming?",
            ["Never", "With friends only", "With strangers sometimes", "Frequently with strangers"]
        )
        
        streaming = st.selectbox(
            "Do you stream your gameplay?",
            ["Never", "Rarely", "Regularly", "Professionally"]
        )
    
    with col2:
        account_sharing = st.selectbox(
            "Do you share gaming accounts?",
            ["Never", "With family", "With friends", "With strangers"]
        )
        
        personal_info_sharing = st.selectbox(
            "How often do you share personal information in games?",
            ["Never", "Rarely", "Sometimes", "Frequently"]
        )
        
        password_practices = st.selectbox(
            "How do you manage gaming passwords?",
            ["Unique strong passwords", "Some unique passwords", "Similar passwords", "Same password everywhere"]
        )
        
        two_factor_auth = st.selectbox(
            "Do you use two-factor authentication?",
            ["On all accounts", "On some accounts", "On few accounts", "Never"]
        )
    
    st.markdown("**Privacy Settings Awareness**")
    
    col3, col4 = st.columns(2)
    
    with col3:
        privacy_settings_check = st.selectbox(
            "How often do you review privacy settings?",
            ["Regularly", "When reminded", "Rarely", "Never"]
        )
        
        data_collection_awareness = st.selectbox(
            "Are you aware of what data games collect?",
            ["Very aware", "Somewhat aware", "Not very aware", "Not aware at all"]
        )
    
    with col4:
        permission_review = st.selectbox(
            "Do you review app permissions before installing games?",
            ["Always", "Usually", "Sometimes", "Never"]
        )
        
        third_party_connections = st.selectbox(
            "Do you connect gaming accounts to social media?",
            ["Never", "Rarely", "Sometimes", "Frequently"]
        )
    
    submitted = st.form_submit_button("🔍 Assess My Privacy Risk", use_container_width=True)

if submitted:
    # Calculate risk score based on responses
    responses = {
        'gaming_frequency': gaming_frequency,
        'multiplayer_gaming': multiplayer_gaming,
        'voice_chat': voice_chat,
        'streaming': streaming,
        'account_sharing': account_sharing,
        'personal_info_sharing': personal_info_sharing,
        'password_practices': password_practices,
        'two_factor_auth': two_factor_auth,
        'privacy_settings_check': privacy_settings_check,
        'data_collection_awareness': data_collection_awareness,
        'permission_review': permission_review,
        'third_party_connections': third_party_connections
    }
    
    risk_score, risk_level, category_scores = calculate_risk_score(responses)
    
    st.markdown("---")
    st.subheader("🎯 Your Privacy Risk Assessment Results")
    
    # Display overall risk
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if risk_level == "Low":
            st.success(f"**Risk Level: {risk_level}**")
            st.metric("Overall Risk Score", f"{risk_score}/100", delta="Low risk")
        elif risk_level == "Medium":
            st.warning(f"**Risk Level: {risk_level}**")
            st.metric("Overall Risk Score", f"{risk_score}/100", delta="Medium risk")
        else:
            st.error(f"**Risk Level: {risk_level}**")
            st.metric("Overall Risk Score", f"{risk_score}/100", delta="High risk")
    
    with col2:
        # Risk breakdown chart
        fig = go.Figure(data=go.Scatterpolar(
            r=list(category_scores.values()),
            theta=list(category_scores.keys()),
            fill='toself',
            name='Risk Levels'
        ))
        fig.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, 100]
                )),
            showlegend=False,
            title="Risk Breakdown by Category",
            height=300
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col3:
        # Risk distribution
        risk_categories = list(category_scores.keys())
        risk_values = list(category_scores.values())
        
        fig = px.bar(
            x=risk_values,
            y=risk_categories,
            orientation='h',
            title="Category Risk Scores",
            color=risk_values,
            color_continuous_scale="RdYlGn_r"
        )
        fig.update_layout(height=300, showlegend=False)
        st.plotly_chart(fig, use_container_width=True)
    
    # Recommendations
    st.subheader("🛡️ Personalized Recommendations")
    
    recommendations = get_risk_recommendations(responses, category_scores)
    
    for i, rec in enumerate(recommendations, 1):
        with st.expander(f"Recommendation {i}: {rec['title']}", expanded=i<=3):
            st.markdown(f"**Priority:** {rec['priority']}")
            st.markdown(f"**Description:** {rec['description']}")
            st.markdown(f"**Action Steps:**")
            for step in rec['steps']:
                st.markdown(f"- {step}")
    
    # Progress tracking
    st.subheader("📈 Track Your Progress")
    
    if st.button("📊 View Detailed Privacy Score", use_container_width=True):
        st.switch_page("pages/privacy_score.py")
    
    if st.button("📚 Learn More About Privacy", use_container_width=True):
        st.switch_page("pages/privacy_education.py")

# Back to dashboard
if st.button("🏠 Back to Dashboard"):
    st.switch_page("app.py")
