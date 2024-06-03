FROM python

WORKDIR /backend


RUN pip3 install -r requirement.txt

COPY . .

CMD [ "uvicorn", "main:app" ]

