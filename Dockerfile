FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# create app user
RUN addgroup --system app && \
    adduser --system --ingroup app --home /home/app app && \
    mkdir -p /home/app && \
    chown -R app:app /home/app

ENV HOME=/home/app

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN python manage.py collectstatic --noinput

RUN chown -R app:app /app

USER app

EXPOSE 7860

CMD ["gunicorn", "core.wsgi:application", "--bind", "0.0.0.0:7860"]
