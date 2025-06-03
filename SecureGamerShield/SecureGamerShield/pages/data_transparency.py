import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from datetime import datetime, timedelta

st.set_page_config(
    page_title="Data Transparency Simulator",
    page_icon="🔍",
    layout="wide"
)

st.title("🔍 Data Collection Transparency Simulator")
st.markdown("### Understand what data games collect and how it's used")

# Game selector
st.subheader("🎮 Select a Game Type to Explore")

game_type = st.selectbox(
    "Choose a game category:",
    ["Mobile Puzzle Game", "Online Multiplayer Shooter", "Social Gaming Platform", "VR Game", "Streaming Platform"]
)

# Simulate data collection based on game type
def get_game_data_collection(game_type):
    base_data = {
        "Device Information": ["Device Model", "Operating System", "Screen Resolution", "Hardware Specs"],
        "Account Data": ["Username", "Email Address", "Age", "Profile Picture"],
        "Gameplay Data": ["Play Time", "Level Progress", "Game Statistics", "Achievement Data"]
    }
    
    if game_type == "Mobile Puzzle Game":
        return {
            **base_data,
            "Location Data": ["Country", "City", "Time Zone"],
            "App Usage": ["Session Duration", "App Opens", "In-App Purchases"],
            "Advertising": ["Ad Interactions", "Marketing Preferences"]
        }
    elif game_type == "Online Multiplayer Shooter":
        return {
            **base_data,
            "Communication": ["Voice Chat", "Text Messages", "Friend Lists"],
            "Network Data": ["IP Address", "Connection Quality", "Server Preferences"],
            "Behavioral Data": ["Playstyle Analysis", "Team Interactions", "Reporting History"]
        }
    elif game_type == "Social Gaming Platform":
        return {
            **base_data,
            "Social Data": ["Friend Networks", "Group Memberships", "Social Interactions"],
            "Content Data": ["Shared Content", "Comments", "Reactions"],
            "Communication": ["Messages", "Voice Chat", "Video Calls"]
        }
    elif game_type == "VR Game":
        return {
            **base_data,
            "Biometric Data": ["Head Movement", "Hand Tracking", "Eye Tracking"],
            "Spatial Data": ["Room Layout", "Movement Patterns", "Physical Interactions"],
            "Health Data": ["Play Session Length", "Movement Intensity"]
        }
    else:  # Streaming Platform
        return {
            **base_data,
            "Streaming Data": ["Stream Content", "Viewer Interactions", "Chat Messages"],
            "Social Data": ["Follower Lists", "Subscriptions", "Community Posts"],
            "Monetization": ["Donations", "Subscriptions", "Revenue Data"]
        }

data_categories = get_game_data_collection(game_type)

# Display data collection overview
st.subheader("📊 Data Collection Overview")

col1, col2 = st.columns([2, 1])

with col1:
    # Create a comprehensive view of collected data
    all_data_points = []
    for category, items in data_categories.items():
        for item in items:
            all_data_points.append({"Category": category, "Data Point": item})
    
    df = pd.DataFrame(all_data_points)
    
    # Count by category
    category_counts = df['Category'].value_counts()
    
    fig = px.pie(
        values=category_counts.values,
        names=category_counts.index,
        title=f"Data Collection Breakdown - {game_type}"
    )
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.metric("Total Data Points", len(all_data_points))
    st.metric("Data Categories", len(data_categories))
    
    # Risk assessment
    high_risk_categories = ["Biometric Data", "Location Data", "Communication", "Social Data"]
    risk_count = sum(1 for cat in data_categories.keys() if cat in high_risk_categories)
    
    if risk_count >= 3:
        st.error(f"High Privacy Risk ({risk_count} sensitive categories)")
    elif risk_count >= 2:
        st.warning(f"Medium Privacy Risk ({risk_count} sensitive categories)")
    else:
        st.success(f"Lower Privacy Risk ({risk_count} sensitive categories)")

# Detailed data breakdown
st.subheader("🔍 Detailed Data Collection Analysis")

for category, items in data_categories.items():
    with st.expander(f"📁 {category} ({len(items)} data points)"):
        
        # Risk level for category
        if category in ["Biometric Data", "Location Data"]:
            st.error("🔴 High Privacy Risk Category")
        elif category in ["Communication", "Social Data", "Behavioral Data"]:
            st.warning("🟡 Medium Privacy Risk Category")
        else:
            st.success("🟢 Lower Privacy Risk Category")
        
        # List data points
        for item in items:
            st.markdown(f"• **{item}**")
        
        # Purpose and usage
        st.markdown("**Typical Uses:**")
        if category == "Device Information":
            st.markdown("- Game optimization and compatibility")
            st.markdown("- Technical support and troubleshooting")
            st.markdown("- Analytics and performance monitoring")
        elif category == "Account Data":
            st.markdown("- User identification and authentication")
            st.markdown("- Personalized gaming experience")
            st.markdown("- Communication with support")
        elif category == "Gameplay Data":
            st.markdown("- Progress tracking and achievements")
            st.markdown("- Game balancing and improvement")
            st.markdown("- Personalized content recommendations")
        elif category == "Location Data":
            st.markdown("- Regional content and pricing")
            st.markdown("- Fraud prevention and security")
            st.markdown("- Local regulations compliance")
        elif category == "Communication":
            st.markdown("- Enable player interaction")
            st.markdown("- Moderation and safety")
            st.markdown("- Social features and friend systems")
        elif category == "Biometric Data":
            st.markdown("- VR/AR experience optimization")
            st.markdown("- Motion controls and interaction")
            st.markdown("- Health and safety monitoring")

