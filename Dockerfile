FROM python

WORKDIR /backend

COPY . .

RUN pip3 install -r requirement.txt


CMD [ "uvicorn", "main:app" ]

