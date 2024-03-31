FROM python

WORKDIR /backend

COPY . /backend/

RUN pip3 install -r req.txt


CMD [ "uvicorn", "main:app" ]

