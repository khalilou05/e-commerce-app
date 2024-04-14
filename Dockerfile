FROM python

WORKDIR /backend

COPY . .

RUN pip3 install -r req.txt


CMD [ "uvicorn", "main:app" ]

