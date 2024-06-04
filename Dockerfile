FROM python

WORKDIR /backend

COPY . .

RUN pip3 install -r requirement.txt

RUN apt-get install -y libpq-dev



CMD psql "user=postgres password=khalil dbname=postgres" -f init.sql &&\ 
uvicorn main:app --host 0.0.0.0 


