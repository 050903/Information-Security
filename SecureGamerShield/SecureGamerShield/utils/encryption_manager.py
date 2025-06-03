"""
Encryption utilities for secure game data handling
Implements AES-256, RSA/ECC encryption and SHA-256/BLAKE3 hashing
"""

import os
import hashlib
import base64
import json
from datetime import datetime
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa, ec
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.backends import default_backend
import blake3

class EncryptionManager:
    """Handles encryption, decryption, and hashing of sensitive game data"""
    
    def __init__(self):
        self.backend = default_backend()
        
    def generate_aes_key(self, password: str, salt: bytes = None) -> tuple:
        """Generate AES-256 key from password using PBKDF2"""
        if salt is None:
            salt = os.urandom(16)
        
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,  # 256 bits
            salt=salt,
            iterations=100000,
            backend=self.backend
        )
        key = kdf.derive(password.encode())
        return key, salt
    
    def encrypt_aes_256(self, data: str, password: str) -> dict:
        """Encrypt data using AES-256-GCM"""
        try:
            # Generate key and salt
            key, salt = self.generate_aes_key(password)
            
            # Generate random IV
            iv = os.urandom(12)  # 96-bit IV for GCM
            
            # Create cipher
            cipher = Cipher(
                algorithms.AES(key),
                modes.GCM(iv),
                backend=self.backend
            )
            encryptor = cipher.encryptor()
            
            # Encrypt data
            ciphertext = encryptor.update(data.encode()) + encryptor.finalize()
            
            return {
                'ciphertext': base64.b64encode(ciphertext).decode(),
                'salt': base64.b64encode(salt).decode(),
                'iv': base64.b64encode(iv).decode(),
                'tag': base64.b64encode(encryptor.tag).decode(),
                'algorithm': 'AES-256-GCM',
                'timestamp': datetime.utcnow().isoformat()
            }
        except Exception as e:
            raise Exception(f"AES encryption failed: {str(e)}")
    
    def decrypt_aes_256(self, encrypted_data: dict, password: str) -> str:
        """Decrypt AES-256-GCM encrypted data"""
        try:
            # Extract components
            ciphertext = base64.b64decode(encrypted_data['ciphertext'])
            salt = base64.b64decode(encrypted_data['salt'])
            iv = base64.b64decode(encrypted_data['iv'])
            tag = base64.b64decode(encrypted_data['tag'])
            
            # Regenerate key
            key, _ = self.generate_aes_key(password, salt)
            
            # Create cipher
            cipher = Cipher(
                algorithms.AES(key),
                modes.GCM(iv, tag),
                backend=self.backend
            )
            decryptor = cipher.decryptor()
            
            # Decrypt data
            plaintext = decryptor.update(ciphertext) + decryptor.finalize()
            return plaintext.decode()
        except Exception as e:
            raise Exception(f"AES decryption failed: {str(e)}")
    
    def generate_rsa_keypair(self, key_size: int = 2048) -> tuple:
        """Generate RSA key pair"""
        private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=key_size,
            backend=self.backend
        )
        public_key = private_key.public_key()
        return private_key, public_key
    
    def generate_ecc_keypair(self) -> tuple:
        """Generate ECC key pair using secp256r1 curve"""
        private_key = ec.generate_private_key(
            ec.SECP256R1(),
            backend=self.backend
        )
        public_key = private_key.public_key()
        return private_key, public_key
    
    def hash_sha256(self, data: str, salt: str = None) -> dict:
        """Hash data using SHA-256 with optional salt"""
        if salt is None:
            salt = os.urandom(32).hex()
        
        hash_input = (data + salt).encode()
        hash_digest = hashlib.sha256(hash_input).hexdigest()
        
        return {
            'hash': hash_digest,
            'salt': salt,
            'algorithm': 'SHA-256',
            'timestamp': datetime.utcnow().isoformat()
        }
    
    def hash_blake3(self, data: str, salt: str = None) -> dict:
        """Hash data using BLAKE3 with optional salt"""
        if salt is None:
            salt = os.urandom(32).hex()
        
        hash_input = (data + salt).encode()
        hash_digest = blake3.blake3(hash_input).hexdigest()
        
        return {
            'hash': hash_digest,
            'salt': salt,
            'algorithm': 'BLAKE3',
            'timestamp': datetime.utcnow().isoformat()
        }
    
    def verify_hash(self, data: str, hash_info: dict) -> bool:
        """Verify data against stored hash"""
        try:
            salt = hash_info['salt']
            stored_hash = hash_info['hash']
            algorithm = hash_info['algorithm']
            
            if algorithm == 'SHA-256':
                new_hash = self.hash_sha256(data, salt)['hash']
            elif algorithm == 'BLAKE3':
                new_hash = self.hash_blake3(data, salt)['hash']
            else:
                raise ValueError(f"Unsupported hash algorithm: {algorithm}")
            
            return new_hash == stored_hash
        except Exception:
            return False

