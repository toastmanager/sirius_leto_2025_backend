# Сириус Лето 2025

## Разработка

1. Создайте и войдите в виртуальное окружение

   - windows

     ```
     python -m venv venv
     venv/Scripts/activate
     ```

   - linux

     ```
     python3 -m venv venv
     source venv/bin/activate
     ```

2. Установите зависимости пакетного менеджера

   ```sh
   pip install -r requirements.txt
   ```

3. Скопируйте `.env.example` в `.env`

   ```sh
   cp .env.example .env
   ```

4. Запустите сторонние зависимости

   ```sh
   docker compose -f docker-compose-dev.yaml up -d
   ```

5. Примените миграции

   ```sh
   python manage.py migrate
   ```

6. Запустите сервер

   ```sh
   python manage.py runserver
   ```
