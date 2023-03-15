FROM python:3.11

WORKDIR /usr/src/app
COPY requirements/requirements.txt ./
RUN pip install -r requirements.txt
COPY . .
ADD entrypoint.sh /entrypoint.sh
RUN chmod a+x /entrypoint.sh
ENV DJANGO_SUPERUSER_PASSWORD=admin
ENTRYPOINT ["/entrypoint.sh"]

EXPOSE 8000
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
