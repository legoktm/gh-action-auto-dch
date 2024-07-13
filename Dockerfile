FROM docker.pkg.github.com/legoktm/gh-action-images/auto-dch:latest

COPY auto_dch.py /auto_dch.py

ENTRYPOINT ["/auto_dch.py"]
