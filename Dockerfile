# Используем Python 3.12
FROM python:3.12

# Устанавливаем рабочую директорию
WORKDIR /app

# Установка зависимостей
COPY ./requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Копируем код
COPY ./ ./

# Устанавливаем переменную окружения
ENV PYTHONUNBUFFERED=1

# Запускаем сервер
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]