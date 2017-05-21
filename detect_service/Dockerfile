FROM python:2

WORKDIR /app

COPY requirements.txt /app
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app
EXPOSE 10000
CMD [ "python", "./app.py" ]