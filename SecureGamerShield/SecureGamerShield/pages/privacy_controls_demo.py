import streamlit as st
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(
    page_title="Privacy Controls Demo",
    page_icon="🎛️",
    layout="wide"
)

st.title("🎛️ Privacy Controls Demonstration")
st.markdown("### Interactive demo of gaming privacy settings and their impact")

# Initialize demo state
if 'demo_settings' not in st.session_state:
    st.session_state.demo_settings = {
        'profile_visibility': 'Public',
        'friend_requests': 'Everyone',
        'voice_chat': 'All Players',
        'location_sharing': True,
        'analytics_opt_in': True,
        'ad_personalization': True,
        'social_media_sharing': True,
        'data_retention': 'Indefinite',
        'third_party_sharing': 'All Partners'
    }

# Gaming platform selector
st.subheader("🎮 Choose Gaming Platform to Configure")

platform = st.selectbox(
    "Select a gaming platform:",
    ["Steam", "Xbox Live", "PlayStation Network", "Nintendo Switch Online", "Mobile Gaming App", "Discord"]
)

st.markdown(f"### {platform} Privacy Settings Demo")

# Create tabs for different privacy areas
privacy_tab, impact_tab, comparison_tab = st.tabs(["⚙️ Privacy Settings", "📊 Privacy Impact", "🔍 Before/After"])

with privacy_tab:
    st.markdown("#### Configure Your Privacy Settings")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**Profile & Visibility**")
        
        st.session_state.demo_settings['profile_visibility'] = st.selectbox(
            "Profile Visibility",
            ["Private", "Friends Only", "Friends of Friends", "Public"],
            index=["Private", "Friends Only", "Friends of Friends", "Public"].index(
                st.session_state.demo_settings['profile_visibility']
            )
        )
        
        st.session_state.demo_settings['friend_requests'] = st.selectbox(
            "Friend Requests From",
            ["No One", "Friends of Friends", "Everyone"],
            index=["No One", "Friends of Friends", "Everyone"].index(
                st.session_state.demo_settings['friend_requests']
            )
        )
        
        st.session_state.demo_settings['voice_chat'] = st.selectbox(
            "Voice Chat With",
            ["No One", "Friends Only", "Friends & Groups", "All Players"],
            index=["No One", "Friends Only", "Friends & Groups", "All Players"].index(
                st.session_state.demo_settings['voice_chat']
            )
        )
        
        st.markdown("**Data Collection**")
        
        st.session_state.demo_settings['location_sharing'] = st.checkbox(
            "Share Location Data",
            value=st.session_state.demo_settings['location_sharing']
        )
        
        st.session_state.demo_settings['analytics_opt_in'] = st.checkbox(
            "Analytics Data Collection",
            value=st.session_state.demo_settings['analytics_opt_in']
        )
    
    with col2:
        st.markdown("**Advertising & Social**")
        
        st.session_state.demo_settings['ad_personalization'] = st.checkbox(
            "Personalized Advertisements",
            value=st.session_state.demo_settings['ad_personalization']
        )
        
        st.session_state.demo_settings['social_media_sharing'] = st.checkbox(
            "Automatic Social Media Sharing",
            value=st.session_state.demo_settings['social_media_sharing']
        )
        
        st.markdown("**Data Management**")
        
        st.session_state.demo_settings['data_retention'] = st.selectbox(
            "Data Retention Period",
            ["6 months", "1 year", "2 years", "5 years", "Indefinite"],
            index=["6 months", "1 year", "2 years", "5 years", "Indefinite"].index(
                st.session_state.demo_settings['data_retention']
            )
        )
        
        st.session_state.demo_settings['third_party_sharing'] = st.selectbox(
            "Third-Party Data Sharing",
            ["None", "Essential Only", "Marketing Partners", "All Partners"],
            index=["None", "Essential Only", "Marketing Partners", "All Partners"].index(
                st.session_state.demo_settings['third_party_sharing']
            )
        )

