FROM debian:latest

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get upgrade -y && \
 apt-get install python3 devscripts -y

COPY auto_dch.py /auto_dch.py

ENTRYPOINT ["/auto_dch.py"]
