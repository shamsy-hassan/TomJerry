# JWT helper functions
# ============================================================
# File: backend/utils/jwt_helper.py
# Description:
#   This module handles the creation, decoding, and verification
#   of JSON Web Tokens (JWT) for user authentication.
#   It provides helper functions for securely encoding user data
#   into tokens and verifying them during protected API calls.
# ============================================================

import jwt
import datetime
from flask import current_app

# ============================================================
# SECTION 1: JWT Configuration
# ------------------------------------------------------------
# Here we define default configurations for token behavior.
# - SECRET_KEY is loaded from Flask app config.
# - ALGORITHM defines the encryption type for the token.
# ============================================================

DEFAULT_ALGORITHM = "HS256"
DEFAULT_EXPIRY_MINUTES = 60  # Tokens valid for 1 hour


# ============================================================
# SECTION 2: Token Encoding (Generate JWT)
# ------------------------------------------------------------
# This function takes in user data (like user_id, username, etc.)
# and encodes it into a signed JWT string.
# ============================================================

def encode_token(payload, expires_in=DEFAULT_EXPIRY_MINUTES):
    """
    Generate a JWT token with expiration.
    
    :param payload: Dictionary of data to encode (e.g., {'user_id': 1})
    :param expires_in: Expiration time in minutes (default: 60)
    :return: Encoded JWT token (string)
    """
    secret_key = current_app.config.get("SECRET_KEY", "change-me")
    expiry = datetime.datetime.utcnow() + datetime.timedelta(minutes=expires_in)
    payload["exp"] = expiry  # Attach expiration to token

    token = jwt.encode(payload, secret_key, algorithm=DEFAULT_ALGORITHM)
    print(f"[JWT] Token generated for payload={payload}")
    return token


# ============================================================
# SECTION 3: Token Decoding (Verify JWT)
# ------------------------------------------------------------
# This function decodes the token and verifies its validity.
# It raises an exception if the token is expired or invalid.
# ============================================================

def decode_token(token):
    """
    Decode and validate a JWT token.
    
    :param token: JWT string to decode
    :return: Decoded payload dictionary if valid, otherwise None
    """
    secret_key = current_app.config.get("SECRET_KEY", "change-me")

    try:
        decoded = jwt.decode(token, secret_key, algorithms=[DEFAULT_ALGORITHM])
        print(f"[JWT] Token decoded successfully for user_id={decoded.get('user_id')}")
        return decoded
    except jwt.ExpiredSignatureError:
        print("[JWT] ❌ Token expired.")
        return None
    except jwt.InvalidTokenError:
        print("[JWT] ❌ Invalid token.")
        return None


# ============================================================
# SECTION 4: Helper - Token Validation for API Routes
# ------------------------------------------------------------
# This helper verifies a token (usually passed in headers)
# and extracts the payload for authenticated endpoints.
# ============================================================

def validate_request_token(request):
    """
    Validate a JWT token passed in request headers.
    
    Expected Header: Authorization: Bearer <token>
    :param request: Flask request object
    :return: Decoded payload if valid, else None
    """
    auth_header = request.headers.get("Authorization")
    if not auth_header:
        print("[JWT] Missing Authorization header.")
        return None

    parts = auth_header.split()
    if len(parts) != 2 or parts[0].lower() != "bearer":
        print("[JWT] Invalid Authorization header format.")
        return None

    token = parts[1]
    return decode_token(token)
