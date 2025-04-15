FROM python:3.12.10-alpine3.21 AS base

WORKDIR /svc

COPY requirements.txt requirements.txt
RUN rm -rf /var/cache/apk/* && rm -rf /tmp/*
RUN apk update && apk add --update python3 && rm -rf /var/cache/apk/* && \
    pip wheel -r requirements.txt --wheel-dir=/svc/wheels

WORKDIR /app
COPY app.py .
COPY ZeroTier ./ZeroTier
COPY static ./static

FROM python:3.12.10-alpine3.21

COPY --from=base /svc /svc
WORKDIR /svc

RUN pip install --no-index --find-links=/svc/wheels -r requirements.txt

COPY --from=base /app /app
WORKDIR /app
CMD ["uvicorn", "app:app"]
