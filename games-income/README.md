# games-income.com — Bonus Scraper

Гео-таргетированный агрегатор бонусов для казино и беттинг-сайтов.

## Структура проекта

```
games-income/
└── scraper/
    ├── bonus_scraper.py     ← Ядро: парсит бонусы, хранит в SQLite
    ├── scheduler.py         ← Планировщик: запускает парсер по расписанию
    ├── requirements.txt     ← Зависимости Python
    ├── .env.template        ← Шаблон конфига (скопируйте в .env)
    ├── bonuses.db           ← SQLite база данных (создается автоматически)
    ├── output/              ← JSON-экспорты (создается автоматически)
    └── config/
        ├── sites_by_geo.json *   **GEO Support**: India (IN), Turkey (TR), Brazil (BR).
        └── bonus_selectors.json ← CSS-селекторы для каждого бренда
```

## Быстрый старт

```bash
# 1. Установить зависимости
pip3 install -r requirements.txt

# 2. Скопировать .env
cp .env.template .env
# Затем вставить ваши ключи в .env

# 3. Тестовый запуск (без записи в базу)
python3 bonus_scraper.py --geo IN --type casino --dry-run

# 4. Реальный запуск (записывает в bonuses.db)
python3 bonus_scraper.py --geo IN --type all

# 5. Экспортировать JSON для WordPress/фронтенда
python3 bonus_scraper.py --geo IN --export --output output/bonuses_india.json
```

## Планировщик (Автоматический режим)

```bash
# Разовый запуск для всех ГЕО
python3 scheduler.py

# Бесконечный цикл каждые 6 часов (для сервера)
python3 scheduler.py --loop --export
```

## Добавление ГЕО / Сайтов

Отредактируйте `config/sites_by_geo.json`:

```json
"DE": {
  "name": "Germany",
  "currency": "EUR",
  "language": "de",
  "casino": [
    {
      "name": "Betsson",
      "brand_id": "betsson",
      "bonus_url": "https://www.betsson.de/promotions",
      "affiliate_url": "https://your-affiliate-link",
      "logo": "https://betsson.de/favicon.ico",
      "rating": 4.5
    }
  ],
  "betting": []
}
```

## Добавление в Cron (Linux/Mac сервер)

```
# Запускать каждые 6 часов
0 */6 * * * /usr/bin/python3 /path/to/scraper/scheduler.py --export
```

## Интеграция с WordPress

После экспорта `output/bonuses_IN.json` загружайте данные через WordPress REST API:

```python
import requests, json

with open("output/bonuses_IN.json") as f:
    data = json.load(f)

for bonus in data["bonuses"]:
    requests.post(
        "https://games-income.com/wp-json/wp/v2/posts",
        auth=("admin", "your_app_password"),
        json={
            "title": f"{bonus['brand_name']}: {bonus['bonus_title']}",
            "content": f"<p>Amount: {bonus['bonus_amount']}</p>",
            "status": "publish"
        }
    )
```
