ARG VERSION=latest

FROM ubuntu:${VERSION}

RUN apt-get -y update && apt-get install -y

RUN apt-get -y install python

RUN apt-get install -y python3-pip

RUN pip3 install requests

RUN pip3 install bs4

COPY . /usr/src/python_test

WORKDIR /usr/src/python_test

CMD [ "scrapURLS.py" ]

ENTRYPOINT [ "python3" ]
