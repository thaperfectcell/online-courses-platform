import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

app = Celery('config')

# Загружаем настройки Celery из Django settings с префиксом CELERY_
app.config_from_object('django.conf:settings', namespace='CELERY')

# Автоматически искать tasks.py во всех установленных приложениях
app.autodiscover_tasks()
