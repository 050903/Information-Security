import streamlit as st
import plotly.express as px
from utils.education_content import get_education_modules, get_quiz_questions

st.set_page_config(
    page_title="Privacy Education",
    page_icon="📚",
    layout="wide"
)

st.title("📚 Gaming Privacy Education Center")
st.markdown("### Learn to protect your privacy while gaming")

# Initialize session state for progress tracking
if 'completed_modules' not in st.session_state:
    st.session_state.completed_modules = set()
if 'quiz_scores' not in st.session_state:
    st.session_state.quiz_scores = {}
if 'current_module' not in st.session_state:
    st.session_state.current_module = None

# Get education modules
modules = get_education_modules()

# Progress overview
st.subheader("📊 Your Learning Progress")

col1, col2, col3 = st.columns(3)

with col1:
    completion_rate = len(st.session_state.completed_modules) / len(modules) * 100
    st.metric("Modules Completed", f"{len(st.session_state.completed_modules)}/{len(modules)}")

with col2:
    avg_score = sum(st.session_state.quiz_scores.values()) / len(st.session_state.quiz_scores) if st.session_state.quiz_scores else 0
    st.metric("Average Quiz Score", f"{avg_score:.1f}%")

with col3:
    st.metric("Learning Level", "Beginner" if completion_rate < 50 else "Intermediate" if completion_rate < 80 else "Advanced")

# Progress bar
progress_bar = st.progress(completion_rate / 100)
st.markdown(f"**Overall Progress: {completion_rate:.1f}%**")

st.markdown("---")

# Module selection
st.subheader("🎯 Choose a Learning Module")

module_names = list(modules.keys())
selected_module = st.selectbox("Select a module to learn:", module_names)

