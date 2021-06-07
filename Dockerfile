FROM python:3.7
RUN libmysqlclient-dev nginx -y
RUN apt-get update -y
COPY ../CRM_CONSIG_DJANGO /home/
RUN pip install -r CRM_CONSIG_DJANGO/requirements.txt
RUN cd CRM_CONSIG_DJANGO && python manage.py makemigrations && python manage.py migrate
CMD cd /home/CRM_CONSIG_DJANGO && /home/CRM_CONSIG_DJANGO/venv/bin/gunicorn --access-logfile - --workers 3 --bind 0.0.0.0:8000 CrmConsig.wsgi:application