"""
WordPress API utilities for PBN Automation project.
Provides unified interface for WordPress operations.
"""

import base64
import logging
from typing import Optional
import requests
from requests import Response


logger = logging.getLogger(__name__)


class WordPressError(Exception):
    """Исключение для ошибок WordPress."""
    pass


class WordPressAPI:
    """Класс для работы с WordPress REST API."""
    
    def __init__(
        self,
        site_url: str,
        username: str,
        app_password: str,
        timeout: int = 30
    ):
        """
        Инициализирует WordPress API клиент.
        
        Args:
            site_url: URL сайта (например, https://example.com)
            username: Имя пользователя WordPress
            app_password: Application Password
            timeout: Таймаут запросов в секундах
        """
        # Normalize URL - force HTTPS
        if site_url.startswith("http://"):
            logger.info(f"Upgrading URL to HTTPS to avoid redirect...")
            site_url = site_url.replace("http://", "https://")
        
        self.site_url = site_url.rstrip('/')
        self.username = username.strip()
        self.app_password = app_password.strip()
        self.timeout = timeout
        
        # Create auth header
        auth_string = f"{self.username}:{self.app_password}"
        auth_header = base64.b64encode(auth_string.encode()).decode()
        
        self.headers = {
            'Authorization': f'Basic {auth_header}',
            'Content-Type': 'application/json',
            'User-Agent': 'PBN-Publisher/2.0'
        }
        
        self.endpoint = f"{self.site_url}/wp-json/wp/v2"
    
    def _request(
        self,
        method: str,
        path: str,
        **kwargs
    ) -> Optional[dict]:
        """
        Выполняет HTTP запрос к WordPress API.
        
        Args:
            method: HTTP метод (GET, POST, PUT, DELETE)
            path: Путь относительно wp-json/wp/v2
            **kwargs: Дополнительные параметры для requests
            
        Returns:
            Ответ API в виде словаря или None при ошибке
        """
        url = f"{self.endpoint}/{path.lstrip('/')}"
        
        try:
            response = requests.request(
                method,
                url,
                headers=self.headers,
                timeout=self.timeout,
                **kwargs
            )
            
            # Логируем статус
            logger.debug(f"WP API: {method} {url} -> {response.status_code}")
            
            if response.status_code in [200, 201]:
                return response.json() if response.content else {}
            
            # Обработка ошибок
            logger.warning(f"WP API Error: {response.status_code}")
            try:
                error_data = response.json()
                if 'message' in error_data:
                    logger.warning(f"WP Message: {error_data['message']}")
            except:
                pass
            
            return None
            
        except requests.exceptions.Timeout:
            logger.error(f"Timeout requesting {url}")
            return None
        except requests.exceptions.ConnectionError as e:
            logger.error(f"Connection error to {url}: {e}")
            return None
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
            return None
    
    def get_posts(
        self,
        per_page: int = 10,
        page: int = 1,
        status: str = "publish",
        **kwargs
    ) -> list[dict]:
        """
        Получает список постов.
        
        Args:
            per_page: Количество постов на странице
            page: Номер страницы
            status: Статус постов (publish, draft, etc.)
            **kwargs: Дополнительные параметры
            
        Returns:
            Список постов
        """
        params = {
            'per_page': per_page,
            'page': page,
            'status': status,
            **kwargs
        }
        
        result = self._request('GET', 'posts', params=params)
        return result if isinstance(result, list) else []
    
    def get_post(self, post_id: int) -> Optional[dict]:
        """
        Получает конкретный пост по ID.
        
        Args:
            post_id: ID поста
            
        Returns:
            Данные поста или None
        """
        return self._request('GET', f'posts/{post_id}')
    
    def get_post_by_slug(self, slug: str) -> Optional[dict]:
        """
        Получает пост по slug.
        
        Args:
            slug: Slug поста
            
        Returns:
            Данные поста или None
        """
        result = self._request('GET', 'posts', params={'slug': slug})
        if isinstance(result, list) and result:
            return result[0]
        return None
    
    def create_post(
        self,
        title: str,
        content: str,
        status: str = "publish",
        categories: Optional[list[int]] = None,
        tags: Optional[list[int]] = None,
        meta_description: Optional[str] = None,
        **kwargs
    ) -> Optional[dict]:
        """
        Создает новый пост.
        
        Args:
            title: Заголовок поста
            content: HTML контент
            status: Статус (publish, draft)
            categories: ID категорий
            tags: ID тегов
            meta_description: Meta description
            **kwargs: Дополнительные поля
            
        Returns:
            Созданный пост или None
        """
        data = {
            'title': title,
            'content': content,
            'status': status,
            **kwargs
        }
        
        if categories:
            data['categories'] = categories
        if tags:
            data['tags'] = tags
        if meta_description:
            data['meta'] = {'description': meta_description}
        
        return self._request('POST', 'posts', json=data)
    
    def update_post(
        self,
        post_id: int,
        title: Optional[str] = None,
        content: Optional[str] = None,
        status: Optional[str] = None,
        **kwargs
    ) -> Optional[dict]:
        """
        Обновляет существующий пост.
        
        Args:
            post_id: ID поста
            title: Новый заголовок
            content: Новый контент
            status: Новый статус
            **kwargs: Дополнительные поля
            
        Returns:
            Обновленный пост или None
        """
        data = {}
        
        if title is not None:
            data['title'] = title
        if content is not None:
            data['content'] = content
        if status is not None:
            data['status'] = status
        
        data.update(kwargs)
        
        return self._request('POST', f'posts/{post_id}', json=data)
    
    def delete_post(self, post_id: int, force: bool = False) -> bool:
        """
        Удаляет пост.
        
        Args:
            post_id: ID поста
            force: Принудительное удаление (без корзины)
            
        Returns:
            True при успехе
        """
        result = self._request(
            'DELETE',
            f'posts/{post_id}',
            params={'force': 'true' if force else 'false'}
        )
        return result is not None
    
    def get_categories(self) -> list[dict]:
        """
        Получает все категории.
        
        Returns:
            Список категорий
        """
        result = self._request('GET', 'categories', params={'per_page': 100})
        return result if isinstance(result, list) else []
    
    def get_category_by_name(self, name: str) -> Optional[dict]:
        """
        Получает категорию по имени.
        
        Args:
            name: Название категории
            
        Returns:
            Данные категории или None
        """
        result = self._request('GET', 'categories', params={'search': name})
        if isinstance(result, list) and result:
            return result[0]
        return None
    
    def create_category(
        self,
        name: str,
        description: str = "",
        parent: int = 0
    ) -> Optional[dict]:
        """
        Создает новую категорию.
        
        Args:
            name: Название категории
            description: Описание
            parent: ID родительской категории
            
        Returns:
            Созданная категория или None
        """
        data = {
            'name': name,
            'description': description,
            'parent': parent
        }
        
        return self._request('POST', 'categories', json=data)
    
    def get_or_create_category(
        self,
        name: str,
        description: str = ""
    ) -> int:
        """
        Получает существующую или создает новую категорию.
        
        Args:
            name: Название категории
            description: Описание
            
        Returns:
            ID категории
        """
        existing = self.get_category_by_name(name)
        if existing:
            return existing['id']
        
        created = self.create_category(name, description)
        return created['id'] if created else 0
    
    def get_tags(self) -> list[dict]:
        """Получает все теги."""
        result = self._request('GET', 'tags', params={'per_page': 100})
        return result if isinstance(result, list) else []
    
    def get_tag_by_name(self, name: str) -> Optional[dict]:
        """Получает тег по имени."""
        result = self._request('GET', 'tags', params={'search': name})
        if isinstance(result, list) and result:
            return result[0]
        return None
    
    def create_tag(self, name: str, description: str = "") -> Optional[dict]:
        """Создает новый тег."""
        data = {'name': name, 'description': description}
        return self._request('POST', 'tags', json=data)
    
    def get_or_create_tag(self, name: str, description: str = "") -> int:
        """Получает существующий или создает новый тег."""
        existing = self.get_tag_by_name(name)
        if existing:
            return existing['id']
        
        created = self.create_tag(name, description)
        return created['id'] if created else 0
    
    def get_pages(self, per_page: int = 10) -> list[dict]:
        """Получает список страниц."""
        result = self._request('GET', 'pages', params={'per_page': per_page})
        return result if isinstance(result, list) else []
    
    def get_page_by_slug(self, slug: str) -> Optional[dict]:
        """Получает страницу по slug."""
        result = self._request('GET', 'pages', params={'slug': slug})
        if isinstance(result, list) and result:
            return result[0]
        return None
    
    def create_page(
        self,
        title: str,
        content: str,
        status: str = "publish",
        **kwargs
    ) -> Optional[dict]:
        """Создает новую страницу."""
        data = {
            'title': title,
            'content': content,
            'status': status,
            **kwargs
        }
        return self._request('POST', 'pages', json=data)
    
    def test_connection(self) -> bool:
        """
        Тестирует соединение с WordPress.
        
        Returns:
            True если соединение успешно
        """
        result = self._request('GET', 'users/me')
        return result is not None


# === Convenience functions ===

def publish_post(
    site_url: str,
    username: str,
    app_password: str,
    title: str,
    content: str,
    status: str = "publish"
) -> Optional[dict]:
    """
    Упрощенная функция для публикации поста.
    
    Args:
        site_url: URL сайта
        username: Имя пользователя
        app_password: Application Password
        title: Заголовок
        content: HTML контент
        status: Статус публикации
        
    Returns:
        Созданный пост или None
    """
    api = WordPressAPI(site_url, username, app_password)
    return api.create_post(title, content, status)


def find_post_by_title(
    site_url: str,
    username: str,
    app_password: str,
    title_fragment: str
) -> Optional[dict]:
    """
    Находит пост по части заголовка.
    
    Args:
        site_url: URL сайта
        username: Имя пользователя
        app_password: Application Password
        title_fragment: Часть заголовка для поиска
        
    Returns:
        Данные поста или None
    """
    api = WordPressAPI(site_url, username, app_password)
    posts = api.get_posts(per_page=100)
    
    for post in posts:
        if title_fragment.lower() in post.get('title', {}).get('rendered', '').lower():
            return post
    
    return None
