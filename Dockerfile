FROM python

WORKDIR /backend

COPY . .

RUN pip3 install -r requirement.txt

RUN apt-get update \
&& apt-get install -y \
apt-get install libpq5

ENTRYPOINT uvicorn main:app

CMD [ "python3", "-m", "init_db.py" ]


