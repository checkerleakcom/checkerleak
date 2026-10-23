"""
Auth API Router: Endpoints for client registration, login, email verification, and profile management.
"""
from typing import Optional
from fastapi import APIRouter, HTTPException, Header, Query, Request
from pydantic import BaseModel, Field
from app.core.auth import AuthService, User
from app.core.rate_limiter import AuthRateLimiter

auth_router = APIRouter(prefix="/v1/auth", tags=["Authentication"])
auth_service = AuthService()
auth_limiter = AuthRateLimiter()


class RegisterRequest(BaseModel):
    email: str = Field(..., example="client@company.com")
    password: str = Field(..., min_length=6, example="SecurePass123!")
    full_name: str = Field(..., example="Hamza Alami")
    referrer: Optional[str] = Field(None, max_length=512)
    landing_path: Optional[str] = Field("/", max_length=255)
    utm_source: Optional[str] = Field(None, max_length=64)
    session_id: Optional[str] = Field(None, max_length=64)


class LoginRequest(BaseModel):
    email: str = Field(..., example="client@company.com")
    password: str = Field(..., example="SecurePass123!")


class VerifyEmailRequest(BaseModel):
    token: str = Field(..., example="verification_token_string")


class ResendVerificationRequest(BaseModel):
    email: str = Field(..., example="client@company.com")


class ChangePasswordRequest(BaseModel):
    user_id: int = Field(..., example=1)
    current_password: str = Field(..., min_length=1)
    new_password: str = Field(..., min_length=6, example="NewSecurePass123!")


class RegenerateApiKeyRequest(BaseModel):
    user_id: int = Field(..., example=1)


class AuthResponse(BaseModel):
    user: User
    token: str
    message: str


def _get_client_ip(request: Request) -> str:
    """Extract real client IP address respecting reverse proxies."""
    forwarded = request.headers.get("X-Forwarded-For")
    if forwarded:
        return forwarded.split(",")[0].strip()
    return request.client.host if request.client else "127.0.0.1"


@auth_router.post("/register", response_model=AuthResponse)
def register_client(req: RegisterRequest, request: Request):
    """Register a new client, generate verification token, auto-generate API Key, and send verification email."""
    client_ip = _get_client_ip(request)
    is_allowed, _ = auth_limiter.check_register_allowed(client_ip)
    if not is_allowed:
        raise HTTPException(
            status_code=429,
            detail="Registration limit reached. Maximum 10 accounts per hour per IP.",
        )

    import hashlib
    from app.api.telemetry_router import classify_referrer

    ip = (
        request.headers.get("CF-Connecting-IP") or
        request.headers.get("X-Forwarded-For", "").split(",")[0].strip() or
        client_ip
    )
    ip_hash = hashlib.sha256(ip.encode("utf-8")).hexdigest()[:32] if ip else None
    country = request.headers.get("CF-IPCountry", "XX")[:8]
    if not country or country == "XX":
        country = request.headers.get("X-Country", "XX")[:8]

    # Referrer classification
    ref = req.referrer or request.headers.get("Referer", "")
    source_channel, source_engine = classify_referrer(ref)
    if req.utm_source:
        if source_channel == "DIRECT":
            source_channel = "CAMPAIGN"
        source_engine = req.utm_source

    landing_path = req.landing_path or "/"

    try:
        user = auth_service.register(
            email=req.email,
            password=req.password,
            full_name=req.full_name,
            registration_source=source_engine,
            source_channel=source_channel,
            country=country,
            landing_path=landing_path,
            ip_hash=ip_hash,
        )
        auth_limiter.record_register(client_ip)
        return AuthResponse(
            user=user,
            token=user.api_key,
            message="Account registered successfully. Please check your inbox to verify your email.",
        )
    except ValueError as ve:
        error_msg = str(ve)
        if error_msg == "EMAIL_ALREADY_EXISTS":
            raise HTTPException(status_code=409, detail="An account with this email already exists.")
        elif error_msg == "PASSWORD_TOO_SHORT":
            raise HTTPException(status_code=400, detail="Password must be at least 6 characters.")
        raise HTTPException(status_code=400, detail=error_msg)
    except Exception:
        raise HTTPException(status_code=500, detail="INTERNAL_REGISTRATION_ERROR")


@auth_router.post("/login", response_model=AuthResponse)
def login_client(req: LoginRequest, request: Request):
    """Authenticate client and return their active profile and credit balance."""
    client_ip = _get_client_ip(request)
    is_allowed, retry_after = auth_limiter.check_login_allowed(client_ip)
    if not is_allowed:
        raise HTTPException(
            status_code=429,
            detail=f"Account locked temporarily due to excessive failed attempts. Please retry in {retry_after} seconds.",
        )

    try:
        user = auth_service.authenticate(email=req.email, password=req.password)
        auth_limiter.record_login_success(client_ip)
        return AuthResponse(
            user=user,
            token=user.api_key,
            message="Login successful.",
        )
    except ValueError as ve:
        if str(ve) == "INVALID_CREDENTIALS":
            is_locked, lockout_sec = auth_limiter.record_login_failure(client_ip)
            if is_locked:
                raise HTTPException(
                    status_code=429,
                    detail=f"Too many failed login attempts. Access locked for {lockout_sec // 60} minutes.",
                )
            raise HTTPException(status_code=401, detail="Invalid email or password.")
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception:
        raise HTTPException(status_code=500, detail="INTERNAL_AUTH_ERROR")


