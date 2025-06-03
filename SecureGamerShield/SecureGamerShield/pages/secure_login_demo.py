import streamlit as st
import json
from datetime import datetime
from utils.encryption_manager import GameDataSecurityManager, EncryptionManager
from utils.database_manager import SecureGameDataDB

st.set_page_config(
    page_title="Secure Login & Encryption Demo",
    page_icon="🔐",
    layout="wide"
)

st.title("🔐 Secure Game Data Encryption Demo")
st.markdown("### Experience AES-256 encryption and BLAKE3/SHA-256 hashing for gaming data")

# Initialize session state
if 'security_manager' not in st.session_state:
    st.session_state.security_manager = GameDataSecurityManager()
if 'database' not in st.session_state:
    st.session_state.database = SecureGameDataDB()
if 'encrypted_session_data' not in st.session_state:
    st.session_state.encrypted_session_data = None
if 'login_successful' not in st.session_state:
    st.session_state.login_successful = False

# Create tabs for different security demonstrations
demo_tab, encryption_tab, verification_tab = st.tabs(["🔐 Secure Login", "🛡️ Encryption Details", "✅ Verification"])

with demo_tab:
    st.subheader("Secure Login Flow Demonstration")
    
    st.markdown("""
    **This demo simulates the complete secure login process:**
    1. **Login**: User authentication
    2. **Game Detection**: Identify currently playing game
    3. **Data Retrieval**: Collect game-related user data
    4. **Encryption**: Apply AES-256 encryption
    5. **Hashing**: Use SHA-256/BLAKE3 for sensitive fields
    6. **Secure Storage**: Return encrypted data safely
    """)
    
    # Login form
    with st.form("secure_login_form"):
        st.markdown("#### User Login")
        
        col1, col2 = st.columns(2)
        
        with col1:
            user_id = st.text_input("User ID", value="gamer_user_123", help="Enter your gaming user ID")
            
        with col2:
            password = st.text_input("Password", type="password", value="SecureGamePass2024!", help="Enter your secure password")
        
        # Game selection (simulating detection)
        detected_game = st.selectbox(
            "Currently Playing Game (Auto-detected)",
            ["Valorant", "League of Legends", "Fortnite", "Minecraft", "Among Us", "Call of Duty", "Apex Legends", "Rocket League"],
            help="In production, this would be automatically detected"
        )
        
        submitted = st.form_submit_button("🔐 Secure Login & Encrypt Data", use_container_width=True, type="primary")
    
    if submitted and user_id and password:
        with st.spinner("Processing secure login..."):
            try:
                # Simulate the complete secure login flow
                secure_response = st.session_state.security_manager.secure_login_flow(user_id, password)
                
                if secure_response['status'] == 'success':
                    st.session_state.encrypted_session_data = secure_response
                    st.session_state.login_successful = True
                    
                    # Store in database
                    user_id_hash = secure_response['user_id_hash']
                    encrypted_data = secure_response['encrypted_data']
                    
                    # Create user record
                    st.session_state.database.create_user(
                        user_id_hash=user_id_hash,
                        username=user_id,
                        email_hash=""
                    )
                    
                    # Store encrypted game data
                    data_stored = st.session_state.database.store_encrypted_game_data(
                        user_id_hash=user_id_hash,
                        game_name=detected_game,
                        encrypted_data=encrypted_data,
                        data_hash=user_id_hash[:32]  # Using truncated hash as example
                    )
                    
                    # Log security action
                    st.session_state.database.log_security_action(
                        user_id_hash=user_id_hash,
                        action_type="secure_login",
                        resource_type="game_data",
                        details={
                            "game": detected_game,
                            "encryption_algorithm": encrypted_data['algorithm'],
                            "data_stored": data_stored
                        }
                    )
                    
                    st.success("🎉 Secure login successful! Data encrypted and stored securely in database.")
                    
                    # Display security summary
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        st.metric("Security Level", secure_response['security_info']['security_level'].upper())
                        
                    with col2:
                        st.metric("Encryption Algorithm", secure_response['security_info']['encryption_algorithm'])
                    
                    with col3:
                        st.metric("Key Strength", secure_response['data_summary']['encryption_key_strength'])
                    
                    # Show what was secured
                    st.subheader("🛡️ Security Operations Completed")
                    
                    security_info = secure_response['security_info']
                    data_summary = secure_response['data_summary']
                    
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.markdown("**Encryption Applied:**")
                        st.info(f"✅ {data_summary['total_fields_encrypted']} data fields encrypted with AES-256-GCM")
                        st.info(f"✅ {data_summary['sensitive_fields_hashed']} sensitive fields hashed with BLAKE3")
                        st.info(f"✅ User ID hashed with SHA-256")
                        
                    with col2:
                        st.markdown("**Security Features:**")
                        st.success(f"🔐 {data_summary['authentication_method']} key derivation")
                        st.success(f"🛡️ {security_info['encryption_algorithm']} encryption")
                        st.success(f"🔒 256-bit encryption keys")
                    
                else:
                    st.error(f"Login failed: {secure_response.get('error_message', 'Unknown error')}")
                    st.session_state.login_successful = False
                    
            except Exception as e:
                st.error(f"Security operation failed: {str(e)}")
                st.session_state.login_successful = False

