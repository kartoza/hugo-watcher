# hugo-watcher

A fork of the debian based klakegg/hugo
(https://hub.docker.com/r/klakegg/hugo/) docker image that watches a directory
and autobuilds when files change.

Please note that this docker image is was originally developed to support the
Kartoza OpenSource-GIS-Stack (https://github.com/kartoza/OpenSource-GIS-Stack/)
project - see that project for a fully worked out example.

If you are just looking for a generic Hugo image that watches a directory and
builds when the files change, you can clone and tweak this project - probably
you just need to tweak the provided templates.

This repo includes a sample docker-compose service showing typical usage:

```
docker-compose up -d

```

After running you can find the site at
[http://localhost:8000](http://localhost:8000) and the file manager at (user
admin, pass admin) at [http://localhost:8001](http://localhost:8001).

Create or edit markdown files in the source directory using the filemanager and
then reload the web site to see the generated changes.

See https://github.com/kartoza/osgs for a full usage example.

Tim Sutton 
info@kartoza.com
July 2021
