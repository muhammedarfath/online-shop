FROM python:3.11



WORKDIR /mysite

COPY . /mysite

RUN pip install --upgrade pip --no-cache-dir

RUN pip install -r /mysite/requirements.txt --no-cache-dir

# CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
CMD ["gunicorn", "mysite.wsgi:application","--bind", "0.0.0.0:8000"]







