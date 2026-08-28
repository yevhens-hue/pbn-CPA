"""
Configuration management for PBN Automation project.
Provides centralized configuration with environment variable support.
"""

import os
import logging
from dataclasses import dataclass, field
from typing import Optional, List
from pathlib import Path
from dotenv import load_dotenv


logger = logging.getLogger(__name__)


# Загрузка .env файла
load_dotenv()


@dataclass
class GoogleConfig:
    """Конфигурация Google API."""
    credentials: str = ""
    sheet_id: str = ""
    
    def __post_init__(self):
        if not self.credentials:
            self.credentials = os.getenv("GOOGLE_CREDENTIALS", "")
        if not self.sheet_id:
            self.sheet_id = os.getenv("SHEET_ID", "")
    
    @property
    def is_configured(self) -> bool:
        return bool(self.credentials)


@dataclass
class AIConfig:
    """Конфигурация AI сервисов."""
    gemini_api_key: str = ""
    groq_api_key: str = ""
    anthropic_api_key: str = ""
    openai_api_key: str = ""
    
    def __post_init__(self):
        if not self.gemini_api_key:
            self.gemini_api_key = os.getenv("GEMINI_API_KEY", "")
        if not self.groq_api_key:
            self.groq_api_key = os.getenv("GROQ_API_KEY", "")
        if not self.anthropic_api_key:
            self.anthropic_api_key = os.getenv("ANTHROPIC_API_KEY", "")
        if not self.openai_api_key:
            self.openai_api_key = os.getenv("OPENAI_API_KEY", "")
    
    @property
    def has_any_key(self) -> bool:
        return any([
            self.gemini_api_key,
            self.groq_api_key,
            self.anthropic_api_key,
            self.openai_api_key
        ])


@dataclass
class TelegramConfig:
    """Конфигурация Telegram."""
    bot_token: str = ""
    channel_id: str = ""
    
    def __post_init__(self):
        if not self.bot_token:
            self.bot_token = os.getenv("TELEGRAM_BOT_TOKEN", "")
        if not self.channel_id:
            self.channel_id = os.getenv("TELEGRAM_CHANNEL_ID", "")
    
    @property
    def is_configured(self) -> bool:
        return bool(self.bot_token)


@dataclass
class DatabaseConfig:
    """Конфигурация базы данных."""
    path: str = ".cache"
    max_age_hours: int = 24
    
    def __post_init__(self):
        if not self.path:
            self.path = os.getenv("DB_PATH", ".cache")
    
    @property
    def cache_dir(self) -> Path:
        return Path(self.path)


@dataclass
class SEOConfig:
    """Конфигурация SEO параметров."""
    default_lang: str = "en"
    target_geo: str = "IN"
    current_year: int = 2026
    
    def __post_init__(self):
        if not self.default_lang:
            self.default_lang = os.getenv("DEFAULT_LANG", "en")
        if not self.target_geo:
            self.target_geo = os.getenv("TARGET_GEO", "IN")
        if not self.current_year:
            self.current_year = int(os.getenv("CURRENT_YEAR", "2026"))


@dataclass
class Config:
    """
    Главная конфигурация проекта.
    Объединяет все настройки в одном месте.
    """
    google: GoogleConfig = field(default_factory=GoogleConfig)
    ai: AIConfig = field(default_factory=AIConfig)
    telegram: TelegramConfig = field(default_factory=TelegramConfig)
    database: DatabaseConfig = field(default_factory=DatabaseConfig)
    seo: SEOConfig = field(default_factory=SEOConfig)
    
    # Глобальные настройки
    debug: bool = False
    log_level: str = "INFO"
    
    def __post_init__(self):
        self.debug = os.getenv("DEBUG", "").lower() in ("1", "true", "yes")
        self.log_level = os.getenv("LOG_LEVEL", "INFO")
    
    @classmethod
    def from_env(cls) -> 'Config':
        """Создает конфигурацию из переменных окружения."""
        return cls(
            google=GoogleConfig(),
            ai=AIConfig(),
            telegram=TelegramConfig(),
            database=DatabaseConfig(),
            seo=SEOConfig()
        )
    
    def validate(self) -> List[str]:
        """
        Валидирует конфигурацию.
        
        Returns:
            Список ошибок (пустой если всё OK)
        """
        errors = []
        
        if not self.google.is_configured:
            errors.append("Google credentials not configured")
        
        if not self.ai.has_any_key:
            errors.append("No AI API keys configured")
        
        return errors
    
    def log_status(self) -> None:
        """Логирует статус конфигурации."""
        logger.info("=" * 50)
        logger.info("Configuration Status")
        logger.info("=" * 50)
        
        # Google
        google_status = "✅ Configured" if self.google.is_configured else "❌ Missing"
        logger.info(f"Google: {google_status}")
        
        if self.google.sheet_id:
            logger.info(f"  Sheet ID: {self.google.sheet_id[:20]}...")
        
        # AI
        ai_count = sum([
            bool(self.ai.gemini_api_key),
            bool(self.ai.groq_api_key),
            bool(self.ai.anthropic_api_key),
            bool(self.ai.openai_api_key)
        ])
        logger.info(f"AI Keys: {ai_count}/4 configured")
        
        # Telegram
        tg_status = "✅ Configured" if self.telegram.is_configured else "❌ Missing"
        logger.info(f"Telegram: {tg_status}")
        
        # SEO
        logger.info(f"Target: {self.seo.target_geo} | Lang: {self.seo.default_lang}")
        
        logger.info("=" * 50)


# Глобальный экземпляр конфигурации
_config: Optional[Config] = None


def get_config() -> Config:
    """
    Возвращает глобальный экземпляр конфигурации.
    Создает его при первом вызове.
    
    Returns:
        Глобальный объект Config
    """
    global _config
    if _config is None:
        _config = Config.from_env()
    return _config


def reload_config() -> Config:
    """Перезагружает конфигурацию из переменных окружения."""
    global _config
    _config = Config.from_env()
    return _config


# === Convenience accessors ===

def get_google_credentials() -> str:
    """Возвращает Google credentials из конфигурации."""
    return get_config().google.credentials


def get_sheet_id() -> str:
    """Возвращает ID Google Таблицы."""
    return get_config().google.sheet_id


def get_gemini_key() -> str:
    """Возвращает Gemini API ключ."""
    return get_config().ai.gemini_api_key


def get_groq_key() -> str:
    """Возвращает Groq API ключ."""
    return get_config().ai.groq_api_key


def get_telegram_token() -> str:
    """Возвращает Telegram bot token."""
    return get_config().telegram.bot_token


def get_target_geo() -> str:
    """Возвращает целевой гео."""
    return get_config().seo.target_geo
