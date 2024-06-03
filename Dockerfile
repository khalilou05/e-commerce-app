FROM python

WORKDIR /backend

COPY . .

RUN pip3 install -r requirement.txt


ENTRYPOINT [ "/bin/python3", "-m","init_db.py" ]
CMD [ "uvicorn", "main:app" ]

