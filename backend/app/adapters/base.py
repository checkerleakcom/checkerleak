"""
Base Platform Adapter Interface & Immutable Result Models.
"""
from abc import ABC, abstractmethod
from enum import Enum
from typing import Optional, Dict, Any
from pydantic import BaseModel, ConfigDict
from app.core.normalizer import NormalizedPhone


class PlatformType(str, Enum):
    WHATSAPP = "WHATSAPP"
    TELEGRAM = "TELEGRAM"
    IMESSAGE = "IMESSAGE"
    RCS = "RCS"
    VIBER = "VIBER"
    LINE = "LINE"
    FACEBOOK = "FACEBOOK"
    INSTAGRAM = "INSTAGRAM"
    LINKEDIN = "LINKEDIN"
    BINANCE = "BINANCE"


class PlatformCheckResult(BaseModel):
    """Immutable result for a platform verification query."""
    model_config = ConfigDict(frozen=True)

    platform: PlatformType
    is_registered: bool
    confidence_score: int  # 0 to 100
    account_type: Optional[str] = None  # e.g., 'PERSONAL', 'BUSINESS'
    avatar_url: Optional[str] = None
    has_avatar: bool = False
    details: Dict[str, Any] = {}
    error: Optional[str] = None


class BasePlatformAdapter(ABC):
    """Abstract contract for platform-specific verifiers."""

    @abstractmethod
    def check(self, phone: NormalizedPhone) -> PlatformCheckResult:
        """Run passive account verification against the platform."""
        pass
