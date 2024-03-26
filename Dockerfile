FROM python:3.12.2-alpine3.19

WORKDIR /app
COPY . /app

RUN pip install poetry
RUN poetry install

# CMD ["poetry", "run", "gunicorn", "wsgi:app"]
CMD ["sleep", "100000"]
