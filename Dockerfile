FROM python:3.9.20-bullseye
WORKDIR /usr/app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 80
CMD ["python", "app.py"]