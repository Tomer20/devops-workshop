FROM python:3.7

RUN mkdir /app
WORKDIR /app
COPY app /app
COPY requirements.txt /requirements.txt
RUN pip install -r /requirements.txt
ENTRYPOINT ["python3","./app.py"]