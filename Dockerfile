# 1. Выбираем базовый образ Python
FROM python:3.11-slim

# 2. Устанавливаем рабочую директорию в контейнере
WORKDIR /app

# 3. Копируем файл зависимостей
COPY requirements.txt .

# 4. Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt

# 5. Копируем весь проект в контейнер
COPY . .

# 6. Указываем порт (если приложение веб-сервер, например FastAPI/Flask)
EXPOSE 8000

# 7. Команда для запуска приложения
# Замените на свою команду, например для FastAPI: uvicorn main:app --host 0.0.0.0 --port 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
