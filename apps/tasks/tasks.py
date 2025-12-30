from celery import shared_task
import time

from django.core.mail import send_mail

from config import settings


@shared_task
def send_email(message:str,to:str):
    send_mail("New task for you", message, settings.EMAIL_HOST_USER,  [to])

@shared_task
def completed_task(message:str,to:str):
    send_mail("Your task is completed", message, settings.EMAIL_HOST_USER, [to])
@shared_task
def task():
    print("Starting task")
@shared_task
def new_comment(message:str,to:str):
    send_mail('Arina',message,settings.EMAIL_HOST_USER,[to])
