FROM python:3.6

ENV PYTHONUNBUFFERED 1

RUN mkdir -p /var/log/gunicorn

RUN mkdir /grabwack
WORKDIR /grabwack

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .

CMD ["/bin/bash", "initialization-script.sh"]
