"""
Google API utilities for PBN Automation project.
Provides unified authentication and common operations for Google services.
"""

import os
import json
import logging
from pathlib import Path
from typing import Optional

# Google Auth - поддержка обоих вариантов
try:
    from google.oauth2 import service_account
    from google.auth.transport.requests import Request
    
    HAS_GOOGLE_AUTH = True
except ImportError:
    HAS_GOOGLE_AUTH = False
    # Fallback к старому oauth2client
    try:
        from oauth2client.service_account import ServiceAccountCredentials
    except ImportError:
        ServiceAccountCredentials = None

import gspread
from gspread import Spreadsheet, Worksheet


logger = logging.getLogger(__name__)


class GoogleAuthError(Exception):
    """Исключение при ошибке аутентификации Google."""
    pass


class GoogleAPIError(Exception):
    """Общее исключение для ошибок Google API."""
    pass


def get_credentials(
    credentials_path: Optional[str] = None,
    scope: Optional[list[str]] = None
) -> service_account.Credentials:
    """
    Загружает и возвращает Google service account credentials.
    
    Args:
        credentials_path: Путь к JSON файлу credentials (или имя переменной окружения)
        scope: OAuth scope для API
        
    Returns:
        Объект credentials для работы с Google API
        
    Raises:
        GoogleAuthError: Если не удалось получить credentials
    """
    if scope is None:
        scope = [
            "https://spreadsheets.google.com/feeds",
            "https://www.googleapis.com/auth/drive"
        ]
    
    # Попробовать загрузить из переменной окружения
    json_creds = os.getenv("GOOGLE_CREDENTIALS")
    
    # Если передан путь к файлу
    if credentials_path:
        creds_path = Path(credentials_path)
        if creds_path.exists():
            json_creds = str(creds_path)
    
    if not json_creds:
        raise GoogleAuthError("GOOGLE_CREDENTIALS not set in environment")
    
    # Определить способ загрузки
    creds = None
    
    if HAS_GOOGLE_AUTH:
        # Используем google-auth
        if os.path.exists(json_creds):
            # Это путь к файлу
            try:
                creds = service_account.Credentials.from_service_account_file(
                    json_creds,
                    scopes=scope
                )
            except Exception as e:
                raise GoogleAuthError(f"Failed to load credentials from file: {e}")
        else:
            # Это JSON строка
            try:
                creds_dict = json.loads(json_creds)
                creds = service_account.Credentials.from_service_account_info(
                    creds_dict,
                    scopes=scope
                )
            except json.JSONDecodeError as e:
                raise GoogleAuthError(f"Invalid JSON in GOOGLE_CREDENTIALS: {e}")
            except Exception as e:
                raise GoogleAuthError(f"Failed to load credentials from env: {e}")
    else:
        # Fallback к oauth2client
        if ServiceAccountCredentials is None:
            raise GoogleAuthError("Neither google-auth nor oauth2client available")
        
        if os.path.exists(json_creds):
            creds = ServiceAccountCredentials.from_json_keyfile_name(json_creds, scope)
        else:
            try:
                creds_dict = json.loads(json_creds)
                creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
            except Exception as e:
                raise GoogleAuthError(f"Failed to load credentials: {e}")
    
    return creds


def authorize_gspread(
    credentials_path: Optional[str] = None,
    scope: Optional[list[str]] = None
) -> gspread.Client:
    """
    Авторизует и возвращает gspread клиент.
    
    Args:
        credentials_path: Путь к JSON файлу credentials
        scope: OAuth scope
        
    Returns:
        Авторизованный gspread клиент
    """
    creds = get_credentials(credentials_path, scope)
    return gspread.authorize(creds)


def get_worksheet(
    spreadsheet_id: str,
    worksheet_name: str,
    credentials_path: Optional[str] = None
) -> Worksheet:
    """
    Получает рабочий лист из Google Таблицы.
    
    Args:
        spreadsheet_id: ID таблицы
        worksheet_name: Имя листа
        credentials_path: Путь к credentials
        
    Returns:
        Объект Worksheet
        
    Raises:
        GoogleAPIError: Если лист не найден
    """
    client = authorize_gspread(credentials_path)
    
    try:
        spreadsheet = client.open_by_key(spreadsheet_id)
        return spreadsheet.worksheet(worksheet_name)
    except gspread.exceptions.WorksheetNotFoundError:
        # Попробовать первый лист
        try:
            return spreadsheet.sheet1
        except Exception as e:
            raise GoogleAPIError(f"Worksheet '{worksheet_name}' not found: {e}")
    except Exception as e:
        raise GoogleAPIError(f"Error opening spreadsheet: {e}")