with encryption_tab:
    st.subheader("🔍 Encryption Implementation Details")
    
    if st.session_state.login_successful and st.session_state.encrypted_session_data:
        encrypted_data = st.session_state.encrypted_session_data['encrypted_data']
        
        st.markdown("#### Encrypted Data Structure")
        
        # Show encrypted data (safe to display)
        display_data = {
            'algorithm': encrypted_data['algorithm'],
            'encryption_method': encrypted_data['encryption_method'],
            'timestamp': encrypted_data['timestamp'],
            'user_id_hash': encrypted_data['user_id_hash'][:16] + "...",  # Truncate for display
            'ciphertext_length': len(encrypted_data['ciphertext']),
            'salt_length': len(encrypted_data['salt']),
            'iv_length': len(encrypted_data['iv'])
        }
        
        st.json(display_data)
        
        # Technical details
        st.markdown("#### 🔧 Technical Implementation")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**AES-256-GCM Encryption:**")
            st.code("""
# Key derivation using PBKDF2-SHA256
kdf = PBKDF2HMAC(
    algorithm=hashes.SHA256(),
    length=32,  # 256 bits
    salt=salt,
    iterations=100000
)

# AES-256-GCM for authenticated encryption
cipher = Cipher(
    algorithms.AES(key),
    modes.GCM(iv),
    backend=default_backend()
)
            """, language="python")
        
        with col2:
            st.markdown("**BLAKE3 Hashing:**")
            st.code("""
# BLAKE3 for sensitive data hashing
hash_input = (data + salt).encode()
hash_digest = blake3.blake3(hash_input).hexdigest()

# SHA-256 for user ID hashing
hash_input = (user_id + salt).encode()
sha256_hash = hashlib.sha256(hash_input).hexdigest()
            """, language="python")
        
        # Security features breakdown
        st.markdown("#### 🛡️ Security Features")
        
        features = [
            "**Authenticated Encryption**: AES-256-GCM provides both confidentiality and integrity",
            "**Key Stretching**: PBKDF2 with 100,000 iterations prevents brute force attacks",
            "**Random IV**: Each encryption uses a unique initialization vector",
            "**Salt Protection**: Random salts prevent rainbow table attacks",
            "**Hash Security**: BLAKE3 and SHA-256 for irreversible sensitive data protection",
            "**Memory Safety**: Secure key derivation and cleanup"
        ]
        
        for feature in features:
            st.success(feature)
    
    else:
        st.info("Complete a secure login first to see encryption details")

