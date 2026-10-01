# Institute OMR grader (OMRChecker based) - web UI + CLI
FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    MPLBACKEND=Agg \
    OMR_DATA_DIR=/data \
    OMR_CONFIG_DIR=/app/config \
    OMR_HOST=0.0.0.0 \
    OMR_PORT=8000 \
    OMR_LOG_LEVEL=INFO

WORKDIR /app

COPY requirements.txt requirements.app.txt ./
RUN pip install -r requirements.app.txt

COPY main.py ./
COPY src ./src
COPY omr_app ./omr_app
COPY config ./config

RUN useradd --create-home --uid 1000 omr && mkdir -p /data && chown -R omr:omr /data /app/config
USER omr

VOLUME ["/data"]
EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=5s --start-period=20s --retries=3 \
  CMD python -c "import urllib.request,os; urllib.request.urlopen('http://127.0.0.1:%s/api/meta' % os.environ.get('OMR_PORT','8000'), timeout=4)" || exit 1

# default: web interface. CLI example:
#   docker compose run --rm omr grade /data/in --key institute_2026_business_management --out /data/out
ENTRYPOINT ["python", "-m", "omr_app"]
CMD ["serve"]
