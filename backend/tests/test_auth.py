"""
Test suite for Client Authentication & Credit Management - TDD
Validates registration, password hashing, token/session management, and credit deduction.
"""
import pytest
from app.core.auth import AuthService, User
from app.core.database import DatabaseService


@pytest.fixture
def auth_service(tmp_path):
    db_path = str(tmp_path / "test_auth.db")
    db = DatabaseService(db_path=db_path)
    return AuthService(db=db)


def test_user_registration_success(auth_service):
    user = auth_service.register(
        email="client@example.com",
        password="SecurePassword123!",
        full_name="Hamza Dev"
    )
    assert isinstance(user, User)
    assert user.email == "client@example.com"
    assert user.full_name == "Hamza Dev"
    assert user.credits == 0  # 0 free checks granted by default (pay-as-you-go)
    assert user.api_key.startswith("pk_live_")


def test_user_registration_duplicate_email(auth_service):
    auth_service.register("client@example.com", "Password123", "Client One")
    with pytest.raises(ValueError, match="EMAIL_ALREADY_EXISTS"):
        auth_service.register("client@example.com", "Password456", "Client Two")


def test_user_login_success_and_failure(auth_service):
    auth_service.register("login@example.com", "CorrectPass123", "Login User")
    
    # Successful login
    user = auth_service.authenticate("login@example.com", "CorrectPass123")
    assert user is not None
    assert user.email == "login@example.com"

    # Failed login with wrong password
    with pytest.raises(ValueError, match="INVALID_CREDENTIALS"):
        auth_service.authenticate("login@example.com", "WrongPassword")


def test_credit_deduction(auth_service):
    user = auth_service.register("credits@example.com", "Pass123", "Credit User")
    assert user.credits == 0
    auth_service.add_credits(user.id, amount=1000)
    
    updated_user = auth_service.deduct_credits(user.id, amount=25)
    assert updated_user.credits == 975


def test_credit_deduction_insufficient_balance(auth_service):
    user = auth_service.register("broke@example.com", "Pass123", "Broke User")
    assert user.credits == 0
    
    with pytest.raises(ValueError, match="INSUFFICIENT_CREDITS"):
        auth_service.deduct_credits(user.id, amount=5)


def test_add_credits_success_and_validation(auth_service):
    user = auth_service.register("topup@example.com", "Pass123", "Topup User")
    assert user.credits == 0
    topup_user = auth_service.add_credits(user.id, 250)
    assert topup_user.credits == 250
    with pytest.raises(ValueError, match="AMOUNT_MUST_BE_POSITIVE"):
        auth_service.add_credits(user.id, 0)
    with pytest.raises(ValueError, match="AMOUNT_MUST_BE_POSITIVE"):
        auth_service.add_credits(user.id, -10)
