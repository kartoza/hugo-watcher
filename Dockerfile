FROM klakegg/hugo:0.86.0-debian
RUN apt update && apt install -y python3-pip && pip3 install watchdog
ADD hugo_watcher.py /hugo_watcher.py
ADD archetypes /src/archetypes
ADD layouts /src/layouts
ADD resources /src/resources
ADD static /src/static
ENTRYPOINT ["python3", "/hugo_watcher.py"]
