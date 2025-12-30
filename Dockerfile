FROM python:3.11
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY apps ./apps
COPY config ./config
COPY manage.py .
COPY run.sh .
ENV DJANGO_SETTINGS_MODULE=config.settings
EXPOSE 8000
CMD ["bash", "run.sh"]