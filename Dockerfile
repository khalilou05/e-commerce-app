FROM python

WORKDIR /backend

COPY . .

RUN pip3 install -r requirement.txt

RUN apt-get install -y libpq-dev



CMD uvicorn main:app; python3 -m init_db.py 