if selected_module:
    module = modules[selected_module]
    
    # Module header
    col1, col2 = st.columns([3, 1])
    
    with col1:
        st.markdown(f"## {module['icon']} {selected_module}")
        st.markdown(f"**{module['description']}**")
        
    with col2:
        difficulty_color = "🟢" if module['difficulty'] == "Beginner" else "🟡" if module['difficulty'] == "Intermediate" else "🔴"
        st.markdown(f"**Difficulty:** {difficulty_color} {module['difficulty']}")
        st.markdown(f"**Duration:** ⏱️ {module['duration']}")
        
        if selected_module in st.session_state.completed_modules:
            st.success("✅ Completed")
        else:
            st.info("📖 Not started")
    
    st.markdown("---")
    
    # Module content tabs
    content_tab, quiz_tab, resources_tab = st.tabs(["📖 Content", "🧠 Quiz", "🔗 Resources"])
    
    with content_tab:
        st.markdown("### Learning Objectives")
        for objective in module['objectives']:
            st.markdown(f"• {objective}")
        
        st.markdown("### Content")
        
        # Display content sections
        for i, section in enumerate(module['content'], 1):
            with st.expander(f"Section {i}: {section['title']}", expanded=i==1):
                st.markdown(section['content'])
                
                # Interactive elements
                if 'interactive' in section:
                    if section['interactive']['type'] == 'checklist':
                        st.markdown("**✅ Interactive Checklist:**")
                        for item in section['interactive']['items']:
                            st.checkbox(item, key=f"{selected_module}_check_{i}_{item}")
                    
                    elif section['interactive']['type'] == 'scenario':
                        st.markdown("**🎭 Scenario Practice:**")
                        st.info(section['interactive']['scenario'])
                        
                        choice = st.radio(
                            "What would you do?",
                            section['interactive']['choices'],
                            key=f"{selected_module}_scenario_{i}"
                        )
                        
                        if st.button(f"Check Answer", key=f"{selected_module}_answer_{i}"):
                            if choice == section['interactive']['correct']:
                                st.success("✅ Correct! " + section['interactive']['explanation'])
                            else:
                                st.error("❌ " + section['interactive']['explanation'])
        
        # Mark as completed button
        if st.button("✅ Mark Module as Completed", type="primary", use_container_width=True):
            st.session_state.completed_modules.add(selected_module)
            st.success(f"Module '{selected_module}' marked as completed!")
            st.rerun()
    
    with quiz_tab:
        st.markdown("### 🧠 Knowledge Quiz")
        
        if selected_module in st.session_state.quiz_scores:
            st.info(f"Previous score: {st.session_state.quiz_scores[selected_module]}%")
        
        quiz_questions = get_quiz_questions(selected_module)
        
        if quiz_questions:
            with st.form(f"quiz_{selected_module}"):
                answers = {}
                
                for i, question in enumerate(quiz_questions):
                    st.markdown(f"**Question {i+1}:** {question['question']}")
                    
                    if question['type'] == 'multiple_choice':
                        answers[i] = st.radio(
                            "Select your answer:",
                            question['options'],
                            key=f"q_{i}"
                        )
                    elif question['type'] == 'true_false':
                        answers[i] = st.radio(
                            "True or False?",
                            ["True", "False"],
                            key=f"q_{i}"
                        )
                    
                    st.markdown("---")
                
                if st.form_submit_button("📊 Submit Quiz", use_container_width=True):
                    score = 0
                    total = len(quiz_questions)
                    
                    for i, question in enumerate(quiz_questions):
                        if answers[i] == question['correct']:
                            score += 1
                    
                    percentage = (score / total) * 100
                    st.session_state.quiz_scores[selected_module] = percentage
                    
                    if percentage >= 80:
                        st.success(f"🎉 Excellent! You scored {score}/{total} ({percentage:.1f}%)")
                    elif percentage >= 60:
                        st.warning(f"👍 Good job! You scored {score}/{total} ({percentage:.1f}%)")
                    else:
                        st.error(f"📚 Keep studying! You scored {score}/{total} ({percentage:.1f}%)")
                    
                    # Show correct answers
                    st.markdown("### 📝 Answer Review")
                    for i, question in enumerate(quiz_questions):
                        if answers[i] == question['correct']:
                            st.success(f"Q{i+1}: ✅ Correct")
                        else:
                            st.error(f"Q{i+1}: ❌ Correct answer: {question['correct']}")
                            st.markdown(f"*Explanation: {question.get('explanation', 'No explanation available')}*")
        else:
            st.info("Quiz coming soon for this module!")
    
    with resources_tab:
        st.markdown("### 📚 Additional Resources")
        
        if 'resources' in module:
            for resource in module['resources']:
                with st.expander(f"{resource['type']} - {resource['title']}"):
                    st.markdown(resource['description'])
                    if 'url' in resource:
                        st.markdown(f"[Learn More]({resource['url']})")
        
        st.markdown("### 🔗 External Links")
        st.markdown("""
        - [Privacy Rights Organizations](https://www.eff.org/)
        - [Gaming Privacy Guidelines](https://www.esrb.org/privacy/)
        - [Data Protection Resources](https://gdpr.eu/)
        - [Cybersecurity for Gamers](https://www.cisa.gov/cybersecurity)
        """)
        
        st.markdown("### 📖 Recommended Reading")
        st.markdown("""
        - "The Age of Surveillance Capitalism" by Shoshana Zuboff
        - "Weapons of Math Destruction" by Cathy O'Neil
        - "Privacy's Blueprint" by Woodrow Hartzog
        """)

# Learning path recommendations
st.markdown("---")
st.subheader("🛤️ Recommended Learning Path")

if completion_rate < 30:
    st.info("🌟 **For Beginners:** Start with 'Understanding Gaming Privacy' and 'Password Security'")
elif completion_rate < 70:
    st.info("🎯 **Next Steps:** Focus on 'Social Gaming Privacy' and 'Data Rights & Control'")
else:
    st.success("🏆 **Advanced:** Complete 'Emerging Threats' and consider helping others!")

# Achievements system
st.subheader("🏆 Privacy Learning Achievements")

achievements = []
if len(st.session_state.completed_modules) >= 1:
    achievements.append("🎯 First Steps - Completed your first module")
if len(st.session_state.completed_modules) >= 3:
    achievements.append("📚 Learning Momentum - Completed 3 modules")
if len(st.session_state.completed_modules) >= len(modules):
    achievements.append("🏆 Privacy Expert - Completed all modules")
if st.session_state.quiz_scores and max(st.session_state.quiz_scores.values()) >= 90:
    achievements.append("🧠 Quiz Master - Scored 90%+ on a quiz")

if achievements:
    for achievement in achievements:
        st.success(achievement)
else:
    st.info("Complete modules and quizzes to unlock achievements!")

# Back to dashboard
if st.button("🏠 Back to Dashboard"):
    st.switch_page("app.py")
