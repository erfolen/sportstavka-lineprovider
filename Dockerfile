FROM python:3.12.5

RUN pip install poetry

RUN mkdir /line-provider

WORKDIR /line-provider

COPY . .

RUN poetry install --no-root

ENV PYTHONUNBUFFERED=1

RUN chmod +x entrypoint.sh
