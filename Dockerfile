FROM python

LABEL maintainer="sergioarroyopay@gmail.com"

COPY requirements.txt .

RUN pip install -r requirements.txt

WORKDIR /usr/src/app

CMD ["python", "./manage.py"]