with verification_tab:
    st.subheader("✅ Data Integrity Verification")
    
    if st.session_state.login_successful and st.session_state.encrypted_session_data:
        
        st.markdown("#### Decrypt and Verify Data")
        st.markdown("Enter your password to decrypt and verify the encrypted game data:")
        
        with st.form("verification_form"):
            verify_password = st.text_input("Password for Decryption", type="password")
            verify_submitted = st.form_submit_button("🔓 Decrypt & Verify")
        
        if verify_submitted and verify_password:
            try:
                # Set password and decrypt
                st.session_state.security_manager.set_session_password(verify_password)
                decrypted_data = st.session_state.security_manager.decrypt_game_data(
                    st.session_state.encrypted_session_data['encrypted_data']
                )
                
                st.success("✅ Decryption successful! Data integrity verified.")
                
                # Show decrypted game data structure (safe parts)
                safe_data = {
                    'game_name': decrypted_data.get('game_name'),
                    'progress': decrypted_data.get('progress', {}),
                    'scores': decrypted_data.get('scores', {}),
                    'settings': decrypted_data.get('settings', {}),
                    'metadata': decrypted_data.get('metadata', {})
                }
                
                st.markdown("#### 🎮 Decrypted Game Data")
                st.json(safe_data)
                
                # Show hash verification
                if 'sensitive_data' in decrypted_data:
                    st.markdown("#### 🔐 Sensitive Data Hashes")
                    sensitive_hashes = decrypted_data['sensitive_data']
                    
                    for field, hash_info in sensitive_hashes.items():
                        if isinstance(hash_info, dict) and 'hash' in hash_info:
                            st.code(f"{field}: {hash_info['hash'][:32]}... ({hash_info['algorithm']})")
                
            except Exception as e:
                st.error(f"Decryption failed: {str(e)}")
                st.warning("Possible causes: Incorrect password, corrupted data, or tampering detected")
    
    else:
        st.info("Complete a secure login first to verify data integrity")

# Additional security information
st.markdown("---")
st.subheader("🔒 Security Standards & Compliance")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("**Encryption Standards:**")
    st.markdown("• AES-256-GCM (NIST approved)")
    st.markdown("• PBKDF2-SHA256 key derivation")
    st.markdown("• 256-bit encryption keys")
    st.markdown("• Authenticated encryption")

with col2:
    st.markdown("**Hashing Algorithms:**")
    st.markdown("• BLAKE3 (latest cryptographic hash)")
    st.markdown("• SHA-256 (industry standard)")
    st.markdown("• Salt-based protection")
    st.markdown("• Collision resistance")

with col3:
    st.markdown("**Security Benefits:**")
    st.markdown("• Data confidentiality")
    st.markdown("• Integrity verification")
    st.markdown("• Authentication protection")
    st.markdown("• Forward secrecy")

# Implementation guide
with st.expander("📚 Implementation Guide for Developers"):
    st.markdown("""
    ### Real-World Integration Steps
    
    **1. Game Detection Integration:**
    ```python
    # Steam API integration
    import requests
    steam_api_key = "YOUR_STEAM_API_KEY"
    user_steam_id = "USER_STEAM_ID"
    
    # Xbox Live API
    xbox_auth_token = "YOUR_XBOX_TOKEN"
    
    # PlayStation Network API
    psn_access_token = "YOUR_PSN_TOKEN"
    ```
    
    **2. Production Database Setup:**
    ```sql
    CREATE TABLE encrypted_game_data (
        user_id_hash VARCHAR(64) PRIMARY KEY,
        encrypted_data TEXT NOT NULL,
        encryption_metadata JSON NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
    );
    ```
    
    **3. API Integration Points:**
    - Steam Web API for game detection
    - Xbox Live API for Xbox users
    - PlayStation Network API for PS users
    - Local process monitoring for desktop games
    - Browser extension for web games
    
    **4. Security Considerations:**
    - Implement rate limiting for encryption operations
    - Use secure key management systems (HSM/KMS)
    - Regular security audits and penetration testing
    - Compliance with GDPR, CCPA, and other privacy regulations
    """)

# Back to dashboard
if st.button("🏠 Back to Dashboard"):
    st.switch_page("app.py")