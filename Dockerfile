FROM python:3.6-alpine
ADD blwwwapi /opt/service/
WORKDIR /opt/service
RUN mkdir blwwwapi && mv *.py ./blwwwapi/
ADD setup.py /opt/service/
RUN python setup.py install
EXPOSE 10000
ENTRYPOINT /usr/local/bin/blwwwapi
