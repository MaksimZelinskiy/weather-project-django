FROM python:3.10
RUN apt-get update -y
RUN apt-get upgrade -y

WORKDIR /app

COPY ./requirements.txt ./

RUN  pip install --upgrade pip
RUN pip install -r requirements.txt

COPY ./src ./src

RUN python ./src/weather_project/manage.py migrate --noinput

CMD [ "python", "./src/weather_project/manage.py", "runserver", "0.0.0.0:8000"]

