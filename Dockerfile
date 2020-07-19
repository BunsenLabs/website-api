FROM python:3.8-alpine
ADD dist/*.tar.gz /opt/service/
WORKDIR /opt/service
RUN cd * && python setup.py install
EXPOSE 10000
ENTRYPOINT /usr/local/bin/blwwwapi
