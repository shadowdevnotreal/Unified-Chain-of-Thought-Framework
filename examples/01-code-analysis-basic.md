# Example 1: Basic Code Analysis with `cot`

**Scenario:** You have a simple authentication function and want to review it for issues.

**Intensity Level:** Standard (`cot`) - 4K tokens

---

## The Code

```python
def authenticate_user(username, password):
    user = db.query(f"SELECT * FROM users WHERE username = '{username}'")
    if user and user.password == password:
        return True
    return False
```

---

## Your Prompt

```bash
cot review this authentication function for security and best practices
```

---

## Expected CoT Output

```
╔═══════════════════════════════════════════════════════════════
║ LISTEN Phase
╚═══════════════════════════════════════════════════════════════

Task: Review authentication function for security and best practices
Code provided: Python function with database query and password check
Context: Authentication mechanism - critical security component

╔═══════════════════════════════════════════════════════════════
║ THINK Phase
╚═══════════════════════════════════════════════════════════════

Breaking down the analysis:
1. Database query method - using string formatting
2. Password comparison - plain text comparison
3. Return logic - boolean based on user existence and password match
4. Error handling - none visible
5. Input validation - none visible

Identifying components:
- Database interaction pattern
- Authentication logic
- Security implications

╔═══════════════════════════════════════════════════════════════
║ REASON Phase
╚═══════════════════════════════════════════════════════════════

Critical Security Issues Identified:

1. **SQL Injection Vulnerability** ⚠️ CRITICAL
   - Using f-string for SQL query construction
   - Direct username insertion without sanitization
   - Attack vector: username = "' OR '1'='1' --"

2. **Plain Text Password Comparison** ⚠️ CRITICAL
   - Passwords should be hashed, never stored or compared as plain text
   - Violates fundamental security principles
   - Exposes user credentials

3. **Missing Input Validation** ⚠️ HIGH
   - No checks for None, empty strings, or malicious input
   - No length validation
   - No type checking

4. **No Error Handling** ⚠️ MEDIUM
   - Database errors will crash the function
   - No logging of failed attempts
   - No rate limiting consideration

Best Practice Violations:
- ❌ Not using parameterized queries
- ❌ Not using password hashing (bcrypt, argon2)
- ❌ No timing attack protection
- ❌ No account lockout mechanism

╔═══════════════════════════════════════════════════════════════
║ RESPOND Phase
╚═══════════════════════════════════════════════════════════════

Summary: This authentication function has CRITICAL security vulnerabilities
that must be addressed before deployment.

Recommended Secure Implementation:

```python
import bcrypt
from typing import Optional

def authenticate_user(username: str, password: str) -> bool:
    """
    Securely authenticate a user with hashed password comparison.

    Args:
        username: User's username
        password: User's plain text password (will be compared to hash)

    Returns:
        bool: True if authentication successful, False otherwise
    """
    # Input validation
    if not username or not password:
        return False

    if len(username) > 255 or len(password) > 255:
        return False

    try:
        # Parameterized query prevents SQL injection
        user = db.query(
            "SELECT * FROM users WHERE username = %s",
            (username,)
        )

        if not user:
            # Use constant-time comparison to prevent timing attacks
            bcrypt.checkpw(b"dummy", bcrypt.hashpw(b"dummy", bcrypt.gensalt()))
            return False

        # Compare password hash securely
        password_bytes = password.encode('utf-8')
        stored_hash = user.password_hash.encode('utf-8')

        return bcrypt.checkpw(password_bytes, stored_hash)

    except Exception as e:
        # Log error but don't expose details to caller
        logger.error(f"Authentication error: {e}")
        return False
```

Priority Actions:
1. ⚠️  IMMEDIATE: Replace f-string SQL with parameterized queries
2. ⚠️  IMMEDIATE: Implement password hashing (bcrypt/argon2)
3. ⚠️  HIGH: Add input validation
4. ⚠️  HIGH: Add error handling and logging
5. 📋 MEDIUM: Implement rate limiting
6. 📋 MEDIUM: Add account lockout after failed attempts

Confidence Level: High (99%)
Risk Assessment: Current code is NOT production-ready
```

---

## Key Takeaways

**Standard `cot` is perfect for:**
- ✅ Code reviews
- ✅ Security audits of single functions
- ✅ Quick analysis tasks
- ✅ Identifying obvious issues

**Processing time:** ~5-10 seconds

**Output quality:** Comprehensive for straightforward analysis tasks
