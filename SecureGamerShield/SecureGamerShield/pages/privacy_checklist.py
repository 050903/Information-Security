import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(
    page_title="Privacy Checklist",
    page_icon="📋",
    layout="wide"
)

st.title("📋 Gaming Privacy Checklist")
st.markdown("### Comprehensive privacy protection checklist for gamers")

# Initialize session state for checklist progress
if 'checklist_progress' not in st.session_state:
    st.session_state.checklist_progress = {}

# Checklist categories and items
checklist_categories = {
    "Account Security": {
        "icon": "🔐",
        "items": [
            {
                "task": "Enable two-factor authentication on all gaming accounts",
                "description": "Add an extra layer of security to your gaming accounts",
                "priority": "High",
                "effort": "Low"
            },
            {
                "task": "Use unique, strong passwords for each gaming platform",
                "description": "Prevent credential stuffing attacks and account takeovers",
                "priority": "High", 
                "effort": "Medium"
            },
            {
                "task": "Review and update recovery email addresses",
                "description": "Ensure you can recover your accounts if needed",
                "priority": "Medium",
                "effort": "Low"
            },
            {
                "task": "Check for account breaches using services like HaveIBeenPwned",
                "description": "See if your email has been involved in data breaches",
                "priority": "Medium",
                "effort": "Low"
            },
            {
                "task": "Enable login notifications and alerts",
                "description": "Get notified of suspicious login attempts",
                "priority": "Medium",
                "effort": "Low"
            }
        ]
    },
    "Platform Privacy Settings": {
        "icon": "⚙️",
        "items": [
            {
                "task": "Review privacy settings on Steam",
                "description": "Control who can see your profile, friends list, and game activity",
                "priority": "High",
                "effort": "Medium"
            },
            {
                "task": "Configure Xbox Live privacy settings",
                "description": "Manage communication, sharing, and visibility preferences",
                "priority": "High",
                "effort": "Medium"
            },
            {
                "task": "Adjust PlayStation Network privacy controls",
                "description": "Control friend requests, messages, and activity visibility",
                "priority": "High",
                "effort": "Medium"
            },
            {
                "task": "Set up Nintendo Switch parental controls (if applicable)",
                "description": "Manage communication and purchase restrictions",
                "priority": "Medium",
                "effort": "Medium"
            },
            {
                "task": "Review mobile gaming platform settings (iOS/Android)",
                "description": "Control app permissions and data sharing",
                "priority": "High",
                "effort": "Medium"
            }
        ]
    },
    "Communication Privacy": {
        "icon": "💬",
        "items": [
            {
                "task": "Configure voice chat privacy settings",
                "description": "Control who can hear you and when voice is recorded",
                "priority": "High",
                "effort": "Low"
            },
            {
                "task": "Review Discord privacy and safety settings",
                "description": "Manage DMs, friend requests, and data collection",
                "priority": "High",
                "effort": "Medium"
            },
            {
                "task": "Set up content filters and blocked words",
                "description": "Protect yourself from harassment and inappropriate content",
                "priority": "Medium",
                "effort": "Low"
            },
            {
                "task": "Limit friend requests to friends-of-friends only",
                "description": "Reduce spam and unwanted contact from strangers",
                "priority": "Medium",
                "effort": "Low"
            },
            {
                "task": "Review game-specific chat and communication settings",
                "description": "Each game may have unique privacy controls",
                "priority": "Medium",
                "effort": "High"
            }
        ]
    },
    "Data Collection Control": {
        "icon": "📊",
        "items": [
            {
                "task": "Opt out of analytics and telemetry data collection",
                "description": "Reduce the amount of behavioral data collected about you",
                "priority": "High",
                "effort": "Medium"
            },
            {
                "task": "Disable personalized advertising across gaming platforms",
                "description": "Prevent your gaming data from being used for targeted ads",
                "priority": "Medium",
                "effort": "Medium"
            },
            {
                "task": "Review and limit location data sharing",
                "description": "Control when and how games access your location",
                "priority": "High",
                "effort": "Medium"
            },
            {
                "task": "Turn off automatic crash reporting and diagnostics",
                "description": "Prevent automatic sharing of error data and system information",
                "priority": "Low",
                "effort": "Low"
            },
            {
                "task": "Review third-party data sharing agreements",
                "description": "Understand what data is shared with partners and advertisers",
                "priority": "Medium",
                "effort": "High"
            }
        ]
    },
    "Device & App Security": {
        "icon": "📱",
        "items": [
            {
                "task": "Keep gaming apps and operating system updated",
                "description": "Install security patches and privacy improvements",
                "priority": "High",
                "effort": "Low"
            },
            {
                "task": "Review and limit app permissions on mobile devices",
                "description": "Control access to camera, microphone, contacts, and location",
                "priority": "High",
                "effort": "Medium"
            },
            {
                "task": "Use device lock screens and biometric authentication",
                "description": "Protect your device if it's lost or stolen",
                "priority": "High",
                "effort": "Low"
            },
            {
                "task": "Install games only from official app stores",
                "description": "Avoid malware and unofficial apps that may compromise privacy",
                "priority": "High",
                "effort": "Low"
            },
            {
                "task": "Use a VPN for online gaming (if needed)",
                "description": "Protect your IP address and encrypt your connection",
                "priority": "Low",
                "effort": "Medium"
            }
        ]
    },
    "Social Media Integration": {
        "icon": "🔗",
        "items": [
            {
                "task": "Audit connected social media accounts",
                "description": "Review which social platforms are linked to your gaming accounts",
                "priority": "Medium",
                "effort": "Medium"
            },
            {
                "task": "Disable automatic sharing of gaming achievements",
                "description": "Control what gaming activity is posted to social media",
                "priority": "Medium",
                "effort": "Low"
            },
            {
                "task": "Review Facebook Gaming privacy settings",
                "description": "Control visibility of gaming activity on Facebook",
                "priority": "Medium",
                "effort": "Medium"
            },
            {
                "task": "Limit Twitter/X integration with gaming platforms",
                "description": "Control what gaming data is shared with Twitter",
                "priority": "Low",
                "effort": "Low"
            },
            {
                "task": "Remove unused social media connections",
                "description": "Disconnect old or unnecessary social media integrations",
                "priority": "Medium",
                "effort": "Low"
            }
        ]
    }
}

