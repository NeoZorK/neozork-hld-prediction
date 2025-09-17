# 🔐 Pocket Hedge Fund Authentication Documentation

## 🎯 **Authentication Overview**

The Pocket Hedge Fund uses **JWT-based authentication** with comprehensive security features including password hashing, multi-factor authentication, and role-based access control. The authentication system is **80% functional** with complete user management and token validation.

**Authentication Type**: JWT Bearer Token  
**Password Security**: Bcrypt with salt rounds 12  
**Token Expiry**: 30 minutes (access), 7 days (refresh)  
**MFA Support**: TOTP-based multi-factor authentication  
**Role System**: Admin, Investor, Manager roles  

---

## 🔑 **Authentication Flow**

### **1. User Registration**
```
User → POST /api/v1/auth/register → Validate Data → Hash Password → Create User → Return Success
```

### **2. User Login**
```
User → POST /api/v1/auth/login → Validate Credentials → Generate JWT → Return Token
```

### **3. Token Validation**
```
Request → Extract Token → Validate JWT → Check Expiry → Verify User → Allow Access
```

### **4. Token Refresh**
```
Request → Validate Refresh Token → Generate New Access Token → Return New Token
```

---

## 👤 **User Management**

### **User Registration**
```http
POST /api/v1/auth/register
Content-Type: application/json

{
  "email": "user@example.com",
  "username": "username",
  "password": "SecurePassword123!",
  "first_name": "John",
  "last_name": "Doe",
  "phone": "+1234567890",
  "country": "US"
}
```

**Password Requirements:**
- Minimum 8 characters
- At least 1 uppercase letter
- At least 1 lowercase letter
- At least 1 number
- At least 1 special character

**Response:**
```json
{
  "success": true,
  "message": "User registered successfully",
  "user": {
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "email": "user@example.com",
    "username": "username",
    "first_name": "John",
    "last_name": "Doe",
    "kyc_status": "pending",
    "role": "investor",
    "is_active": true,
    "created_at": "2025-01-05T10:00:00Z"
  }
}
```

### **User Login**
```http
POST /api/v1/auth/login
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "SecurePassword123!"
}
```

**Response:**
```json
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "refresh_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "token_type": "bearer",
  "expires_in": 1800,
  "user": {
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "email": "user@example.com",
    "username": "username",
    "first_name": "John",
    "last_name": "Doe",
    "role": "investor",
    "kyc_status": "pending",
    "mfa_enabled": false
  }
}
```

### **Token Refresh**
```http
POST /api/v1/auth/refresh
Content-Type: application/json

{
  "refresh_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
```

**Response:**
```json
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "token_type": "bearer",
  "expires_in": 1800
}
```

### **User Logout**
```http
POST /api/v1/auth/logout
Authorization: Bearer <access_token>
```

**Response:**
```json
{
  "message": "Successfully logged out"
}
```

---

## 🔐 **JWT Token System**

### **Token Structure**
```json
{
  "header": {
    "alg": "HS256",
    "typ": "JWT"
  },
  "payload": {
    "sub": "user_id",
    "email": "user@example.com",
    "username": "username",
    "role": "investor",
    "iat": 1641384000,
    "exp": 1641385800,
    "jti": "token_id"
  },
  "signature": "HMACSHA256(base64UrlEncode(header) + '.' + base64UrlEncode(payload), secret)"
}
```

### **Token Configuration**
```python
JWT_CONFIG = {
    "secret_key": "your-secret-key",
    "algorithm": "HS256",
    "access_token_expire_minutes": 30,
    "refresh_token_expire_days": 7,
    "issuer": "neozork-pocket-hedge-fund"
}
```

### **Token Validation**
```python
def validate_token(token: str) -> dict:
    """Validate JWT token and return payload."""
    try:
        payload = jwt.decode(
            token,
            JWT_CONFIG["secret_key"],
            algorithms=[JWT_CONFIG["algorithm"]],
            options={"verify_exp": True}
        )
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")
```

---

## 🛡️ **Password Security**

