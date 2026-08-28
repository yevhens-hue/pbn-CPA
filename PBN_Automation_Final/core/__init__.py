"""
PBN Automation Core Module

Этот модуль содержит основные утилиты и функции для работы проекта.
Рекомендуется использовать вместо дублирующегося кода в корневой директории.

Основные компоненты:
- utils: Утилиты общего назначения (логирование, файлы)
- google_utils: Работа с Google API (Sheets, Drive)
- wordpress: WordPress REST API клиент
- config: Управление конфигурацией
- seo_optimizer: SEO утилиты (schema, CTA)
- indexing_api: Google Indexing API

Пример использования:
    from core import setup_logger, get_config, WordPressAPI
    
    # Логирование
    logger = setup_logger(__name__)
    
    # Конфигурация
    config = get_config()
    
    # WordPress
    wp = WordPressAPI(site_url, username, password)
    wp.create_post(title, content)
"""

# Core utilities
from .utils import (
    setup_logger,
    get_project_root,
    find_file,
    ensure_dir,
    safe_json_load,
    safe_json_dump,
    get_timestamp,
    mask_sensitive,
)

# Google utilities
from .google_utils import (
    get_credentials,
    authorize_gspread,
    get_worksheet,
    get_all_records,
    append_row,
    update_cell,
    rows_to_dicts,
    GoogleAuthError,
    GoogleAPIError,
)

# WordPress utilities
from .wordpress import (
    WordPressAPI,
    WordPressError,
    publish_post,
    find_post_by_title,
)

# Configuration
from .config import (
    Config,
    get_config,
    reload_config,
    get_google_credentials,
    get_sheet_id,
    get_gemini_key,
    get_groq_key,
    get_telegram_token,
    get_target_geo,
    GoogleConfig,
    AIConfig,
    TelegramConfig,
    SEOConfig,
)

# SEO utilities
from .seo_optimizer import (
    generate_game_schema,
    generate_faq_schema,
    generate_review_schema,
    generate_howto_schema,
    get_updated_title,
    generate_whatsapp_cta,
    get_random_indian_city,
)

# Indexing API
from .indexing_api import (
    submit_to_google_indexing,
)

# Re-export commonly used items
__all__ = [
    # Utils
    "setup_logger",
    "get_project_root",
    "find_file",
    "ensure_dir",
    "safe_json_load",
    "safe_json_dump",
    "get_timestamp",
    "mask_sensitive",
    # Google
    "get_credentials",
    "authorize_gspread",
    "get_worksheet",
    "get_all_records",
    "append_row",
    "update_cell",
    "rows_to_dicts",
    "GoogleAuthError",
    "GoogleAPIError",
    # WordPress
    "WordPressAPI",
    "WordPressError",
    "publish_post",
    "find_post_by_title",
    # Config
    "Config",
    "get_config",
    "reload_config",
    "get_google_credentials",
    "get_sheet_id",
    "get_gemini_key",
    "get_groq_key",
    "get_telegram_token",
    "get_target_geo",
    "GoogleConfig",
    "AIConfig",
    "TelegramConfig",
    "SEOConfig",
    # SEO
    "generate_game_schema",
    "generate_faq_schema",
    "generate_review_schema",
    "generate_howto_schema",
    "get_updated_title",
    "generate_whatsapp_cta",
    "get_random_indian_city",
    # Indexing
    "submit_to_google_indexing",
]

__version__ = "2.0.0"
