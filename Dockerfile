FROM alpine:edge
RUN apk --no-cache add uwsgi uwsgi-python3 uwsgi-http python3 py3-pip
WORKDIR /app
COPY blwwwapi /app/blwwwapi
COPY requirements.txt setup.py /app/
ENTRYPOINT uwsgi --plugins http,python --http :9090 --wsgi-file blwwwapi/uwsgi.py --enable-threads --stats :9191
EXPOSE 9090
EXPOSE 9191
RUN pip install -r requirements.txt
