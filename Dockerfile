FROM python

WORKDIR /backend


RUN pip3 install -r requirement.txt

COPY . .

ENTRYPOINT [ "init_db.py" ]
CMD [ "uvicorn", "main:app" ]

