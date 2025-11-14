# 1. Базовый образ с Python
FROM python:3.12-slim

# 2. Настройки окружения внутри контейнера
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# 3. Рабочая директория внутри контейнера
WORKDIR /app

# 4. Копируем только зависимости сначала
COPY requirements.txt /app/

# 5. Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt

# 6. Копируем весь проект в контейнер
COPY . /app/

# 7. Открываем порт 8000 (на уровне документации)
EXPOSE 8000

# 8. Команда запуска: gunicorn, не runserver
CMD ["gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:8000"]
