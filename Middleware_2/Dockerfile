FROM alpine:3.7

RUN apk add --no-cache python3 && \
    python3 -m ensurepip && \
    rm -r /usr/lib/python*/ensurepip && \
    pip3 install --upgrade pip setuptools && \
    if [ ! -e /usr/bin/pip ]; then ln -s pip3 /usr/bin/pip ; fi && \
    if [[ ! -e /usr/bin/python ]]; then ln -sf /usr/bin/python3 /usr/bin/python; fi && \
    rm -r /root/.cache
RUN apk update && apk add glib && apk add gobject-introspection-dev \
    && apk add pkgconfig && apk add cairo-dev && apk add gcc \
    && apk add python3-dev && apk add openssl-dev && apk add g++ \
    && apk add py-openssl
RUN pip3 install nbxmpp requests pygobject
RUN pip3 install flask
COPY . /home/

RUN chmod 0775 -R /home/

ENV HOME /home/

WORKDIR /home

USER 1001

CMD ["/bin/sh", "-c", "python3 /home/mid2HTTP.py"]