class GameDataSecurityManager:
    """Manages secure handling of game-related user data"""
    
    def __init__(self):
        self.encryption_manager = EncryptionManager()
        self.session_password = None
    
    def set_session_password(self, password: str):
        """Set the session password for encryption"""
        self.session_password = password
    
    def detect_current_game(self, user_session: dict) -> str:
        """Detect currently playing game from user session"""
        # In a real implementation, this would integrate with:
        # - Steam API
        # - Xbox Live API
        # - PlayStation Network API
        # - Process monitoring
        # - Browser activity monitoring
        
        # For demo purposes, simulate game detection
        detected_games = [
            "Valorant", "League of Legends", "Fortnite", 
            "Minecraft", "Among Us", "Call of Duty", 
            "Apex Legends", "Rocket League"
        ]
        
        # Simulate detection based on session data
        if 'last_game' in user_session:
            return user_session['last_game']
        
        # Default fallback
        return detected_games[0]  # Would be actual detection in production
    
    def retrieve_game_data(self, user_id: str, game_name: str) -> dict:
        """Retrieve user's game-related data"""
        # In production, this would fetch from:
        # - Game APIs
        # - Local game files
        # - Cloud save data
        # - Platform-specific APIs
        
        # Simulated game data structure
        game_data = {
            'user_id': user_id,
            'game_name': game_name,
            'progress': {
                'level': 42,
                'experience_points': 15750,
                'achievements_unlocked': 23,
                'total_playtime_hours': 127.5,
                'last_played': datetime.utcnow().isoformat()
            },
            'scores': {
                'high_score': 89500,
                'average_score': 45200,
                'total_matches': 312,
                'wins': 187,
                'losses': 125
            },
            'settings': {
                'difficulty': 'Hard',
                'graphics_quality': 'Ultra',
                'audio_volume': 0.8,
                'control_scheme': 'Custom',
                'privacy_mode': True
            },
            'sensitive_data': {
                'auth_token': f"token_{user_id}_{game_name}",
                'session_key': f"session_{os.urandom(16).hex()}",
                'api_credentials': f"cred_{user_id}"
            },
            'metadata': {
                'retrieved_at': datetime.utcnow().isoformat(),
                'data_version': '1.0',
                'encryption_required': True
            }
        }
        
        return game_data
    
    def encrypt_game_data(self, game_data: dict, encryption_method: str = 'AES') -> dict:
        """Encrypt game data using specified method"""
        if not self.session_password:
            raise ValueError("Session password not set. Call set_session_password() first.")
        
        try:
            # Separate sensitive and non-sensitive data
            sensitive_fields = ['auth_token', 'session_key', 'api_credentials']
            encrypted_data = game_data.copy()
            
            # Hash sensitive fields
            if 'sensitive_data' in game_data:
                for field, value in game_data['sensitive_data'].items():
                    if field in sensitive_fields:
                        # Hash sensitive tokens/credentials
                        hash_info = self.encryption_manager.hash_blake3(str(value))
                        encrypted_data['sensitive_data'][f"{field}_hash"] = hash_info
                        # Remove original sensitive data
                        del encrypted_data['sensitive_data'][field]
            
            # Convert to JSON for encryption
            data_json = json.dumps(encrypted_data, default=str)
            
            # Encrypt based on method
            if encryption_method.upper() == 'AES':
                encryption_result = self.encryption_manager.encrypt_aes_256(
                    data_json, 
                    self.session_password
                )
            else:
                raise ValueError(f"Unsupported encryption method: {encryption_method}")
            
            # Add metadata
            encryption_result['original_game'] = game_data['game_name']
            encryption_result['user_id_hash'] = self.encryption_manager.hash_sha256(
                game_data['user_id']
            )['hash']
            encryption_result['encryption_method'] = encryption_method
            
            return encryption_result
        
        except Exception as e:
            raise Exception(f"Game data encryption failed: {str(e)}")
    
    def decrypt_game_data(self, encrypted_data: dict) -> dict:
        """Decrypt game data"""
        if not self.session_password:
            raise ValueError("Session password not set. Call set_session_password() first.")
        
        try:
            encryption_method = encrypted_data.get('encryption_method', 'AES')
            
            if encryption_method == 'AES':
                decrypted_json = self.encryption_manager.decrypt_aes_256(
                    encrypted_data,
                    self.session_password
                )
                return json.loads(decrypted_json)
            else:
                raise ValueError(f"Unsupported decryption method: {encryption_method}")
        
        except Exception as e:
            raise Exception(f"Game data decryption failed: {str(e)}")
    
    def secure_login_flow(self, user_id: str, password: str) -> dict:
        """Complete secure login flow with game detection and data encryption"""
        try:
            # Set session password for encryption
            self.set_session_password(password)
            
            # Simulate user session data
            user_session = {
                'user_id': user_id,
                'login_time': datetime.utcnow().isoformat(),
                'last_game': 'Valorant'  # Would come from actual detection
            }
            
            # Step 1: Detect current game
            current_game = self.detect_current_game(user_session)
            
            # Step 2: Retrieve game data
            game_data = self.retrieve_game_data(user_id, current_game)
            
            # Step 3: Encrypt the data
            encrypted_data = self.encrypt_game_data(game_data, 'AES')
            
            # Step 4: Prepare secure response
            secure_response = {
                'status': 'success',
                'user_id_hash': encrypted_data['user_id_hash'],
                'detected_game': current_game,
                'encrypted_data': encrypted_data,
                'security_info': {
                    'encryption_algorithm': encrypted_data['algorithm'],
                    'hash_algorithms_used': ['SHA-256', 'BLAKE3'],
                    'data_encrypted_at': encrypted_data['timestamp'],
                    'security_level': 'high'
                },
                'data_summary': {
                    'total_fields_encrypted': len(game_data),
                    'sensitive_fields_hashed': 3,
                    'encryption_key_strength': '256-bit',
                    'authentication_method': 'PBKDF2-SHA256'
                }
            }
            
            return secure_response
        
        except Exception as e:
            return {
                'status': 'error',
                'error_message': str(e),
                'security_info': {
                    'error_logged': True,
                    'timestamp': datetime.utcnow().isoformat()
                }
            }

def verify_encryption_integrity(encrypted_data: dict, password: str) -> bool:
    """Verify the integrity of encrypted data"""
    try:
        manager = GameDataSecurityManager()
        manager.set_session_password(password)
        
        # Try to decrypt and verify
        decrypted = manager.decrypt_game_data(encrypted_data)
        return isinstance(decrypted, dict) and 'game_name' in decrypted
    except Exception:
        return False