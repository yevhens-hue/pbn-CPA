# 🚀 PBN Automation Empire (Antigravity Edition)

> **⚠️ ВНИМАНИЕ:** Основная директория проекта — `PBN_Automation_Final/`. 
> Все новые разработки ведутся в ней.

## Структура проекта

```
PBN_Automation_Final/    # Основная директория (активная разработка)
├── core/                # Модули ядра
├── docs/                # Документация
├── infrastructure/      # Скрипты развертывания
├── samples/             # Примеры контента
└── publish_post.py     # Основной скрипт публикации

games-income/           # Фронтенд Next.js для casino/betting
├── frontend/            # Next.js приложение
└── scraper/            # Скрейпер бонусов

tests/                  # Unit тесты
```

## ⚡ Быстрый старт

1. **Перейдите в основную директорию:**
   ```bash
   cd PBN_Automation_Final
   ```

2. **Настройте окружение:**
   Создайте файл `.env` на основе `.env.example` и добавьте ваш `GEMINI_API_KEY`.

3. **Установите зависимости:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Запустите публикацию:**
   ```bash
   python3 publish_post.py data/sites_data.json
   ```

## 🧪 Тестирование

```bash
# Установите pytest
pip install pytest

# Запустите тесты
pytest tests/ -v
```

## 📚 Документация

- [Техническая документация](PBN_Automation_Final/docs/TECHNICAL_ROADMAP.md)
- [План развертывания](PBN_Automation_Final/docs/DEPLOYMENT.md)
- [Бизнес-план](PBN_Automation_Final/docs/BUSINESS_PLAN.md)

---

**Разработчик:** [Martin Scott](https://github.com/martin-scott)
