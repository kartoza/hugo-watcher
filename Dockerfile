FROM klakegg/hugo:0.86.0-debian
RUN apt update && apt install -y python3-pip && pip3 install watchdog
ADD hugo_watcher.py /hugo_watcher.py
ADD themes_template/hugo-clarity/exampleSite /site_template
ADD themes_template /themes_template
ENTRYPOINT ["python3", "/hugo_watcher.py"]
