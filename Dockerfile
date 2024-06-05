FROM python

WORKDIR /backend

COPY . .

RUN pip3 install -r requirement.txt

RUN apt-get install -y libpq-dev



CMD python3 init_db.py && uvicorn main:app --host 0.0.0.0 