with impact_tab:
    st.markdown("#### Real-Time Privacy Impact Analysis")
    
    # Calculate privacy score based on settings
    def calculate_privacy_impact(settings):
        score = 100
        
        # Profile visibility impact
        if settings['profile_visibility'] == 'Public':
            score -= 25
        elif settings['profile_visibility'] == 'Friends of Friends':
            score -= 15
        elif settings['profile_visibility'] == 'Friends Only':
            score -= 5
        
        # Friend requests impact
        if settings['friend_requests'] == 'Everyone':
            score -= 15
        elif settings['friend_requests'] == 'Friends of Friends':
            score -= 8
        
        # Voice chat impact
        if settings['voice_chat'] == 'All Players':
            score -= 20
        elif settings['voice_chat'] == 'Friends & Groups':
            score -= 10
        elif settings['voice_chat'] == 'Friends Only':
            score -= 5
        
        # Data collection impacts
        if settings['location_sharing']:
            score -= 15
        if settings['analytics_opt_in']:
            score -= 10
        if settings['ad_personalization']:
            score -= 10
        if settings['social_media_sharing']:
            score -= 8
        
        # Data retention impact
        retention_penalties = {
            'Indefinite': 15,
            '5 years': 12,
            '2 years': 8,
            '1 year': 4,
            '6 months': 0
        }
        score -= retention_penalties.get(settings['data_retention'], 0)
        
        # Third-party sharing impact
        sharing_penalties = {
            'All Partners': 20,
            'Marketing Partners': 15,
            'Essential Only': 5,
            'None': 0
        }
        score -= sharing_penalties.get(settings['third_party_sharing'], 0)
        
        return max(0, score)
    
    current_score = calculate_privacy_impact(st.session_state.demo_settings)
    
    # Display current impact
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if current_score >= 80:
            st.success(f"**Privacy Score: {current_score}/100**")
            st.markdown("🛡️ **High Protection**")
        elif current_score >= 60:
            st.warning(f"**Privacy Score: {current_score}/100**")
            st.markdown("⚠️ **Medium Protection**")
        else:
            st.error(f"**Privacy Score: {current_score}/100**")
            st.markdown("🚨 **Low Protection**")
    
    with col2:
        # Risk categories
        risks = []
        if st.session_state.demo_settings['profile_visibility'] == 'Public':
            risks.append("Public Profile Exposure")
        if st.session_state.demo_settings['location_sharing']:
            risks.append("Location Tracking")
        if st.session_state.demo_settings['voice_chat'] == 'All Players':
            risks.append("Communication with Strangers")
        if st.session_state.demo_settings['third_party_sharing'] == 'All Partners':
            risks.append("Extensive Data Sharing")
        
        st.markdown("**Current Risks:**")
        if risks:
            for risk in risks:
                st.markdown(f"🔴 {risk}")
        else:
            st.success("🟢 Minimal Privacy Risks")
    
    with col3:
        # Data collection summary
        collected_data = []
        if st.session_state.demo_settings['analytics_opt_in']:
            collected_data.append("Behavioral Analytics")
        if st.session_state.demo_settings['location_sharing']:
            collected_data.append("Location Data")
        if st.session_state.demo_settings['ad_personalization']:
            collected_data.append("Advertising Profile")
        if st.session_state.demo_settings['social_media_sharing']:
            collected_data.append("Social Media Activity")
        
        st.markdown("**Data Being Collected:**")
        if collected_data:
            for data in collected_data:
                st.markdown(f"📊 {data}")
        else:
            st.success("📊 Minimal Data Collection")
    
    # Impact visualization
    st.markdown("#### Privacy Protection Breakdown")
    
    # Create radar chart
    categories = [
        'Profile Privacy',
        'Communication Security', 
        'Data Collection Control',
        'Social Media Privacy',
        'Third-Party Sharing'
    ]
    
    # Calculate scores for each category
    profile_score = 100 - (25 if st.session_state.demo_settings['profile_visibility'] == 'Public' else 
                          15 if st.session_state.demo_settings['profile_visibility'] == 'Friends of Friends' else
                          5 if st.session_state.demo_settings['profile_visibility'] == 'Friends Only' else 0)
    
    comm_score = 100 - (20 if st.session_state.demo_settings['voice_chat'] == 'All Players' else
                        10 if st.session_state.demo_settings['voice_chat'] == 'Friends & Groups' else
                        5 if st.session_state.demo_settings['voice_chat'] == 'Friends Only' else 0)
    
    data_score = 100 - (15 if st.session_state.demo_settings['location_sharing'] else 0) - \
                      (10 if st.session_state.demo_settings['analytics_opt_in'] else 0)
    
    social_score = 100 - (10 if st.session_state.demo_settings['ad_personalization'] else 0) - \
                        (8 if st.session_state.demo_settings['social_media_sharing'] else 0)
    
    sharing_penalties = {
        'All Partners': 20,
        'Marketing Partners': 15,
        'Essential Only': 5,
        'None': 0
    }
    sharing_score = 100 - sharing_penalties.get(st.session_state.demo_settings['third_party_sharing'], 0)
    
    scores = [profile_score, comm_score, data_score, social_score, sharing_score]
    
    fig = go.Figure(data=go.Scatterpolar(
        r=scores,
        theta=categories,
        fill='toself',
        name='Current Settings'
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

with comparison_tab:
    st.markdown("#### Before vs After Comparison")
    
    # Show different privacy presets
    st.markdown("**Compare with Privacy Presets:**")
    
    preset = st.selectbox(
        "Choose a preset to compare:",
        ["Maximum Privacy", "Balanced Privacy", "Default Settings", "Minimal Privacy"]
    )
    
    # Define presets
    presets = {
        "Maximum Privacy": {
            'profile_visibility': 'Private',
            'friend_requests': 'No One',
            'voice_chat': 'Friends Only',
            'location_sharing': False,
            'analytics_opt_in': False,
            'ad_personalization': False,
            'social_media_sharing': False,
            'data_retention': '6 months',
            'third_party_sharing': 'None'
        },
        "Balanced Privacy": {
            'profile_visibility': 'Friends Only',
            'friend_requests': 'Friends of Friends',
            'voice_chat': 'Friends & Groups',
            'location_sharing': False,
            'analytics_opt_in': True,
            'ad_personalization': False,
            'social_media_sharing': False,
            'data_retention': '1 year',
            'third_party_sharing': 'Essential Only'
        },
        "Default Settings": {
            'profile_visibility': 'Friends of Friends',
            'friend_requests': 'Everyone',
            'voice_chat': 'All Players',
            'location_sharing': True,
            'analytics_opt_in': True,
            'ad_personalization': True,
            'social_media_sharing': True,
            'data_retention': '2 years',
            'third_party_sharing': 'Marketing Partners'
        },
        "Minimal Privacy": {
            'profile_visibility': 'Public',
            'friend_requests': 'Everyone',
            'voice_chat': 'All Players',
            'location_sharing': True,
            'analytics_opt_in': True,
            'ad_personalization': True,
            'social_media_sharing': True,
            'data_retention': 'Indefinite',
            'third_party_sharing': 'All Partners'
        }
    }
    
    preset_settings = presets[preset]
    preset_score = calculate_privacy_impact(preset_settings)
    
    # Comparison visualization
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**Your Current Settings**")
        st.metric("Privacy Score", f"{current_score}/100")
        
        # Show key differences
        st.markdown("**Key Settings:**")
        st.markdown(f"• Profile: {st.session_state.demo_settings['profile_visibility']}")
        st.markdown(f"• Voice Chat: {st.session_state.demo_settings['voice_chat']}")
        st.markdown(f"• Location: {'Enabled' if st.session_state.demo_settings['location_sharing'] else 'Disabled'}")
        st.markdown(f"• Analytics: {'Enabled' if st.session_state.demo_settings['analytics_opt_in'] else 'Disabled'}")
        st.markdown(f"• Third-party: {st.session_state.demo_settings['third_party_sharing']}")
    
    with col2:
        st.markdown(f"**{preset} Preset**")
        
        score_diff = preset_score - current_score
        st.metric("Privacy Score", f"{preset_score}/100", delta=f"{score_diff:+}")
        
        st.markdown("**Key Settings:**")
        st.markdown(f"• Profile: {preset_settings['profile_visibility']}")
        st.markdown(f"• Voice Chat: {preset_settings['voice_chat']}")
        st.markdown(f"• Location: {'Enabled' if preset_settings['location_sharing'] else 'Disabled'}")
        st.markdown(f"• Analytics: {'Enabled' if preset_settings['analytics_opt_in'] else 'Disabled'}")
        st.markdown(f"• Third-party: {preset_settings['third_party_sharing']}")
    
    # Apply preset button
    if st.button(f"🔄 Apply {preset} Settings", use_container_width=True, type="primary"):
        st.session_state.demo_settings = preset_settings.copy()
        st.success(f"{preset} settings applied!")
        st.rerun()
    
    # Show what changes
    st.markdown("#### What Would Change?")
    
    changes = []
    for key, value in preset_settings.items():
        if st.session_state.demo_settings[key] != value:
            current_val = st.session_state.demo_settings[key]
            changes.append(f"• {key.replace('_', ' ').title()}: {current_val} → {value}")
    
    if changes:
        st.markdown("**Settings that would change:**")
        for change in changes:
            st.markdown(change)
    else:
        st.success("Your settings already match this preset!")

# Quick recommendations
st.subheader("💡 Personalized Recommendations")

recommendations = []

if st.session_state.demo_settings['profile_visibility'] == 'Public':
    recommendations.append({
        'title': 'Make Profile Private',
        'description': 'Change profile visibility to "Friends Only" to reduce exposure',
        'impact': '+15 privacy points'
    })

if st.session_state.demo_settings['location_sharing']:
    recommendations.append({
        'title': 'Disable Location Sharing',
        'description': 'Turn off location data sharing to protect your physical privacy',
        'impact': '+15 privacy points'
    })

if st.session_state.demo_settings['third_party_sharing'] == 'All Partners':
    recommendations.append({
        'title': 'Limit Third-Party Sharing',
        'description': 'Change to "Essential Only" to reduce data sharing with external companies',
        'impact': '+15 privacy points'
    })

if st.session_state.demo_settings['voice_chat'] == 'All Players':
    recommendations.append({
        'title': 'Restrict Voice Chat',
        'description': 'Limit voice chat to "Friends Only" for better communication privacy',
        'impact': '+15 privacy points'
    })

if recommendations:
    for i, rec in enumerate(recommendations[:3]):  # Show top 3 recommendations
        with st.expander(f"Recommendation {i+1}: {rec['title']}"):
            st.markdown(rec['description'])
            st.success(rec['impact'])
else:
    st.success("🎉 Your privacy settings look great! No immediate recommendations.")

# Back to dashboard
if st.button("🏠 Back to Dashboard"):
    st.switch_page("app.py")