# Data sharing and third parties
st.subheader("🤝 Data Sharing and Third Parties")

sharing_info = {
    "Analytics Providers": ["Google Analytics", "Facebook Analytics", "Custom Analytics"],
    "Advertising Networks": ["AdMob", "Unity Ads", "Facebook Audience Network"],
    "Cloud Services": ["AWS", "Google Cloud", "Microsoft Azure"],
    "Social Platforms": ["Facebook", "Twitter", "Discord"],
    "Payment Processors": ["Stripe", "PayPal", "App Store/Play Store"]
}

for partner_type, partners in sharing_info.items():
    with st.expander(f"📤 {partner_type}"):
        st.markdown("**Typical Partners:**")
        for partner in partners:
            st.markdown(f"• {partner}")
        
        st.markdown("**Data Typically Shared:**")
        if partner_type == "Analytics Providers":
            st.markdown("- Usage statistics and behavior patterns")
            st.markdown("- Device and technical information")
            st.markdown("- Performance and crash data")
        elif partner_type == "Advertising Networks":
            st.markdown("- Device identifiers and demographics")
            st.markdown("- Usage patterns and preferences")
            st.markdown("- Location data (if available)")
        elif partner_type == "Cloud Services":
            st.markdown("- Game save data and progress")
            st.markdown("- User-generated content")
            st.markdown("- Technical logs and metrics")

# Privacy controls simulation
st.subheader("⚙️ Privacy Controls Simulation")

st.markdown("**Try adjusting these privacy settings:**")

col1, col2, col3 = st.columns(3)

with col1:
    data_collection = st.selectbox(
        "Data Collection Level",
        ["Minimal", "Standard", "Enhanced", "Full"]
    )
    
    analytics_sharing = st.checkbox("Share Analytics Data", value=True)
    
    location_tracking = st.checkbox("Enable Location Tracking", value=False)

with col2:
    ad_personalization = st.checkbox("Personalized Ads", value=True)
    
    social_features = st.checkbox("Social Features", value=True)
    
    communication_logs = st.checkbox("Store Communication Logs", value=True)

with col3:
    third_party_sharing = st.selectbox(
        "Third-Party Data Sharing",
        ["Disabled", "Essential Only", "Marketing Partners", "All Partners"]
    )
    
    data_retention = st.selectbox(
        "Data Retention Period",
        ["6 months", "1 year", "2 years", "Indefinite"]
    )

# Show impact of choices
if st.button("🔍 See Impact of Your Choices"):
    st.markdown("---")
    st.subheader("📈 Impact Analysis")
    
    # Calculate privacy score based on choices
    privacy_score = 100
    
    if data_collection == "Full":
        privacy_score -= 25
    elif data_collection == "Enhanced":
        privacy_score -= 15
    elif data_collection == "Standard":
        privacy_score -= 10
    
    if analytics_sharing:
        privacy_score -= 10
    if location_tracking:
        privacy_score -= 20
    if ad_personalization:
        privacy_score -= 15
    if communication_logs:
        privacy_score -= 10
    
    if third_party_sharing == "All Partners":
        privacy_score -= 20
    elif third_party_sharing == "Marketing Partners":
        privacy_score -= 15
    elif third_party_sharing == "Essential Only":
        privacy_score -= 5
    
    if data_retention == "Indefinite":
        privacy_score -= 15
    elif data_retention == "2 years":
        privacy_score -= 10
    elif data_retention == "1 year":
        privacy_score -= 5
    
    privacy_score = max(0, privacy_score)
    
    col1, col2 = st.columns(2)
    
    with col1:
        if privacy_score >= 80:
            st.success(f"🛡️ High Privacy Protection: {privacy_score}/100")
        elif privacy_score >= 60:
            st.warning(f"⚠️ Medium Privacy Protection: {privacy_score}/100")
        else:
            st.error(f"🚨 Low Privacy Protection: {privacy_score}/100")
    
    with col2:
        # Show what data is still being collected
        active_collection = []
        if data_collection != "Minimal":
            active_collection.extend(["Basic Usage Data", "Device Information"])
        if analytics_sharing:
            active_collection.append("Analytics Data")
        if location_tracking:
            active_collection.append("Location Data")
        if communication_logs:
            active_collection.append("Communication Logs")
        
        st.markdown("**Data Still Being Collected:**")
        for item in active_collection:
            st.markdown(f"• {item}")

# Back to dashboard
if st.button("🏠 Back to Dashboard"):
    st.switch_page("app.py")
