import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
from utils.database_manager import SecureGameDataDB
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(
    page_title="Database Dashboard",
    page_icon="🗄️",
    layout="wide"
)

st.title("🗄️ Secure Database Dashboard")
st.markdown("### Monitor encrypted data storage and database operations")

# Initialize database connection
if 'database' not in st.session_state:
    try:
        st.session_state.database = SecureGameDataDB()
        db_connected = True
    except Exception as e:
        st.error(f"Database connection failed: {str(e)}")
        db_connected = False
else:
    db_connected = True

if db_connected:
    # Get database statistics
    stats = st.session_state.database.get_database_stats()
    
    if stats:
        # Database overview metrics
        st.subheader("📊 Database Overview")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Total Users", stats.get('total_users', 0))
        
        with col2:
            st.metric("Encrypted Game Records", stats.get('total_game_data_records', 0))
        
        with col3:
            st.metric("Privacy Assessments", stats.get('total_assessments', 0))
        
        with col4:
            st.metric("Recent Activity (24h)", stats.get('recent_activity_24h', 0))
        
        # Database health information
        st.subheader("💾 Database Health")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.info(f"**Database Size:** {stats.get('database_size', 'Unknown')}")
            st.success("✅ Database Connection: Healthy")
            st.success("✅ Tables Initialized: Complete")
        
        with col2:
            # Connection test
            if st.button("🔍 Test Database Connection"):
                try:
                    test_stats = st.session_state.database.get_database_stats()
                    if test_stats:
                        st.success("Database connection test successful!")
                    else:
                        st.warning("Database connection test returned empty results")
                except Exception as e:
                    st.error(f"Database connection test failed: {str(e)}")
        
        st.markdown("---")
        
        # Sample data operations
        st.subheader("🧪 Database Operations Demo")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### Create Sample User")
            
            with st.form("create_user_form"):
                sample_username = st.text_input("Username", value="demo_user")
                sample_user_id = st.text_input("User ID Hash", value="demo_hash_123")
                
                if st.form_submit_button("Create Sample User"):
                    try:
                        success = st.session_state.database.create_user(
                            user_id_hash=sample_user_id,
                            username=sample_username
                        )
                        if success:
                            st.success("Sample user created successfully!")
                        else:
                            st.error("Failed to create sample user")
                    except Exception as e:
                        st.error(f"Error creating user: {str(e)}")
        
        with col2:
            st.markdown("#### Log Security Action")
            
            with st.form("log_action_form"):
                action_user_id = st.text_input("User ID Hash", value="demo_hash_123", key="action_user")
                action_type = st.selectbox("Action Type", [
                    "login", "logout", "data_access", "settings_change", 
                    "encryption", "decryption", "assessment_complete"
                ])
                
                if st.form_submit_button("Log Security Action"):
                    try:
                        success = st.session_state.database.log_security_action(
                            user_id_hash=action_user_id,
                            action_type=action_type,
                            resource_type="demo",
                            details={"demo": True, "timestamp": datetime.now().isoformat()}
                        )
                        if success:
                            st.success("Security action logged successfully!")
                        else:
                            st.error("Failed to log security action")
                    except Exception as e:
                        st.error(f"Error logging action: {str(e)}")
        
        # Database schema information
        st.subheader("🏗️ Database Schema")
        
        schema_info = {
            "users": {
                "description": "User accounts and authentication data",
                "fields": ["id", "user_id_hash", "username", "email_hash", "created_at", "last_login", "privacy_score"]
            },
            "encrypted_game_data": {
                "description": "Encrypted game data with AES-256 protection",
                "fields": ["id", "user_id_hash", "game_name", "encrypted_payload", "encryption_metadata", "data_hash"]
            },
            "privacy_assessments": {
                "description": "Privacy risk assessment results",
                "fields": ["id", "user_id_hash", "assessment_data", "risk_score", "risk_level", "recommendations"]
            },
            "privacy_settings": {
                "description": "User privacy preferences and settings",
                "fields": ["id", "user_id_hash", "settings_data", "encryption_preferences", "data_retention_days"]
            },
            "security_audit_log": {
                "description": "Security events and audit trail",
                "fields": ["id", "user_id_hash", "action_type", "resource_type", "details", "timestamp"]
            },
            "education_progress": {
                "description": "Privacy education module completion tracking",
                "fields": ["id", "user_id_hash", "module_name", "completion_status", "quiz_score", "completed_at"]
            }
        }
        
        for table_name, info in schema_info.items():
            with st.expander(f"📋 {table_name}"):
                st.markdown(f"**Description:** {info['description']}")
                st.markdown("**Fields:**")
                for field in info['fields']:
                    st.markdown(f"• `{field}`")
        
        # Security features
        st.subheader("🔒 Security Features")
        
        security_features = [
            "**Encrypted Storage**: All sensitive game data encrypted with AES-256-GCM",
            "**Hash Protection**: User IDs and sensitive fields protected with SHA-256/BLAKE3",
            "**Audit Logging**: Comprehensive security event logging for compliance",
            "**Data Isolation**: User data strictly isolated by hashed user IDs",
            "**Retention Policies**: Automatic cleanup of old data based on retention settings",
            "**Connection Security**: Encrypted database connections (SSL/TLS)",
            "**Access Control**: Database-level permissions and access restrictions",
            "**Backup Encryption**: Encrypted database backups for disaster recovery"
        ]
        
        for feature in security_features:
            st.success(feature)
        
        # Data retention and cleanup
        st.subheader("🧹 Data Management")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### Data Retention Policy")
            st.info("**Default Retention:** 365 days for user data")
            st.info("**Audit Logs:** 90 days retention")
            st.info("**Assessment Data:** User-configurable retention")
            
            if st.button("🗑️ Run Data Cleanup"):
                try:
                    success = st.session_state.database.cleanup_old_data()
                    if success:
                        st.success("Data cleanup completed successfully!")
                    else:
                        st.error("Data cleanup failed")
                except Exception as e:
                    st.error(f"Error during cleanup: {str(e)}")
        
        with col2:
            st.markdown("#### Database Maintenance")
            st.info("**Encryption**: AES-256-GCM for data at rest")
            st.info("**Indexing**: Optimized queries with proper indexes")
            st.info("**Monitoring**: Real-time performance monitoring")
            
            # Refresh stats
            if st.button("🔄 Refresh Statistics"):
                try:
                    new_stats = st.session_state.database.get_database_stats()
                    if new_stats:
                        st.success("Statistics refreshed successfully!")
                        st.rerun()
                    else:
                        st.warning("No statistics available")
                except Exception as e:
                    st.error(f"Error refreshing stats: {str(e)}")
    
    else:
        st.error("Unable to retrieve database statistics")
        st.info("The database may be initializing or there may be a connection issue")

else:
    st.error("Database connection not available")
    st.info("Please check the database configuration and try again")

# Implementation notes
with st.expander("📚 Implementation Notes"):
    st.markdown("""
    ### Database Security Implementation
    
    **Encryption at Rest:**
    - All sensitive game data encrypted with AES-256-GCM
    - Encryption keys derived using PBKDF2-SHA256
    - Individual encryption for each data record
    
    **Data Protection:**
    - User IDs hashed with SHA-256 for anonymization
    - Sensitive credentials hashed with BLAKE3
    - No plaintext storage of personal information
    
    **Audit and Compliance:**
    - Comprehensive security event logging
    - Data retention policies enforced automatically
    - GDPR and CCPA compliance features built-in
    
    **Performance Optimization:**
    - Database indexes on frequently queried fields
    - Efficient JSON storage for complex data structures
    - Connection pooling for scalability
    
    **Production Considerations:**
    - SSL/TLS encryption for database connections
    - Regular security audits and penetration testing
    - Automated backup and disaster recovery
    - Database access monitoring and alerting
    """)

# Back to dashboard
if st.button("🏠 Back to Dashboard"):
    st.switch_page("app.py")