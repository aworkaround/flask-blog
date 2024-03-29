FROM python:3.12.2-alpine3.19

WORKDIR /app
COPY . /app

RUN pip install poetry
RUN poetry install

CMD ["sleep", "5", ";", "poetry", "run", "gunicorn", "wsgi:app"]
