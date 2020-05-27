FROM debian:latest

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get upgrade -y && \
 apt-get install python3 devscripts -y

COPY auto-dch.py /auto-dch.py

ENTRYPOINT ["/auto-dch.py"]
