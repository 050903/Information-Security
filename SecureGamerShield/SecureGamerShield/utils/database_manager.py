"""
Database manager for secure storage of encrypted game data
Uses PostgreSQL with proper security measures
"""

import os
import json
from datetime import datetime
from typing import Optional, Dict, List
import sqlalchemy as sa
from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError
import pandas as pd

class SecureGameDataDB:
    """Manages secure database operations for encrypted game data"""
    
    def __init__(self):
        self.database_url = os.getenv('DATABASE_URL')
        if not self.database_url:
            raise ValueError("DATABASE_URL environment variable not set")
        
        self.engine = create_engine(self.database_url)
        self._initialize_tables()
    
    def _initialize_tables(self):
        """Create necessary tables for secure data storage"""
        
        # Create tables for encrypted game data storage
        create_tables_sql = """
        -- Users table for authentication and user management
        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            user_id_hash VARCHAR(64) UNIQUE NOT NULL,
            username VARCHAR(100) NOT NULL,
            email_hash VARCHAR(64),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            last_login TIMESTAMP,
            privacy_score INTEGER DEFAULT 0,
            account_status VARCHAR(20) DEFAULT 'active'
        );
        
        -- Encrypted game data storage
        CREATE TABLE IF NOT EXISTS encrypted_game_data (
            id SERIAL PRIMARY KEY,
            user_id_hash VARCHAR(64) NOT NULL,
            game_name VARCHAR(100) NOT NULL,
            encrypted_payload TEXT NOT NULL,
            encryption_metadata JSONB NOT NULL,
            data_hash VARCHAR(64) NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            encryption_version VARCHAR(10) DEFAULT '1.0',
            FOREIGN KEY (user_id_hash) REFERENCES users(user_id_hash)
        );
        
        -- Privacy assessment results
        CREATE TABLE IF NOT EXISTS privacy_assessments (
            id SERIAL PRIMARY KEY,
            user_id_hash VARCHAR(64) NOT NULL,
            assessment_data JSONB NOT NULL,
            risk_score INTEGER NOT NULL,
            risk_level VARCHAR(20) NOT NULL,
            recommendations JSONB,
            completed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id_hash) REFERENCES users(user_id_hash)
        );
        
        -- User privacy settings and preferences
        CREATE TABLE IF NOT EXISTS privacy_settings (
            id SERIAL PRIMARY KEY,
            user_id_hash VARCHAR(64) UNIQUE NOT NULL,
            settings_data JSONB NOT NULL,
            encryption_preferences JSONB,
            data_retention_days INTEGER DEFAULT 365,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id_hash) REFERENCES users(user_id_hash)
        );
        
        -- Security audit log
        CREATE TABLE IF NOT EXISTS security_audit_log (
            id SERIAL PRIMARY KEY,
            user_id_hash VARCHAR(64),
            action_type VARCHAR(50) NOT NULL,
            resource_type VARCHAR(50),
            resource_id VARCHAR(100),
            details JSONB,
            ip_address INET,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            success BOOLEAN DEFAULT TRUE
        );
        
        -- Education progress tracking
        CREATE TABLE IF NOT EXISTS education_progress (
            id SERIAL PRIMARY KEY,
            user_id_hash VARCHAR(64) NOT NULL,
            module_name VARCHAR(100) NOT NULL,
            completion_status VARCHAR(20) DEFAULT 'in_progress',
            quiz_score INTEGER,
            completed_at TIMESTAMP,
            time_spent_minutes INTEGER,
            FOREIGN KEY (user_id_hash) REFERENCES users(user_id_hash),
            UNIQUE(user_id_hash, module_name)
        );
        
        -- Create indexes for better performance
        CREATE INDEX IF NOT EXISTS idx_users_user_id_hash ON users(user_id_hash);
        CREATE INDEX IF NOT EXISTS idx_encrypted_game_data_user_game ON encrypted_game_data(user_id_hash, game_name);
        CREATE INDEX IF NOT EXISTS idx_privacy_assessments_user ON privacy_assessments(user_id_hash);
        CREATE INDEX IF NOT EXISTS idx_security_audit_log_user_timestamp ON security_audit_log(user_id_hash, timestamp);
        CREATE INDEX IF NOT EXISTS idx_education_progress_user ON education_progress(user_id_hash);
        """
        
        try:
            with self.engine.connect() as conn:
                conn.execute(text(create_tables_sql))
                conn.commit()
        except SQLAlchemyError as e:
            raise Exception(f"Failed to initialize database tables: {str(e)}")
    
    def create_user(self, user_id_hash: str, username: str, email_hash: str = "") -> bool:
        """Create a new user record"""
        try:
            with self.engine.connect() as conn:
                result = conn.execute(
                    text("""
                    INSERT INTO users (user_id_hash, username, email_hash, last_login)
                    VALUES (:user_id_hash, :username, :email_hash, :last_login)
                    ON CONFLICT (user_id_hash) DO UPDATE SET
                        last_login = :last_login
                    """),
                    {
                        'user_id_hash': user_id_hash,
                        'username': username,
                        'email_hash': email_hash,
                        'last_login': datetime.utcnow()
                    }
                )
                conn.commit()
                return True
        except SQLAlchemyError as e:
            print(f"Error creating user: {str(e)}")
            return False
    
    def store_encrypted_game_data(self, user_id_hash: str, game_name: str, 
                                 encrypted_data: dict, data_hash: str) -> bool:
        """Store encrypted game data securely"""
        try:
            with self.engine.connect() as conn:
                # Check if data already exists for this user and game
                existing = conn.execute(
                    text("SELECT id FROM encrypted_game_data WHERE user_id_hash = :user_id_hash AND game_name = :game_name"),
                    {'user_id_hash': user_id_hash, 'game_name': game_name}
                ).fetchone()
                
                if existing:
                    # Update existing record
                    conn.execute(
                        text("""
                        UPDATE encrypted_game_data 
                        SET encrypted_payload = :payload,
                            encryption_metadata = :metadata,
                            data_hash = :data_hash,
                            updated_at = :updated_at
                        WHERE user_id_hash = :user_id_hash AND game_name = :game_name
                        """),
                        {
                            'payload': json.dumps(encrypted_data),
                            'metadata': json.dumps(encrypted_data.get('security_info', {})),
                            'data_hash': data_hash,
                            'updated_at': datetime.utcnow(),
                            'user_id_hash': user_id_hash,
                            'game_name': game_name
                        }
                    )
                else:
                    # Insert new record
                    conn.execute(
                        text("""
                        INSERT INTO encrypted_game_data 
                        (user_id_hash, game_name, encrypted_payload, encryption_metadata, data_hash)
                        VALUES (:user_id_hash, :game_name, :payload, :metadata, :data_hash)
                        """),
                        {
                            'user_id_hash': user_id_hash,
                            'game_name': game_name,
                            'payload': json.dumps(encrypted_data),
                            'metadata': json.dumps(encrypted_data.get('security_info', {})),
                            'data_hash': data_hash
                        }
                    )
                
                conn.commit()
                return True
        except SQLAlchemyError as e:
            print(f"Error storing encrypted game data: {str(e)}")
            return False
    
    def retrieve_encrypted_game_data(self, user_id_hash: str, game_name: str = None) -> List[Dict]:
        """Retrieve encrypted game data for a user"""
        try:
            with self.engine.connect() as conn:
                if game_name:
                    # Get specific game data
                    result = conn.execute(
                        text("""
                        SELECT game_name, encrypted_payload, encryption_metadata, 
                               data_hash, created_at, updated_at
                        FROM encrypted_game_data 
                        WHERE user_id_hash = :user_id_hash AND game_name = :game_name
                        """),
                        {'user_id_hash': user_id_hash, 'game_name': game_name}
                    )
                else:
                    # Get all game data for user
                    result = conn.execute(
                        text("""
                        SELECT game_name, encrypted_payload, encryption_metadata,
                               data_hash, created_at, updated_at
                        FROM encrypted_game_data 
                        WHERE user_id_hash = :user_id_hash
                        ORDER BY updated_at DESC
                        """),
                        {'user_id_hash': user_id_hash}
                    )
                
                rows = result.fetchall()
                return [
                    {
                        'game_name': row[0],
                        'encrypted_payload': json.loads(row[1]) if row[1] else {},
                        'encryption_metadata': json.loads(row[2]) if row[2] else {},
                        'data_hash': row[3],
                        'created_at': row[4],
                        'updated_at': row[5]
                    }
                    for row in rows
                ]
        except SQLAlchemyError as e:
            print(f"Error retrieving encrypted game data: {str(e)}")
            return []
    
    def store_privacy_assessment(self, user_id_hash: str, assessment_data: dict, 
                               risk_score: int, risk_level: str, recommendations: list) -> bool:
        """Store privacy assessment results"""
        try:
            with self.engine.connect() as conn:
                conn.execute(
                    text("""
                    INSERT INTO privacy_assessments 
                    (user_id_hash, assessment_data, risk_score, risk_level, recommendations)
                    VALUES (:user_id_hash, :assessment_data, :risk_score, :risk_level, :recommendations)
                    """),
                    {
                        'user_id_hash': user_id_hash,
                        'assessment_data': json.dumps(assessment_data),
                        'risk_score': risk_score,
                        'risk_level': risk_level,
                        'recommendations': json.dumps(recommendations)
                    }
                )
                conn.commit()
                return True
        except SQLAlchemyError as e:
            print(f"Error storing privacy assessment: {str(e)}")
            return False
    
    def get_user_privacy_score_history(self, user_id_hash: str) -> List[Dict]:
        """Get privacy score history for a user"""
        try:
            with self.engine.connect() as conn:
                result = conn.execute(
                    text("""
                    SELECT risk_score, risk_level, completed_at
                    FROM privacy_assessments 
                    WHERE user_id_hash = :user_id_hash
                    ORDER BY completed_at DESC
                    LIMIT 30
                    """),
                    {'user_id_hash': user_id_hash}
                )
                
                rows = result.fetchall()
                return [
                    {
                        'risk_score': row[0],
                        'risk_level': row[1],
                        'completed_at': row[2]
                    }
                    for row in rows
                ]
        except SQLAlchemyError as e:
            print(f"Error retrieving privacy score history: {str(e)}")
            return []
    
    def update_privacy_settings(self, user_id_hash: str, settings_data: dict) -> bool:
        """Update user privacy settings"""
        try:
            with self.engine.connect() as conn:
                conn.execute(
                    text("""
                    INSERT INTO privacy_settings (user_id_hash, settings_data, updated_at)
                    VALUES (:user_id_hash, :settings_data, :updated_at)
                    ON CONFLICT (user_id_hash) DO UPDATE SET
                        settings_data = :settings_data,
                        updated_at = :updated_at
                    """),
                    {
                        'user_id_hash': user_id_hash,
                        'settings_data': json.dumps(settings_data),
                        'updated_at': datetime.utcnow()
                    }
                )
                conn.commit()
                return True
        except SQLAlchemyError as e:
            print(f"Error updating privacy settings: {str(e)}")
            return False
    
    def log_security_action(self, user_id_hash: str, action_type: str, 
                          resource_type: str = None, details: dict = None) -> bool:
        """Log security-related actions for audit purposes"""
        try:
            with self.engine.connect() as conn:
                conn.execute(
                    text("""
                    INSERT INTO security_audit_log 
                    (user_id_hash, action_type, resource_type, details)
                    VALUES (:user_id_hash, :action_type, :resource_type, :details)
                    """),
                    {
                        'user_id_hash': user_id_hash,
                        'action_type': action_type,
                        'resource_type': resource_type,
                        'details': json.dumps(details) if details else None
                    }
                )
                conn.commit()
                return True
        except SQLAlchemyError as e:
            print(f"Error logging security action: {str(e)}")
            return False
    
    def get_database_stats(self) -> Dict:
        """Get database statistics and health information"""
        try:
            with self.engine.connect() as conn:
                stats = {}
                
                # Count users
                result = conn.execute(text("SELECT COUNT(*) FROM users"))
                stats['total_users'] = result.scalar()
                
                # Count encrypted game data records
                result = conn.execute(text("SELECT COUNT(*) FROM encrypted_game_data"))
                stats['total_game_data_records'] = result.scalar()
                
                # Count privacy assessments
                result = conn.execute(text("SELECT COUNT(*) FROM privacy_assessments"))
                stats['total_assessments'] = result.scalar()
                
                # Get recent activity
                result = conn.execute(text("""
                    SELECT COUNT(*) FROM security_audit_log 
                    WHERE timestamp > NOW() - INTERVAL '24 hours'
                """))
                stats['recent_activity_24h'] = result.scalar()
                
                # Database size
                result = conn.execute(text("""
                    SELECT pg_size_pretty(pg_database_size(current_database()))
                """))
                stats['database_size'] = result.scalar()
                
                return stats
        except SQLAlchemyError as e:
            print(f"Error getting database stats: {str(e)}")
            return {}
    
    def cleanup_old_data(self, retention_days: int = 365) -> bool:
        """Clean up old data based on retention policy"""
        try:
            with self.engine.connect() as conn:
                # Clean up old audit logs (keep last 90 days)
                conn.execute(
                    text("""
                    DELETE FROM security_audit_log 
                    WHERE timestamp < NOW() - INTERVAL ':days days'
                    """),
                    {'days': 90}
                )
                
                # Clean up old privacy assessments (keep based on user settings)
                conn.execute(
                    text("""
                    DELETE FROM privacy_assessments 
                    WHERE completed_at < NOW() - INTERVAL ':days days'
                    """),
                    {'days': retention_days}
                )
                
                conn.commit()
                return True
        except SQLAlchemyError as e:
            print(f"Error cleaning up old data: {str(e)}")
            return False

def get_database_connection():
    """Get database connection for external use"""
    return SecureGameDataDB()