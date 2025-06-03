# SecureGamer - Privacy & Data Protection Platform for Gamers

SecureGamer is a comprehensive privacy education and data protection platform designed specifically for video game players. Built with Streamlit and PostgreSQL, it provides interactive tools for privacy assessment, education, and secure data management using enterprise-grade encryption.

## 🛡️ Features

### Core Privacy Tools
- **Privacy Risk Assessment**: Interactive questionnaire to evaluate gaming privacy risks
- **Privacy Education Center**: Comprehensive modules covering gaming privacy fundamentals
- **Privacy Checklist**: Actionable items for improving gaming privacy protection
- **Data Transparency Simulator**: Understand what data games collect and how it's used
- **Privacy Score Dashboard**: Track and improve your privacy protection over time

### Advanced Security Features
- **Secure Login & Encryption Demo**: Experience AES-256-GCM encryption for game data
- **BLAKE3 & SHA-256 Hashing**: Advanced cryptographic protection for sensitive fields
- **Privacy Controls Demo**: Interactive privacy settings simulation
- **Database Dashboard**: Monitor encrypted data storage and operations

### Technical Capabilities
- **AES-256-GCM Encryption**: Industry-standard encryption for sensitive game data
- **PBKDF2-SHA256 Key Derivation**: Secure password-based key generation
- **PostgreSQL Integration**: Secure database storage with proper encryption
- **Security Audit Logging**: Comprehensive tracking for compliance requirements
- **GDPR/CCPA Compliance Tools**: Built-in privacy rights management

## 🚀 Quick Start

### Prerequisites
- Python 3.11+
- PostgreSQL database
- Required Python packages (automatically installed)

### Installation

1. **Clone or download the project files**

2. **Install dependencies**:
   ```bash
   pip install streamlit plotly pandas sqlalchemy psycopg2-binary cryptography blake3
   ```

3. **Set up PostgreSQL database**:
   - Ensure PostgreSQL is running
   - The application will automatically create necessary tables
   - Required environment variables:
     - `DATABASE_URL`
     - `PGHOST`, `PGPORT`, `PGUSER`, `PGPASSWORD`, `PGDATABASE`

4. **Run the application**:
   ```bash
   streamlit run app.py --server.port 5000
   ```

5. **Access the platform**:
   Open your browser to `http://localhost:5000`

## 📊 Database Schema

The platform uses a secure PostgreSQL database with the following main tables:

### users
Stores user account information with hashed identifiers
- `user_id_hash`: SHA-256 hashed user identifier
- `username`: Display name
- `privacy_score`: Current privacy protection score
- `created_at`, `last_login`: Timestamp tracking

### encrypted_game_data
Securely stores encrypted game data
- `encrypted_payload`: AES-256-GCM encrypted game data
- `encryption_metadata`: Encryption parameters and security info
- `data_hash`: Data integrity verification hash

### privacy_assessments
Privacy risk assessment results and history
- `assessment_data`: Complete assessment responses
- `risk_score`: Calculated privacy risk (0-100)
- `risk_level`: Risk classification (Low/Medium/High)
- `recommendations`: Personalized improvement suggestions

### security_audit_log
Comprehensive security event logging
- `action_type`: Type of security action performed
- `resource_type`: Resource accessed or modified
- `details`: Additional context and metadata
- `timestamp`: When the action occurred

## 🔐 Security Implementation

### Encryption Standards
- **AES-256-GCM**: Authenticated encryption for data confidentiality and integrity
- **PBKDF2-SHA256**: Key derivation with 100,000 iterations
- **BLAKE3**: Modern cryptographic hashing for sensitive fields
- **SHA-256**: Standard hashing for user identifiers

### Security Features
- **Data at Rest Encryption**: All sensitive data encrypted in database
- **Hash-based User Identification**: No plaintext user identifiers stored
- **Secure Session Management**: Password-based encryption keys
- **Audit Trail**: Complete logging of security-relevant actions
- **Data Integrity Verification**: Cryptographic verification of stored data

