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

## Dev Checkout

If you want to develop on this repo, make sure to checkout the submodules too...

```
git submodule update --init
```

## Environment Variables

* DOMAIN: Use the environment variable DOMAIN to replace example.com in the
  hugo theme template with your chosen domain name. Make sure to include the
  protocol e.g. https://foo.org
* THEME: Use the environment variable THEME to specify the name of a theme to
  use. By default the hugo-clarity theme is used if no THEME is specified. 

Themes shipped by default include:

* hugo-clarity (default)
* elephants

Starting site template:

There are three levels of overrides for the template path.
The template path provides all the initial contents for the starter site
When the site_path is empty the site_template_path contents will
be copied in to it to create the default starting site.
The override priority is:

1. If the SITE_TEMPLATE_PATH env var is set, that will be used. Typically
   you might mount this template as a docker volume so that you can 
   provide your own template.
2. If the SITE_TEMPLATE_PATH is NOT set and the THEME env var is set then
   we look in the theme dir for a folder called exampleSite and use the
   content we find there as the basis for the site template. The naming
   convention of exampleSite is from https://themes.gohugo.io/ which 
   provides many nice themes.
3. If neither of the above are specified, we will use the exampleSite
   folder provided in the clarity theme which is shipped with this project
   by default insied the themes_template_path.

## Adding themes

To add a theme, you currently need to fork this repo, add a new git submodule
pointing to your theme and then use the ``.build.sh`` script to create a new
docker image. In the future we will add some automation to do this from within
the running container.

## Example Usage

This repo includes a sample docker-compose service showing typical usage:

```
docker-compose up -d

```

## Accessing the site

After running you can find the site at
[http://localhost:8000](http://localhost:8000) and the file manager at (user
admin, pass admin) at [http://localhost:8001](http://localhost:8001).

Create or edit markdown files in the source directory using the filemanager and
then reload the web site to see the generated changes.

See https://github.com/kartoza/osgs for a full usage example.

## Credits

Tim Sutton 
info@kartoza.com
July 2021
