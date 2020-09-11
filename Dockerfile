FROM python:3.8-alpine
RUN pip install --no-cache-dir paho-mqtt smbus2
RUN mkdir -p /fds-mcu/app
WORKDIR /fds-mcu
COPY app ./app
COPY manage.py ./manage.py
CMD ["python", "manage.py"]