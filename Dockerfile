FROM python

WORKDIR /backend

COPY . .

RUN pip3 install -r requirement.txt

ENTRYPOINT uvicorn main:app

CMD [ "python", "-m", "init_db.py" ]


