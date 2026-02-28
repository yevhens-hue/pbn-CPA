# 🌍 VPS Deployment Guide

Инструкция по развертыванию PBN Automation на удаленном сервере.

## 1. Выбор сервера
Вам подойдет любой VPS с минимальными характеристиками:
- **OS**: Ubuntu 22.04 LTS (рекомендуется) или Debian 11.
- **CPU**: 1-2 vCPU.
- **RAM**: 2 GB (для комфортной работы Grafana).
- **Disk**: 20 GB SSD.

## 2. Подготовка окружения
Подключитесь к серверу по SSH и выполните следующие команды:

```bash
# Обновление системы
sudo apt update && sudo apt upgrade -y

# Установка Python и Pip
sudo apt install python3 python3-pip python3-venv -y

# Установка Docker (для Grafana)
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
```

## 3. Установка проекта
Загрузите архив `PBN_Automation_Final.zip` на сервер (например, через SFTP или `scp`).

```bash
# Распаковка
unzip PBN_Automation_Final.zip
cd PBN_Automation_Final

# Установка зависимостей
pip3 install -r core/requirements.txt
```

## 4. Настройка Telegram и API
Откройте файл `.env` и впишите свои ключи:
```bash
nano data/.env
```
*Вставьте туда `GEMINI_API_KEY`, `TELEGRAM_BOT_TOKEN`, `TELEGRAM_CHAT_ID`.*

## 5. Запуск Мониторинга (Grafana)
```bash
docker run -d -p 3000:3000 --name=pbn-grafana \
  -v "$(pwd)/monitoring:/var/lib/grafana/pbn_data" \
  -e "GF_INSTALL_PLUGINS=frser-sqlite-datasource" \
  grafana/grafana
```
*Теперь Grafana доступна по адресу `http://YOUR_SERVER_IP:3000`.*

## 6. Настройка Автоматизации (Cron)
Скрипт `daily_task.sh` будет запускать публикации каждый день.

1. Дайте права на выполнение:
   ```bash
   chmod +x core/daily_task.sh
   ```
2. Откройте редактор Cron:
   ```bash
   crontab -e
   ```
3. Добавьте строку (запуск каждый день в 10:00 утра):
   ```bash
   0 10 * * * /root/PBN_Automation_Final/core/daily_task.sh >> /root/pbn.log 2>&1
   ```

## ✅ Готово!
Ваша система теперь полностью автономна.
- **Ежедневно** она пишет статьи и обновляет ссылки.
- **Вам** приходят отчеты в Telegram.
- **Инвесторы** смотрят красивые графики в Grafana.
