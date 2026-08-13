import os
import base64
import hashlib
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import json
from django.conf import settings
from datetime import datetime

class CredentialVault:
    """
    Secure credential vault for storing and retrieving encrypted credentials.
    Uses Fernet symmetric encryption with a key derived from a secret.
    """
    
    def __init__(self):
        # In a real implementation, the secret key would come from a secure source
        # like AWS KMS, HashiCorp Vault, or environment variables
        self.secret_key = self._get_or_create_secret_key()
        self.cipher_suite = Fernet(self.secret_key)
        
        # In-memory cache for decrypted credentials (use with caution!)
        # In production, consider not caching decrypted credentials at all
        self._credential_cache = {}
    
    def _get_or_create_secret_key(self):
        """
        Get or create a secret key for encryption.
        In production, this should come from a secure secret management system.
        """
        # Try to get key from environment variable
        key_env = os.environ.get('CREDENTIAL_VAULT_KEY')
        if key_env:
            # Ensure it's properly formatted for Fernet
            try:
                # If it's already a base64-encoded key, use it
                if len(key_env) == 44 and key_env.endswith('='):
                    return key_env.encode()
                # Otherwise, derive a key from it
                return self._derive_key(key_env.encode())
            except Exception:
                # If there's an error, derive a key from it
                return self._derive_key(key_env.encode())
        
        # Fallback: derive key from Django's SECRET_KEY (not ideal but better than nothing for demo)
        if hasattr(settings, 'SECRET_KEY') and settings.SECRET_KEY:
            try:
                return self._derive_key(settings.SECRET_KEY.encode())
            except Exception:
                pass
        
        # Last resort: generate a key and store it in a file (NOT SECURE FOR PRODUCTION)
        # This is only for development/demo purposes
        key_file = os.path.join(os.path.dirname(__file__), '.vault_key')
        if os.path.exists(key_file):
            with open(key_file, 'rb') as f:
                return f.read()
        else:
            # Generate a new key
            key = Fernet.generate_key()
            # In production, NEVER store the key in plain text like this
            # This is only for demonstration purposes
            with open(key_file, 'wb') as f:
                f.write(key)
            # Make the file readable only by the owner (Unix-like systems)
            try:
                os.chmod(key_file, 0o600)
            except Exception:
                pass  # Ignore permission errors on Windows
            return key
    
    def _derive_key(self, key_material):
        """
        Derive a Fernet key from key material using PBKDF2.
        """
        # Use a fixed salt for deterministic key derivation (in production, use a random salt stored securely)
        salt = b'flowforge_vault_salt_fixed_for_demo'  # NOT SECURE - only for demo
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
        )
        key = base64.urlsafe_b64encode(kdf.derive(key_material))
        return key
    
    def encrypt_credential(self, credential_data):
        """
        Encrypt credential data.
        
        Args:
            credential_data (str or dict): The credential data to encrypt.
            
        Returns:
            str: Base64-encoded encrypted data.
        """
        if isinstance(credential_data, dict):
            credential_data = json.dumps(credential_data)
        
        if not isinstance(credential_data, str):
            credential_data = str(credential_data)
        
        encrypted_data = self.cipher_suite.encrypt(credential_data.encode('utf-8'))
        return base64.urlsafe_b64encode(encrypted_data).decode('utf-8')
    
    def decrypt_credential(self, encrypted_credential):
        """
        Decrypt credential data.
        
        Args:
            encrypted_credential (str): Base64-encoded encrypted data.
            
        Returns:
            str: Decrypted credential data (as string, or JSON if it was originally JSON).
        """
        try:
            # Add padding if needed
            padding = 4 - len(encrypted_credential) % 4
            if padding != 4:
                encrypted_credential += '=' * padding
            
            encrypted_data = base64.urlsafe_b64decode(encrypted_credential.encode('utf-8'))
            decrypted_data = self.cipher_suite.decrypt(encrypted_data)
            
            # Try to parse as JSON
            try:
                return json.loads(decrypted_data.decode('utf-8'))
            except json.JSONDecodeError:
                # Return as string if not valid JSON
                return decrypted_data.decode('utf-8')
        except Exception as e:
            raise ValueError(f"Failed to decrypt credential: {str(e)}")
    
    def store_credential(self, credential_id, credential_data):
        """
        Store a credential in the vault (in this implementation, we just return the encrypted data).
        In a real implementation, this would store in a database or secure storage.
        
        Args:
            credential_id (str or int): Unique identifier for the credential.
            credential_data (str or dict): The credential data to store.
            
        Returns:
            dict: Storage result including the encrypted credential.
        """
        encrypted = self.encrypt_credential(credential_data)
        
        # In a real implementation, you would store this in a database
        # For this demo, we'll just return the encrypted data
        # The caller is responsible for storing it securely (e.g., in the Credential model)
        
        return {
            "credential_id": credential_id,
            "encrypted_credential": encrypted,
            "encrypted_at": datetime.now().isoformat(),
            "vault_version": "1.0"
        }
    
    def retrieve_credential(self, credential_id, encrypted_credential):
        """
        Retrieve and decrypt a credential from storage.
        
        Args:
            credential_id (str or int): Unique identifier for the credential.
            encrypted_credential (str): The encrypted credential data to decrypt.
            
        Returns:
            The decrypted credential data.
        """
        # Check cache first (in production, be very careful about caching decrypted credentials)
        cache_key = f"{credential_id}:{hashlib.sha256(encrypted_credential.encode()).hexdigest()}"
        if cache_key in self._credential_cache:
            return self._credential_cache[cache_key]
        
        # Decrypt the credential
        decrypted = self.decrypt_credential(encrypted_credential)
        
        # Cache the decrypted credential (with a timeout in production)
        # For security, consider not caching at all, or using a short-lived cache
        self._credential_cache[cache_key] = decrypted
        
        # Limit cache size (simple FIFO eviction)
        if len(self._credential_cache) > 100:
            # Remove oldest entry (simple approach)
            oldest_key = next(iter(self._credential_cache))
            del self._credential_cache[oldest_key]
        
        return decrypted
    
    def clear_cache(self):
        """
        Clear the credential cache.
        Should be called periodically or on security events.
        """
        self._credential_cache.clear()

# Create a singleton instance for easy access
credential_vault = CredentialVault()
