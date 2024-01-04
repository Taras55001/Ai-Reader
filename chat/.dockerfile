# Docker-команда FROM вказує базовий образ контейнера
# Наш базовий образ - це Linux з попередньо встановленим python-3.10
FROM python:3.10

# Встановлення робочої директорії контейнера
WORKDIR /app

# Копіюємо файли з вашого локального контексту в контейнер
COPY . ./

# Встановлення залежностей з файлу requirements.txt
RUN pip install --no-cache-dir -r requirements.txt \
    && python manage.py migrate \
    && python manage.py runserver 80

# Позначимо порт де працює програма всередині контейнера
EXPOSE 3000

# Запустимо нашу програму всередині контейнера
CMD ["gunicorn", "-b", "0.0.0.0:80", "chat.wsgi"]