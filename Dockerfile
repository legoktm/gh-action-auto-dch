FROM legoktm/gh-action-auto-dch:latest

COPY auto_dch.py /auto_dch.py

ENTRYPOINT ["/auto_dch.py"]