# Progress overview
total_items = sum(len(category["items"]) for category in checklist_categories.values())
completed_items = len([item for item in st.session_state.checklist_progress.values() if item])
completion_percentage = (completed_items / total_items) * 100 if total_items > 0 else 0

st.subheader("📊 Overall Progress")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Completed Tasks", f"{completed_items}/{total_items}")

with col2:
    st.metric("Completion Rate", f"{completion_percentage:.1f}%")

with col3:
    high_priority_completed = len([
        key for key, checked in st.session_state.checklist_progress.items() 
        if checked and "High" in key
    ])
    st.metric("High Priority Done", high_priority_completed)

with col4:
    if completion_percentage >= 80:
        st.success("🏆 Expert Level")
    elif completion_percentage >= 60:
        st.warning("🎯 Advanced Level")
    elif completion_percentage >= 40:
        st.info("📈 Intermediate Level")
    else:
        st.error("🌱 Beginner Level")

# Progress bar
st.progress(completion_percentage / 100)

st.markdown("---")

# Filter options
st.subheader("🔍 Filter Checklist")

col1, col2, col3 = st.columns(3)

with col1:
    show_completed = st.checkbox("Show completed tasks", value=True)

with col2:
    priority_filter = st.selectbox(
        "Filter by priority:",
        ["All", "High", "Medium", "Low"]
    )

with col3:
    effort_filter = st.selectbox(
        "Filter by effort level:",
        ["All", "Low", "Medium", "High"]
    )

st.markdown("---")

