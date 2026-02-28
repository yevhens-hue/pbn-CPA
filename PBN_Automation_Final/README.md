# 🚀 PBN Automation Empire (Antigravity Edition)

Автономная система управления сеткой PBN на базе ИИ. 
Проект полностью готов к развертыванию на облачных платформах (Render) или выделенных серверах.

## ✨ Ключевые возможности
- **AI Content Engine:** Генерация уникальных статей через **Google Gemini 1.5 Flash** (оптимизировано под Free Tier).
- **Easy Import:** Удобное управление через Google Sheets (CSV).
- **Persona Shift:** Автоматическая смена стилей письма (Expert, Lifestyle, Neutral).
- **Smart Interlinking:** Модуль автоматической перелинковки старого контента.
- **BI Monitoring:** Подготовка данных для визуализации (SQLite/Grafana).

## 🛠 Быстрый старт (Local / VPS)

1. **Клонируйте репозиторий:**
   ```bash
   git clone https://github.com/martin-scott/pbn-automation.git
   cd pbn-automation
   ```

2. **Настройте окружение:**
   Создайте файл `.env` на основе `.env.example` и добавьте ваш `GEMINI_API_KEY`.

3. **Подготовьте данные:**
   - Заполните [Google Таблицу с сайтами](https://docs.google.com/spreadsheets/d/1CJjN_mSwrGwp2tVuaLK0vENb2c5VnYPQw0JM43HTE-c/edit?gid=643621907#gid=643621907).
   - Скачайте её как CSV и сохраните как `sites_import.csv`.
   - Запустите импорт:
     ```bash
     python3 core/import_from_sheets.py
     ```

4. **Запустите публикацию:**
   ```bash
   python3 core/publish_post.py data/sites_data.json
   ```

## ☁️ Развертывание на Render.com

Проект оптимизирован для запуска в облаке Render (как Cron Job или Background Worker).

1. Создайте новый **Background Worker** или **Cron Job** в Render Dashboard.
2. Подключите ваш репозиторий GitHub: `https://github.com/martin-scott/pbn-automation`.
3. Укажите Build Command: `pip install -r core/requirements.txt`.
4. Укажите Start Command: `python3 core/publish_post.py data/sites_data.json`.
5. Добавьте `GEMINI_API_KEY` в Environment Variables.

## 🗺 Domain Scanner (New!)
Инструмент для поиска свободных доменов в нише (например, India Gambling).

1. **Запуск:**
   ```bash
   python3 core/domain_scanner.py
   ```
2. **Результат:**
   - Список свободных доменов в консоли.
   - Автоматическое добавление найденных доменов в Google Таблицу (лист `Domains`).

---
**Разработчик:** [Martin Scott](https://github.com/martin-scott)
