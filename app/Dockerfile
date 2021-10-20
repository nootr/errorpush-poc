FROM python:3.9

WORKDIR /usr/src/app/
COPY . .

RUN pip3 install -r requirements.txt

CMD ["gunicorn", "--bind=0.0.0.0:80", "main:app"]
