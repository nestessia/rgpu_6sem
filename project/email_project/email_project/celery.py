from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

# Установите настройки Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'email_project.settings')

# Создайте экземпляр Celery
app = Celery('email_project')

# Используйте настройки Django для конфигурации Celery
app.config_from_object('django.conf:settings', namespace='CELERY')

# Автоматически обнаруживайте задачи в приложениях
app.autodiscover_tasks()
