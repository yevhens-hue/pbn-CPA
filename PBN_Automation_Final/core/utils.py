"""
Core utilities for PBN Automation project.
Provides unified logging, error handling, and common utilities.
"""

from __future__ import annotations
import logging
import sys
import os
from pathlib import Path
from typing import Any, Optional, Union
from datetime import datetime


def setup_logger(
    name: str,
    level: int = logging.INFO,
    log_file: Optional[str] = None
) -> logging.Logger:
    """
    Настраивает единый формат логов для всех модулей проекта.
    
    Args:
        name: Имя логера (обычно __name__)
        level: Уровень логирования
        log_file: Опциональный путь для записи логов в файл
        
    Returns:
        Настроенный логер
    """
    logger = logging.getLogger(name)
    logger.setLevel(level)
    
    # Избегаем дублирования обработчиков
    if logger.handlers:
        return logger
    
    # Формат логов
    formatter = logging.Formatter(
        '%(asctime)s | %(levelname)-8s | %(name)s | %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # Консольный обработчик
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(level)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    # Файловый обработчик (если указан)
    if log_file:
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(level)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    
    return logger


def get_project_root() -> Path:
    """Возвращает корневую директорию проекта."""
    # Поднимаемся от текущего файла до корня
    current = Path(__file__).parent
    
    # Ищем директорию с PBN_Automation_Final или games-income
    while current != current.parent:
        if (current / "PBN_Automation_Final").exists() or (current / "games-income").exists():
            return current
        current = current.parent
    
    # Fallback - возвращаем текущую директорию
    return Path.cwd()


def find_file(filename: str, search_paths: Optional[list[str]] = None) -> Optional[Path]:
    """
    Ищет файл в нескольких директориях.
    
    Args:
        filename: Имя файла для поиска
        search_paths: Список директорий для поиска (относительно корня проекта)
        
    Returns:
        Путь к файлу или None, если не найден
    """
    root = get_project_root()
    
    # Стандартные пути поиска
    default_paths = [
        filename,
        f"PBN_Automation_Final/{filename}",
        f"core/{filename}",
        f"data/{filename}",
        filename,
    ]
    
    search_paths = search_paths or default_paths
    
    for path in search_paths:
        full_path = root / path
        if full_path.exists():
            return full_path
    
    return None


def ensure_dir(path: Union[str, Path]) -> Path:
    """Создает директорию, если она не существует."""
    path = Path(path)
    path.mkdir(parents=True, exist_ok=True)
    return path


def safe_json_load(file_path: Union[str, Path], default: Any = None) -> Any:
    """
    Безопасная загрузка JSON файла с обработкой ошибок.
    
    Args:
        file_path: Путь к JSON файлу
        default: Значение по умолчанию в случае ошибки
        
    Returns:
        Загруженные данные или значение по умолчанию
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        logger = logging.getLogger(__name__)
        logger.warning(f"File not found: {file_path}")
        return default
    except json.JSONDecodeError as e:
        logger = logging.getLogger(__name__)
        logger.error(f"Invalid JSON in {file_path}: {e}")
        return default
    except Exception as e:
        logger = logging.getLogger(__name__)
        logger.error(f"Error loading {file_path}: {e}")
        return default


def safe_json_dump(data: Any, file_path: Union[str, Path], indent: int = 2) -> bool:
    """
    Безопасная запись JSON файла с обработкой ошибок.
    
    Args:
        data: Данные для записи
        file_path: Путь к файлу
        indent: Отступ для форматирования
        
    Returns:
        True в случае успеха, False в случае ошибки
    """
    try:
        file_path = Path(file_path)
        file_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=indent, ensure_ascii=False)
        return True
    except Exception as e:
        logger = logging.getLogger(__name__)
        logger.error(f"Error saving {file_path}: {e}")
        return False


def get_timestamp(format: str = "%Y-%m-%d %H:%M:%S") -> str:
    """Возвращает текущую временную метку в указанном формате."""
    return datetime.now().strftime(format)


def mask_sensitive(text: str, visible_chars: int = 4) -> str:
    """
    Маскирует конфиденциальные данные для логирования.
    
    Args:
        text: Текст для маскирования
        visible_chars: Количество видимых символов с конца
        
    Returns:
        Замаскированный текст
    """
    if not text or len(text) <= visible_chars:
        return "*" * len(text)
    
    return "*" * (len(text) - visible_chars) + text[-visible_chars:]


# Устаревшие импорты для обратной совместимости
import json
