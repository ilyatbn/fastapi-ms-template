FROM python:3.11.7-slim-bullseye
RUN apt-get update -qq\
    && apt-get -y install libpq-dev gcc \
    && pip install --upgrade pip \
    && pip install psycopg2 
COPY build/requirements.txt /tmp/
RUN python3 -m pip install -r /tmp/requirements.txt
COPY src /app
RUN groupadd -g 1000 base && \
   useradd -u 1000 -g base base \
   && chown -R base:base /app
USER base:base
WORKDIR /app
ENTRYPOINT [ "./entrypoint.sh", "uvirun" ]
