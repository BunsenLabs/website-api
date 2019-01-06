FROM python:3.7-alpine
ADD blwwwapi /opt/service/
WORKDIR /opt/service
RUN mkdir blwwwapi && mv *.py *.yml workers/ ./blwwwapi/
ADD setup.py MANIFEST.in /opt/service/
RUN python setup.py install
EXPOSE 10000
ENTRYPOINT /usr/local/bin/blwwwapi
