FROM python:3.11 AS builder

COPY setup.py .

RUN mkdir /deps && pip install --upgrade pip && pip install  --prefix=/deps  .

FROM python:3.11
WORKDIR /aaaa

COPY --from=builder /deps /usr/local
COPY . .
COPY ./secrets/cockroach_certificate /home/.postgresql/root.crt

ENV LOG_LEVEL=INFO
ENV LOG_HANDLER=gcp
ENV SENTRY_ENABLED=True
ENV APP_SANDBOX=True

RUN rm ./secrets/cockroach_certificate

ENTRYPOINT ["uvicorn", "aaaa:serve"]
CMD ["--host", "0.0.0.0", "--port", "8080", "--reload-exclude", "infra/*"]