### **Password Hashing**
```python
import bcrypt

def hash_password(password: str) -> str:
    """Hash password using bcrypt."""
    salt = bcrypt.gensalt(rounds=12)
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed.decode('utf-8')

def verify_password(password: str, hashed: str) -> bool:
    """Verify password against hash."""
    return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))
```

### **Password Requirements**
- **Minimum Length**: 8 characters
- **Complexity**: Mixed case, numbers, special characters
- **Common Passwords**: Blocked (top 1000 common passwords)
- **History**: Cannot reuse last 5 passwords
- **Expiry**: 90 days (optional)

### **Password Reset**
```http
POST /api/v1/auth/forgot-password
Content-Type: application/json

{
  "email": "user@example.com"
}
```

**Response:**
```json
{
  "message": "Password reset email sent",
  "reset_token": "reset-token-uuid"
}
```

```http
POST /api/v1/auth/reset-password
Content-Type: application/json

{
  "reset_token": "reset-token-uuid",
  "new_password": "NewSecurePassword123!"
}
```

---

## 🔒 **Multi-Factor Authentication (MFA)**

### **Enable MFA**
```http
POST /api/v1/auth/mfa/enable
Authorization: Bearer <access_token>
```

**Response:**
```json
{
  "secret": "JBSWY3DPEHPK3PXP",
  "qr_code": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAA...",
  "backup_codes": [
    "12345678",
    "87654321",
    "11223344"
  ]
}
```

### **Verify MFA Setup**
```http
POST /api/v1/auth/mfa/verify
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "code": "123456"
}
```

### **MFA Login**
```http
POST /api/v1/auth/login
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "SecurePassword123!",
  "mfa_code": "123456"
}
```

---

## 👥 **Role-Based Access Control (RBAC)**

### **User Roles**
```python
class UserRole(Enum):
    ADMIN = "admin"           # Full system access
    MANAGER = "manager"       # Fund management access
    INVESTOR = "investor"     # Investment access
    VIEWER = "viewer"         # Read-only access
```

### **Permission Matrix**
| Role | Funds | Investors | Portfolio | Transactions | Admin |
|------|-------|-----------|-----------|--------------|-------|
| Admin | CRUD | CRUD | CRUD | CRUD | Yes |
| Manager | CRUD | Read | CRUD | CRUD | No |
| Investor | Read | Own | Own | Own | No |
| Viewer | Read | Read | Read | Read | No |

### **Permission Checking**
```python
def check_permission(user_role: str, resource: str, action: str) -> bool:
    """Check if user has permission for action on resource."""
    permissions = {
        "admin": ["*"],  # All permissions
        "manager": ["funds:crud", "investors:read", "portfolio:crud"],
        "investor": ["funds:read", "investors:own", "portfolio:own"],
        "viewer": ["*:read"]  # Read-only
    }
    
    user_perms = permissions.get(user_role, [])
    required_perm = f"{resource}:{action}"
    
    return "*" in user_perms or required_perm in user_perms
```

---

## 🔍 **Session Management**

### **Session Tracking**
```python
class UserSession:
    def __init__(self, user_id: str, token: str):
        self.user_id = user_id
        self.token = token
        self.created_at = datetime.now()
        self.last_activity = datetime.now()
        self.ip_address = None
        self.user_agent = None
```

### **Session Validation**
```python
async def validate_session(token: str) -> UserSession:
    """Validate user session and update activity."""
    payload = validate_token(token)
    user_id = payload["sub"]
    
    session = await get_user_session(user_id, token)
    if not session:
        raise HTTPException(status_code=401, detail="Invalid session")
    
    # Update last activity
    session.last_activity = datetime.now()
    await update_session(session)
    
    return session
```

### **Session Cleanup**
```python
async def cleanup_expired_sessions():
    """Clean up expired sessions."""
    expired_sessions = await get_expired_sessions()
    for session in expired_sessions:
        await revoke_session(session.token)
```

---

## 🚨 **Security Features**

### **Rate Limiting**
```python
# Login attempts
LOGIN_RATE_LIMIT = "5/minute"
REGISTER_RATE_LIMIT = "3/minute"
PASSWORD_RESET_RATE_LIMIT = "2/hour"

# API requests
API_RATE_LIMIT = "100/minute"
```