def get_all_records(
    spreadsheet_id: str,
    worksheet_name: str,
    credentials_path: Optional[str] = None
) -> list[dict]:
    """
    Получает все записи из рабочего листа.
    
    Args:
        spreadsheet_id: ID таблицы
        worksheet_name: Имя листа
        credentials_path: Путь к credentials
        
    Returns:
        Список записей в виде словарей
    """
    worksheet = get_worksheet(spreadsheet_id, worksheet_name, credentials_path)
    return worksheet.get_all_records()


def append_row(
    spreadsheet_id: str,
    worksheet_name: str,
    row: list,
    credentials_path: Optional[str] = None
) -> None:
    """
    Добавляет строку в рабочий лист.
    
    Args:
        spreadsheet_id: ID таблицы
        worksheet_name: Имя листа
        row: Список значений для строки
        credentials_path: Путь к credentials
    """
    worksheet = get_worksheet(spreadsheet_id, worksheet_name, credentials_path)
    worksheet.append_row(row)


def update_cell(
    spreadsheet_id: str,
    worksheet_name: str,
    row: int,
    col: int,
    value: str,
    credentials_path: Optional[str] = None
) -> None:
    """
    Обновляет значение в ячейке.
    
    Args:
        spreadsheet_id: ID таблицы
        worksheet_name: Имя листа
        row: Номер строки (1-based)
        col: Номер столбца (1-based)
        value: Значение для записи
        credentials_path: Путь к credentials
    """
    worksheet = get_worksheet(spreadsheet_id, worksheet_name, credentials_path)
    worksheet.update_cell(row, col, value)


def find_header_row(worksheet: Worksheet) -> list[str]:
    """
    Находит и возвращает заголовки таблицы.
    
    Args:
        worksheet: Рабочий лист
        
    Returns:
        Список заголовков столбцов
    """
    all_values = worksheet.get_all_values()
    if not all_values:
        return []
    
    # Берем первую строку как заголовки
    headers = [h.strip() if h.strip() else f"Column_{i}" 
               for i, h in enumerate(all_values[0])]
    return headers


def rows_to_dicts(worksheet: Worksheet) -> list[dict]:
    """
    Конвертирует строки таблицы в список словарей.
    
    Args:
        worksheet: Рабочий лист
        
    Returns:
        Список словарей с данными
    """
    headers = find_header_row(worksheet)
    all_values = worksheet.get_all_values()
    
    if not all_values or len(all_values) < 2:
        return []
    
    data_rows = all_values[1:]
    result = []
    
    for row in data_rows:
        record = {}
        for i, header in enumerate(headers):
            if i < len(row):
                record[header] = row[i]
            else:
                record[header] = ""
        result.append(record)
    
    return result


# === Compatibility wrappers ===

class ServiceAccountCredentialsCompat:
    """
    Compatibility wrapper for google-auth with gspread.
    Обеспечивает обратную совместимость сoauth2client.
    """
    _cache = {}
    
    @staticmethod
    def from_json_keyfile_dict(creds_dict: dict, scope: list[str]):
        """Создает credentials из словаря."""
        if not HAS_GOOGLE_AUTH:
            if ServiceAccountCredentials:
                return ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
            raise GoogleAuthError("No auth library available")
        
        creds = service_account.Credentials.from_service_account_info(
            creds_dict, scopes=list(scope)
        )
        return _AuthWrapper(creds)
    
    @staticmethod
    def from_json_keyfile_name(filename: str, scope: list[str]):
        """Создает credentials из файла."""
        if not HAS_GOOGLE_AUTH:
            if ServiceAccountCredentials:
                return ServiceAccountCredentials.from_json_keyfile_name(filename, scope)
            raise GoogleAuthError("No auth library available")
        
        creds = service_account.Credentials.from_service_account_file(
            filename, scopes=list(scope)
        )
        return _AuthWrapper(creds)


class _AuthWrapper:
    """Wrapper to make google-auth credentials compatible with gspread."""
    
    def __init__(self, creds):
        self._creds = creds
    
    def refresh(self, request):
        self._creds.refresh(request)
    
    @property
    def access_token(self):
        return self._creds.token


# Export compatibility class
if HAS_GOOGLE_AUTH:
    ServiceAccountCredentials = ServiceAccountCredentialsCompat