@auth_router.get("/verify-email")
@auth_router.post("/verify-email")
def verify_email(
    token: Optional[str] = Query(None),
    payload: Optional[VerifyEmailRequest] = None,
):
    """
    Validates email verification token, marks user account as verified,
    and returns verified user profile.
    """
    token_str = (payload.token if payload else None) or token
    if not token_str:
        raise HTTPException(status_code=400, detail="Verification token is required.")

    try:
        user = auth_service.verify_email(token_str)
        return {
            "success": True,
            "message": "Email verified successfully! Your account is active with full access.",
            "user": user,
        }
    except ValueError as ve:
        err = str(ve)
        if err == "INVALID_OR_EXPIRED_TOKEN":
            raise HTTPException(status_code=400, detail="This verification link is invalid or has expired.")
        raise HTTPException(status_code=400, detail=err)
    except Exception:
        raise HTTPException(status_code=500, detail="Failed to verify email.")


@auth_router.post("/resend-verification")
def resend_verification(payload: ResendVerificationRequest):
    """Resends email verification token to user."""
    try:
        auth_service.resend_verification(payload.email)
        return {
            "success": True,
            "message": f"Verification email resent to {payload.email}. Please check your inbox and spam folder.",
        }
    except ValueError as ve:
        err = str(ve)
        if err == "ALREADY_VERIFIED":
            raise HTTPException(status_code=400, detail="This email address is already verified.")
        elif err == "USER_NOT_FOUND":
            # For security, we don't leak user existence
            return {
                "success": True,
                "message": f"If an account exists for {payload.email}, a verification link has been sent.",
            }
        raise HTTPException(status_code=400, detail=err)
    except Exception:
        raise HTTPException(status_code=500, detail="Failed to send verification email.")


@auth_router.get("/me", response_model=User)
def get_current_user_profile(
    user_id: int = Query(...),
    authorization: Optional[str] = Header(None),
):
    """
    Fetch client profile and real-time wallet credits.
    Protected against IDOR: API Key is only unmasked if the request carries valid Authorization.
    """
    user = auth_service.get_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found.")

    # Check if caller presented valid Bearer token for this user
    is_authorized = False
    if authorization:
        token = authorization.replace("Bearer ", "").strip()
        if token == user.api_key:
            is_authorized = True

    if not is_authorized:
        # Mask the secret API key to prevent IDOR data exfiltration while keeping UI responsive
        masked_key = (
            f"{user.api_key[:10]}...{user.api_key[-4:]}"
            if len(user.api_key) > 14
            else "pk_live_***"
        )
        return user.model_copy(update={"api_key": masked_key})

    return user


@auth_router.post("/change-password")
def change_password(
    payload: ChangePasswordRequest,
    authorization: Optional[str] = Header(None),
):
    """Change user password after verifying current credentials and optional session authorization."""
    user = auth_service.get_by_id(payload.user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found.")

    if authorization:
        token = authorization.replace("Bearer ", "").strip()
        if token != user.api_key:
            raise HTTPException(status_code=403, detail="Unauthorized session.")

    try:
        auth_service.change_password(
            user_id=payload.user_id,
            current_password=payload.current_password,
            new_password=payload.new_password,
        )
        return {
            "success": True,
            "message": "Password updated successfully. Please use your new password next time you log in.",
        }
    except ValueError as ve:
        err = str(ve)
        if err == "INVALID_CURRENT_PASSWORD":
            raise HTTPException(status_code=400, detail="The current password you entered is incorrect.")
        elif err == "PASSWORD_TOO_SHORT":
            raise HTTPException(status_code=400, detail="New password must be at least 6 characters.")
        raise HTTPException(status_code=400, detail=err)
    except Exception:
        raise HTTPException(status_code=500, detail="Failed to update password.")


@auth_router.post("/regenerate-api-key")
def regenerate_api_key(
    payload: RegenerateApiKeyRequest,
    authorization: Optional[str] = Header(None),
):
    """Regenerates a fresh API Key for the user and invalidates the previous key."""
    user = auth_service.get_by_id(payload.user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found.")

    if authorization:
        token = authorization.replace("Bearer ", "").strip()
        if token != user.api_key:
            raise HTTPException(status_code=403, detail="Unauthorized session.")

    try:
        updated_user = auth_service.regenerate_api_key(payload.user_id)
        return {
            "success": True,
            "message": "A new API Key has been generated. Ensure to update your integration scripts.",
            "api_key": updated_user.api_key,
            "user": updated_user,
        }
    except Exception:
        raise HTTPException(status_code=500, detail="Failed to regenerate API Key.")