# Display checklist by category
for category_name, category_data in checklist_categories.items():
    st.subheader(f"{category_data['icon']} {category_name}")
    
    # Calculate category completion
    category_tasks = [f"{category_name}_{i}" for i in range(len(category_data['items']))]
    category_completed = len([
        task for task in category_tasks 
        if st.session_state.checklist_progress.get(task, False)
    ])
    category_total = len(category_data['items'])
    category_percentage = (category_completed / category_total) * 100 if category_total > 0 else 0
    
    st.progress(category_percentage / 100)
    st.markdown(f"**Progress: {category_completed}/{category_total} tasks completed ({category_percentage:.1f}%)**")
    
    # Display tasks
    for i, item in enumerate(category_data['items']):
        task_key = f"{category_name}_{i}"
        
        # Apply filters
        show_task = True
        
        if not show_completed and st.session_state.checklist_progress.get(task_key, False):
            show_task = False
        
        if priority_filter != "All" and item['priority'] != priority_filter:
            show_task = False
            
        if effort_filter != "All" and item['effort'] != effort_filter:
            show_task = False
        
        if show_task:
            col1, col2 = st.columns([1, 10])
            
            with col1:
                is_checked = st.checkbox(
                    "", 
                    value=st.session_state.checklist_progress.get(task_key, False),
                    key=task_key
                )
                st.session_state.checklist_progress[task_key] = is_checked
            
            with col2:
                if is_checked:
                    st.markdown(f"~~**{item['task']}**~~")
                    st.markdown(f"~~{item['description']}~~")
                else:
                    st.markdown(f"**{item['task']}**")
                    st.markdown(f"{item['description']}")
                
                # Priority and effort badges
                priority_color = "🔴" if item['priority'] == "High" else "🟡" if item['priority'] == "Medium" else "🟢"
                effort_color = "🔵" if item['effort'] == "Low" else "🟠" if item['effort'] == "Medium" else "🔴"
                
                st.markdown(f"{priority_color} **Priority:** {item['priority']} | {effort_color} **Effort:** {item['effort']}")
                st.markdown("---")

# Quick actions
st.subheader("⚡ Quick Actions")

col1, col2, col3 = st.columns(3)

with col1:
    if st.button("✅ Mark All High Priority as Done", use_container_width=True):
        for category_name, category_data in checklist_categories.items():
            for i, item in enumerate(category_data['items']):
                if item['priority'] == "High":
                    task_key = f"{category_name}_{i}"
                    st.session_state.checklist_progress[task_key] = True
        st.success("All high priority tasks marked as completed!")
        st.rerun()

with col2:
    if st.button("📋 Export Checklist", use_container_width=True):
        # Create exportable checklist
        export_data = []
        for category_name, category_data in checklist_categories.items():
            for i, item in enumerate(category_data['items']):
                task_key = f"{category_name}_{i}"
                export_data.append({
                    'Category': category_name,
                    'Task': item['task'],
                    'Description': item['description'],
                    'Priority': item['priority'],
                    'Effort': item['effort'],
                    'Completed': st.session_state.checklist_progress.get(task_key, False)
                })
        
        df = pd.DataFrame(export_data)
        csv = df.to_csv(index=False)
        
        st.download_button(
            label="Download CSV",
            data=csv,
            file_name=f"gaming_privacy_checklist_{datetime.now().strftime('%Y%m%d')}.csv",
            mime="text/csv"
        )

with col3:
    if st.button("🔄 Reset All Progress", use_container_width=True):
        st.session_state.checklist_progress = {}
        st.warning("All progress has been reset!")
        st.rerun()

# Achievements
st.subheader("🏆 Checklist Achievements")

achievements = []
if completed_items >= 5:
    achievements.append("🎯 Getting Started - Completed 5 tasks")
if completed_items >= 15:
    achievements.append("📈 Making Progress - Completed 15 tasks")
if completed_items >= 25:
    achievements.append("🎖️ Privacy Advocate - Completed 25 tasks")
if completion_percentage >= 100:
    achievements.append("🏆 Privacy Master - Completed all tasks")

high_priority_total = sum(
    len([item for item in category["items"] if item["priority"] == "High"])
    for category in checklist_categories.values()
)
high_priority_done = len([
    key for key, checked in st.session_state.checklist_progress.items() 
    if checked and any(
        key.startswith(cat_name) and 
        checklist_categories[cat_name]["items"][int(key.split("_")[-1])]["priority"] == "High"
        for cat_name in checklist_categories.keys()
        if key.startswith(cat_name) and key.split("_")[-1].isdigit()
    )
])

if high_priority_done >= high_priority_total and high_priority_total > 0:
    achievements.append("🔴 High Priority Hero - Completed all high priority tasks")

if achievements:
    for achievement in achievements:
        st.success(achievement)
else:
    st.info("Complete tasks to unlock achievements!")

# Back to dashboard
if st.button("🏠 Back to Dashboard"):
    st.switch_page("app.py")
