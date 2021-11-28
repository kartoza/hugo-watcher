FROM klakegg/hugo:0.86.0-debian
RUN apt update && apt install -y python3-pip && pip3 install watchdog
ADD themes_template /themes_template
ADD hugo_watcher.py /hugo_watcher.py
WORKDIR /src
# -u for unbuffered output so that print statements show in logs
# see https://stackoverflow.com/a/29745541
ENTRYPOINT ["python3", "-u", "/hugo_watcher.py"]
