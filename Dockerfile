FROM python:3.12

WORKDIR /app
COPY . /app

RUN pip install poetry
RUN python -m poetry install

CMD ["poetry", "run", "python", "-m", "gunicorn", "main:app"]