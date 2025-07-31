# Использовать образ Python3.10
FROM python:3.10

# Установить директорию проекта в контейнере
WORKDIR /app

# Скопировать все файлы в контейнер
COPY . .

# Установить переменную окружения PYTHONPATH=/app в контейнере
ENV PYTHONPATH=/app

# Установить зависимости из файла requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Создать .env файл в HOME_DIR
ARG HOME_DIR=/app
RUN echo "HOME_DIR=${HOME_DIR}" > .env

# Команда для запуска скрипта в контейнере
CMD ["python", "src/garage_payments/main.py"]