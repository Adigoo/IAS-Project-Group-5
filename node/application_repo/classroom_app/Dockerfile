
FROM python:3
# ENV PYTHONUNBUFFERED 1
WORKDIR /web_app
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
COPY . .
CMD [ "python3", "-u", "app.py" ]
