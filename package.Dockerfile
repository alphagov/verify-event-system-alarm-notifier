FROM python:3.7 as install

WORKDIR /install
COPY requirements.txt .
RUN python3 -m pip install -r requirements.txt

COPY src src

FROM alpine:3.9 as package

RUN apk add zip
WORKDIR /package
COPY --from=install /usr/local/lib/python3.7/site-packages/ .
COPY --from=install /install/src/ src/

RUN zip -qr verify-event-system-alarm-notifier.zip .