### **Account Lockout**
```python
class AccountLockout:
    def __init__(self):
        self.max_attempts = 5
        self.lockout_duration = 900  # 15 minutes
    
    async def check_lockout(self, email: str) -> bool:
        """Check if account is locked."""
        attempts = await get_failed_attempts(email)
        return attempts >= self.max_attempts
```

### **Suspicious Activity Detection**
```python
async def detect_suspicious_activity(user_id: str, ip_address: str):
    """Detect suspicious login patterns."""
    recent_logins = await get_recent_logins(user_id, hours=24)
    
    # Check for unusual IP addresses
    if ip_address not in [login.ip for login in recent_logins]:
        await log_suspicious_activity(user_id, "unusual_ip", ip_address)
    
    # Check for rapid login attempts
    if len(recent_logins) > 10:
        await log_suspicious_activity(user_id, "rapid_logins", len(recent_logins))
```

---

## 📊 **Audit Logging**

### **Authentication Events**
```python
class AuthEvent(Enum):
    LOGIN_SUCCESS = "login_success"
    LOGIN_FAILED = "login_failed"
    LOGOUT = "logout"
    PASSWORD_CHANGE = "password_change"
    MFA_ENABLED = "mfa_enabled"
    MFA_DISABLED = "mfa_disabled"
    ACCOUNT_LOCKED = "account_locked"
    SUSPICIOUS_ACTIVITY = "suspicious_activity"
```

### **Audit Log Entry**
```python
async def log_auth_event(event: AuthEvent, user_id: str, details: dict):
    """Log authentication event."""
    audit_entry = {
        "user_id": user_id,
        "action": event.value,
        "resource_type": "authentication",
        "details": details,
        "ip_address": get_client_ip(),
        "user_agent": get_user_agent(),
        "timestamp": datetime.now()
    }
    await create_audit_log(audit_entry)
```

---

## 🔧 **Configuration**

### **Environment Variables**
```bash
# JWT Configuration
JWT_SECRET_KEY=your-secret-key-here
JWT_ALGORITHM=HS256
JWT_ACCESS_TOKEN_EXPIRE_MINUTES=30
JWT_REFRESH_TOKEN_EXPIRE_DAYS=7

# Password Security
BCRYPT_ROUNDS=12
PASSWORD_MIN_LENGTH=8
PASSWORD_EXPIRY_DAYS=90

# Rate Limiting
LOGIN_RATE_LIMIT=5/minute
API_RATE_LIMIT=100/minute

# MFA Configuration
MFA_ISSUER=NeoZork Pocket Hedge Fund
MFA_WINDOW=1
```

### **Security Headers**
```python
SECURITY_HEADERS = {
    "X-Content-Type-Options": "nosniff",
    "X-Frame-Options": "DENY",
    "X-XSS-Protection": "1; mode=block",
    "Strict-Transport-Security": "max-age=31536000; includeSubDomains",
    "Content-Security-Policy": "default-src 'self'"
}
```

---

## 🚀 **Quick Start**

### **Setup Authentication**
```python
from src.pocket_hedge_fund.auth.auth_manager import AuthManager

# Initialize auth manager
auth_manager = AuthManager()

# Register user
user = await auth_manager.register_user(
    email="user@example.com",
    username="username",
    password="SecurePassword123!",
    first_name="John",
    last_name="Doe"
)

# Login user
tokens = await auth_manager.login_user(
    email="user@example.com",
    password="SecurePassword123!"
)
```

### **Protect API Endpoints**
```python
from fastapi import Depends, HTTPException
from src.pocket_hedge_fund.auth.auth_manager import get_current_user

@app.get("/api/v1/funds/")
async def get_funds(current_user: dict = Depends(get_current_user)):
    """Get funds - requires authentication."""
    return await get_user_funds(current_user["id"])
```

---

## 📚 **Additional Resources**

- **API Documentation**: [API Documentation](api/)
- **Database Schema**: [Database Documentation](database/)
- **Security Guide**: [Security Documentation](security/)
- **Deployment Guide**: [Deployment Documentation](deployment/)

---

**Last Updated**: January 2025  
**Authentication Version**: 1.0.0  
**Status**: 80% Functional  
**Security Level**: High
