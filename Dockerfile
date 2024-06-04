FROM python

WORKDIR /backend

COPY . .

RUN pip3 install -r requirement.txt

RUN apt-get install libpq-dev

ENTRYPOINT uvicorn main:app

CMD [ "python3", "-m", "init_db.py" ]