### Privacy Protection
- **Zero-Knowledge Architecture**: Minimal personal data collection
- **Configurable Data Retention**: User-controlled data lifecycle
- **GDPR Compliance**: Built-in privacy rights management
- **Anonymization**: Hash-based user identification prevents direct correlation

## 🎮 Gaming Privacy Education

### Educational Modules
1. **Understanding Gaming Privacy**: Fundamentals of privacy in gaming environments
2. **Password Security for Gamers**: Master password security and 2FA
3. **Social Gaming Privacy**: Navigate privacy in multiplayer environments
4. **Data Rights and Control**: Exercise your legal data rights

### Interactive Features
- **Knowledge Quizzes**: Test understanding with interactive questions
- **Scenario Practice**: Real-world privacy decision scenarios
- **Progress Tracking**: Monitor learning advancement and achievements
- **Personalized Recommendations**: Tailored privacy improvement suggestions

## 🏗️ Architecture

### Frontend (Streamlit)
- Interactive web interface for all privacy tools
- Real-time data visualization with Plotly
- Responsive design for desktop and mobile
- Accessible UI following WCAG guidelines

### Backend Security Layer
- `EncryptionManager`: Handles all cryptographic operations
- `GameDataSecurityManager`: Manages secure game data processing
- `SecureGameDataDB`: Database operations with security controls

### Database Layer (PostgreSQL)
- Encrypted data storage with proper indexing
- Transaction-based operations for data consistency
- Automated cleanup and retention policy enforcement
- Connection security with SSL/TLS

## 🛠️ Development

### Project Structure
```
├── app.py                    # Main application entry point
├── pages/                    # Streamlit pages
│   ├── privacy_assessment.py
│   ├── privacy_education.py
│   ├── privacy_checklist.py
│   ├── data_transparency.py
│   ├── privacy_score.py
│   ├── privacy_controls_demo.py
│   ├── secure_login_demo.py
│   └── database_dashboard.py
├── utils/                    # Core utilities
│   ├── encryption_manager.py
│   ├── database_manager.py
│   ├── privacy_calculator.py
│   └── education_content.py
└── .streamlit/
    └── config.toml          # Streamlit configuration
```

### Key Components

#### EncryptionManager
Provides cryptographic services:
- AES-256-GCM encryption/decryption
- PBKDF2 key derivation
- BLAKE3 and SHA-256 hashing
- RSA/ECC key generation (for future use)

#### GameDataSecurityManager
Manages secure game data handling:
- Game detection simulation
- Data retrieval and processing
- Complete encryption workflow
- Secure login flow orchestration

#### SecureGameDataDB
Database operations with security focus:
- Encrypted data storage
- User management with hashed IDs
- Privacy assessment tracking
- Security audit logging

## 🔒 Security Considerations

### Production Deployment
- Use environment variables for database credentials
- Implement proper SSL/TLS for database connections
- Regular security audits and penetration testing
- Secure key management with HSM/KMS solutions
- Monitor and alert on security events

### Data Protection
- Implement data minimization principles
- Regular backup with encryption
- Incident response procedures
- Privacy impact assessments
- User consent management

### Compliance
- GDPR Article 25: Privacy by Design
- CCPA requirements for data transparency
- Gaming industry privacy standards
- Regular compliance audits

## 📝 License

This project is designed for educational and demonstration purposes. For production use, ensure proper security reviews and compliance with applicable regulations.

## 🤝 Contributing

When contributing to this project:
1. Follow secure coding practices
2. Include security considerations in pull requests
3. Test encryption/decryption functionality thoroughly
4. Update documentation for security-relevant changes
5. Ensure compliance with privacy regulations

## 📞 Support

For questions about security implementation or privacy features, refer to the built-in documentation and educational modules within the application.

## ⚠️ Important Notes

- This platform demonstrates security concepts for educational purposes
- For production use, conduct thorough security reviews
- Ensure compliance with local privacy regulations
- Regular updates and security patches recommended
- Database credentials should be securely managed in production environments