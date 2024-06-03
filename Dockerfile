FROM python

WORKDIR /backend

COPY . .

RUN pip3 install -r requirement.txt


ENTRYPOINT [ "python", "-m","init_db.py" ]
CMD [ "uvicorn", "main:app" ]

