# -*- coding: utf-8 -*-
"""
Encryption Manager for NeoZork Interactive ML Trading Strategy Development.

This module provides comprehensive encryption and key management capabilities.
"""

import pandas as pd
import numpy as np
import time
import json
import hashlib
import secrets
import base64
from typing import Dict, Any, Optional, List, Tuple
from enum import Enum
import warnings

class EncryptionAlgorithm(Enum):
    """Encryption algorithm enumeration."""
    AES_256 = "aes_256"
    RSA_2048 = "rsa_2048"
    RSA_4096 = "rsa_4096"
    CHACHA20 = "chacha20"

class KeyType(Enum):
    """Key type enumeration."""
    SYMMETRIC = "symmetric"
    ASYMMETRIC = "asymmetric"
    HASH = "hash"

class EncryptionManager:
    """
    Encryption manager for data protection and key management.
    
    Features:
    - Symmetric Encryption (AES)
    - Asymmetric Encryption (RSA)
    - Key Generation and Management
    - Data Encryption/Decryption
    - Digital Signatures
    - Key Rotation
    """
    
    def __init__(self):
        """Initialize the Encryption Manager."""
        self.keys = {}
        self.encrypted_data = {}
        self.key_rotation_schedule = {}
        self.encryption_history = []
    
    def generate_symmetric_key(self, key_name: str, algorithm: str = EncryptionAlgorithm.AES_256.value) -> Dict[str, Any]:
        """
        Generate a symmetric encryption key.
        
        Args:
            key_name: Name for the key
            algorithm: Encryption algorithm
            
        Returns:
            Key generation result
        """
        try:
            # Validate algorithm
            valid_algorithms = [a.value for a in EncryptionAlgorithm]
            if algorithm not in valid_algorithms:
                return {"status": "error", "message": f"Invalid algorithm: {algorithm}"}
            
            # Check if key already exists
            if key_name in self.keys:
                return {"status": "error", "message": f"Key {key_name} already exists"}
            
            # Generate key based on algorithm
            if algorithm == EncryptionAlgorithm.AES_256.value:
                key_data = secrets.token_bytes(32)  # 256 bits
            elif algorithm == EncryptionAlgorithm.CHACHA20.value:
                key_data = secrets.token_bytes(32)  # 256 bits
            else:
                return {"status": "error", "message": f"Unsupported algorithm for symmetric key: {algorithm}"}
            
            # Generate key ID
            key_id = f"key_{int(time.time())}"
            
            # Create key
            key = {
                "key_id": key_id,
                "key_name": key_name,
                "key_type": KeyType.SYMMETRIC.value,
                "algorithm": algorithm,
                "key_data": base64.b64encode(key_data).decode(),
                "created_time": time.time(),
                "last_used": None,
                "usage_count": 0,
                "is_active": True
            }
            
            # Store key
            self.keys[key_name] = key
            
            result = {
                "status": "success",
                "key_id": key_id,
                "key_name": key_name,
                "key_type": KeyType.SYMMETRIC.value,
                "algorithm": algorithm,
                "key_size": len(key_data) * 8,
                "message": "Symmetric key generated successfully"
            }
            
            return result
            
        except Exception as e:
            return {"status": "error", "message": f"Failed to generate symmetric key: {str(e)}"}
    
    def generate_asymmetric_key_pair(self, key_name: str, algorithm: str = EncryptionAlgorithm.RSA_2048.value) -> Dict[str, Any]:
        """
        Generate an asymmetric encryption key pair.
        
        Args:
            key_name: Name for the key pair
            algorithm: Encryption algorithm
            
        Returns:
            Key pair generation result
        """
        try:
            # Validate algorithm
            valid_algorithms = [a.value for a in EncryptionAlgorithm]
            if algorithm not in valid_algorithms:
                return {"status": "error", "message": f"Invalid algorithm: {algorithm}"}
            
            # Check if key already exists
            if key_name in self.keys:
                return {"status": "error", "message": f"Key {key_name} already exists"}
            
            # Generate key pair based on algorithm
            if algorithm == EncryptionAlgorithm.RSA_2048.value:
                # Simulate RSA key generation
                private_key = secrets.token_bytes(256)  # 2048 bits
                public_key = secrets.token_bytes(256)   # 2048 bits
            elif algorithm == EncryptionAlgorithm.RSA_4096.value:
                # Simulate RSA key generation
                private_key = secrets.token_bytes(512)  # 4096 bits
                public_key = secrets.token_bytes(512)   # 4096 bits
            else:
                return {"status": "error", "message": f"Unsupported algorithm for asymmetric key: {algorithm}"}
            
            # Generate key ID
            key_id = f"key_{int(time.time())}"
            
            # Create key pair
            key_pair = {
                "key_id": key_id,
                "key_name": key_name,
                "key_type": KeyType.ASYMMETRIC.value,
                "algorithm": algorithm,
                "private_key": base64.b64encode(private_key).decode(),
                "public_key": base64.b64encode(public_key).decode(),
                "created_time": time.time(),
                "last_used": None,
                "usage_count": 0,
                "is_active": True
            }
            
            # Store key pair
            self.keys[key_name] = key_pair
            
            result = {
                "status": "success",
                "key_id": key_id,
                "key_name": key_name,
                "key_type": KeyType.ASYMMETRIC.value,
                "algorithm": algorithm,
                "key_size": len(private_key) * 8,
                "public_key": key_pair["public_key"],
                "message": "Asymmetric key pair generated successfully"
            }
            
            return result
            
        except Exception as e:
            return {"status": "error", "message": f"Failed to generate asymmetric key pair: {str(e)}"}
    
    def encrypt_data(self, data: str, key_name: str, algorithm: str = None) -> Dict[str, Any]:
        """
        Encrypt data using specified key.
        
        Args:
            data: Data to encrypt
            key_name: Name of the encryption key
            algorithm: Encryption algorithm (optional, uses key's algorithm if not specified)
            
        Returns:
            Encryption result
        """
        try:
            # Check if key exists
            if key_name not in self.keys:
                return {"status": "error", "message": f"Key {key_name} not found"}
            
            key = self.keys[key_name]
            
            # Check if key is active
            if not key["is_active"]:
                return {"status": "error", "message": f"Key {key_name} is not active"}
            
            # Use key's algorithm if not specified
            if algorithm is None:
                algorithm = key["algorithm"]
            
            # Simulate encryption
            encrypted_data = self._simulate_encryption(data, algorithm)
            
            # Generate encryption ID
            encryption_id = f"enc_{int(time.time())}"
            
            # Store encrypted data
            self.encrypted_data[encryption_id] = {
                "encryption_id": encryption_id,
                "key_name": key_name,
                "algorithm": algorithm,
                "encrypted_data": encrypted_data,
                "encrypted_time": time.time(),
                "data_size": len(data)
            }
            
            # Update key usage
            key["last_used"] = time.time()
            key["usage_count"] += 1
            
            # Log encryption
            self._log_encryption_event("encrypt", key_name, algorithm, len(data))
            
            result = {
                "status": "success",
                "encryption_id": encryption_id,
                "key_name": key_name,
                "algorithm": algorithm,
                "encrypted_data": encrypted_data,
                "data_size": len(data),
                "message": "Data encrypted successfully"
            }
            
            return result
            
        except Exception as e:
            return {"status": "error", "message": f"Failed to encrypt data: {str(e)}"}
    
    def decrypt_data(self, encrypted_data: str, key_name: str) -> Dict[str, Any]:
        """
        Decrypt data using specified key.
        
        Args:
            encrypted_data: Encrypted data
            key_name: Name of the decryption key
            
        Returns:
            Decryption result
        """
        try:
            # Check if key exists
            if key_name not in self.keys:
                return {"status": "error", "message": f"Key {key_name} not found"}
            
            key = self.keys[key_name]
            
            # Check if key is active
            if not key["is_active"]:
                return {"status": "error", "message": f"Key {key_name} is not active"}
            
            # Simulate decryption
            decrypted_data = self._simulate_decryption(encrypted_data, key["algorithm"])
            
            # Update key usage
            key["last_used"] = time.time()
            key["usage_count"] += 1
            
            # Log decryption
            self._log_encryption_event("decrypt", key_name, key["algorithm"], len(decrypted_data))
            
            result = {
                "status": "success",
                "key_name": key_name,
                "algorithm": key["algorithm"],
                "decrypted_data": decrypted_data,
                "data_size": len(decrypted_data),
                "message": "Data decrypted successfully"
            }
            
            return result
            
        except Exception as e:
            return {"status": "error", "message": f"Failed to decrypt data: {str(e)}"}
    
    def create_digital_signature(self, data: str, key_name: str) -> Dict[str, Any]:
        """
        Create a digital signature for data.
        
        Args:
            data: Data to sign
            key_name: Name of the signing key
            
        Returns:
            Digital signature result
        """
        try:
            # Check if key exists
            if key_name not in self.keys:
                return {"status": "error", "message": f"Key {key_name} not found"}
            
            key = self.keys[key_name]
            
            # Check if key is active
            if not key["is_active"]:
                return {"status": "error", "message": f"Key {key_name} is not active"}
            
            # Check if key is asymmetric (required for digital signatures)
            if key["key_type"] != KeyType.ASYMMETRIC.value:
                return {"status": "error", "message": "Digital signatures require asymmetric keys"}
            
            # Create hash of data
            data_hash = hashlib.sha256(data.encode()).hexdigest()
            
            # Simulate digital signature creation
            signature = self._simulate_digital_signature(data_hash, key["private_key"])
            
            # Update key usage
            key["last_used"] = time.time()
            key["usage_count"] += 1
            
            # Log signature creation
            self._log_encryption_event("sign", key_name, key["algorithm"], len(data))
            
            result = {
                "status": "success",
                "key_name": key_name,
                "algorithm": key["algorithm"],
                "data_hash": data_hash,
                "signature": signature,
                "data_size": len(data),
                "message": "Digital signature created successfully"
            }
            
            return result
            
        except Exception as e:
            return {"status": "error", "message": f"Failed to create digital signature: {str(e)}"}
    
    def verify_digital_signature(self, data: bytes, signature: bytes, public_key: bytes) -> Dict[str, Any]:
        """
        Verify a digital signature.
        
        Args:
            data: Data to verify
            signature: Digital signature
            public_key: Public key for verification
            
        Returns:
            Signature verification result
        """
        try:
            # Check if key exists
            if key_name not in self.keys:
                return {"status": "error", "message": f"Key {key_name} not found"}
            
            key = self.keys[key_name]
            
            # Check if key is active
            if not key["is_active"]:
                return {"status": "error", "message": f"Key {key_name} is not active"}
            
            # Check if key is asymmetric
            if key["key_type"] != KeyType.ASYMMETRIC.value:
                return {"status": "error", "message": "Signature verification requires asymmetric keys"}
            
            # Create hash of data
            data_hash = hashlib.sha256(data.encode()).hexdigest()
            
            # Simulate signature verification
            is_valid = self._simulate_signature_verification(data_hash, signature, key["public_key"])
            
            # Update key usage
            key["last_used"] = time.time()
            key["usage_count"] += 1
            
            # Log signature verification
            self._log_encryption_event("verify", key_name, key["algorithm"], len(data))
            
            result = {
                "status": "success",
                "key_name": key_name,
                "algorithm": key["algorithm"],
                "data_hash": data_hash,
                "signature_valid": is_valid,
                "data_size": len(data),
                "message": "Signature is valid" if is_valid else "Signature is invalid"
            }
            
            return result
            
        except Exception as e:
            return {"status": "error", "message": f"Failed to verify digital signature: {str(e)}"}
    
    def rotate_key(self, key_name: str, new_algorithm: str = None) -> Dict[str, Any]:
        """
        Rotate an encryption key.
        
        Args:
            key_name: Name of the key to rotate
            new_algorithm: New algorithm (optional, uses same algorithm if not specified)
            
        Returns:
            Key rotation result
        """
        try:
            # Check if key exists
            if key_name not in self.keys:
                return {"status": "error", "message": f"Key {key_name} not found"}
            
            old_key = self.keys[key_name]
            
            # Use same algorithm if not specified
            if new_algorithm is None:
                new_algorithm = old_key["algorithm"]
            
            # Generate new key
            if old_key["key_type"] == KeyType.SYMMETRIC.value:
                new_key_result = self.generate_symmetric_key(f"{key_name}_new", new_algorithm)
            elif old_key["key_type"] == KeyType.ASYMMETRIC.value:
                new_key_result = self.generate_asymmetric_key_pair(f"{key_name}_new", new_algorithm)
            else:
                return {"status": "error", "message": f"Unsupported key type: {old_key['key_type']}"}
            
            if new_key_result["status"] != "success":
                return new_key_result
            
            # Deactivate old key
            old_key["is_active"] = False
            
            # Log key rotation
            self._log_encryption_event("rotate", key_name, new_algorithm, 0)
            
            result = {
                "status": "success",
                "old_key_name": key_name,
                "new_key_name": f"{key_name}_new",
                "old_algorithm": old_key["algorithm"],
                "new_algorithm": new_algorithm,
                "rotation_time": time.time(),
                "message": "Key rotated successfully"
            }
            
            return result
            
        except Exception as e:
            return {"status": "error", "message": f"Failed to rotate key: {str(e)}"}
    
    def get_key_info(self, key_name: str) -> Dict[str, Any]:
        """
        Get information about a key.
        
        Args:
            key_name: Name of the key
            
        Returns:
            Key information result
        """
        try:
            # Check if key exists
            if key_name not in self.keys:
                return {"status": "error", "message": f"Key {key_name} not found"}
            
            key = self.keys[key_name]
            
            # Remove sensitive information
            key_info = {
                "key_id": key["key_id"],
                "key_name": key["key_name"],
                "key_type": key["key_type"],
                "algorithm": key["algorithm"],
                "created_time": key["created_time"],
                "last_used": key["last_used"],
                "usage_count": key["usage_count"],
                "is_active": key["is_active"]
            }
            
            # Add public key for asymmetric keys
            if key["key_type"] == KeyType.ASYMMETRIC.value:
                key_info["public_key"] = key["public_key"]
            
            result = {
                "status": "success",
                "key_info": key_info
            }
            
            return result
            
        except Exception as e:
            return {"status": "error", "message": f"Failed to get key info: {str(e)}"}
    
    def list_keys(self) -> Dict[str, Any]:
        """
        List all keys.
        
        Returns:
            Keys list result
        """
        try:
            keys_list = []
            
            for key_name, key in self.keys.items():
                key_info = {
                    "key_name": key_name,
                    "key_type": key["key_type"],
                    "algorithm": key["algorithm"],
                    "created_time": key["created_time"],
                    "last_used": key["last_used"],
                    "usage_count": key["usage_count"],
                    "is_active": key["is_active"]
                }
                keys_list.append(key_info)
            
            result = {
                "status": "success",
                "keys": keys_list,
                "n_keys": len(keys_list)
            }
            
            return result
            
        except Exception as e:
            return {"status": "error", "message": f"Failed to list keys: {str(e)}"}
    
    def _simulate_encryption(self, data: str, algorithm: str) -> str:
        """Simulate encryption process."""
        # In real implementation, this would use actual encryption
        # For now, just encode the data
        encoded_data = base64.b64encode(data.encode()).decode()
        return f"{algorithm}:{encoded_data}"
    
    def _simulate_decryption(self, encrypted_data: str, algorithm: str) -> str:
        """Simulate decryption process."""
        # In real implementation, this would use actual decryption
        # For now, just decode the data
        try:
            algorithm_part, encoded_data = encrypted_data.split(":", 1)
            decoded_data = base64.b64decode(encoded_data).decode()
            return decoded_data
        except:
            return "Decryption failed"
    
    def _simulate_digital_signature(self, data_hash: str, private_key: str) -> str:
        """Simulate digital signature creation."""
        # In real implementation, this would use actual digital signature
        # For now, just create a hash of the data and key
        signature_data = f"{data_hash}:{private_key}"
        signature = hashlib.sha256(signature_data.encode()).hexdigest()
        return signature
    
    def _simulate_signature_verification(self, data_hash: str, signature: str, public_key: str) -> bool:
        """Simulate digital signature verification."""
        # In real implementation, this would use actual signature verification
        # For now, just recreate the signature and compare
        expected_signature = self._simulate_digital_signature(data_hash, public_key)
        return signature == expected_signature
    
    def _log_encryption_event(self, event_type: str, key_name: str, algorithm: str, data_size: int) -> None:
        """Log an encryption event."""
        event = {
            "timestamp": time.time(),
            "event_type": event_type,
            "key_name": key_name,
            "algorithm": algorithm,
            "data_size": data_size
        }
        self.encryption_history.append(event)
