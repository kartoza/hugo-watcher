---
title: Creating Content
subtitle: How to add content to the site
images:
- "/unsplash/photo-1518732180525-52cc0d02180b.jpg"
categories:
- Documentation
- System
- Featured
summary: "How to  generate and publish content, utilising the relevant markdown and custom designed blocks for platform components."
---

This site supports the creation of two main content types - Maps and documents.

All content is stored as flat file plaintext documents in the relevant sections. The section defines the content type for each page and how it is renders on the site. The site uses [Markdown](https://commonmark.org/) for content styling, as well as various custom style definitions as illustrated in the [sample](/docs/sample) document.

[Page metadata](https://gohugo.io/content-management/front-matter/), or "front matter", is stored within each file at the top of the file using [yaml](https://docs.ansible.com/ansible/latest/reference_appendices/YAMLSyntax.html) syntax, and allows custom page behaviours to be defined dynamically for all content within a page.

### Maps

Map pages will automatically create an open layers map. The position and zoom level of the map at page load is defined in the page metadata.

Adding WMS layers may be done by configuring the relevant page metadata and specifying the WMS endpoint URL and the layers to be included.

{{< highlight text "linenos=table" >}}

lat: 13.9
long: -60.9
zoom: 13
wms: "https://geoservices.govt.lc/maproxy/service?"
layers:
- "Topo"

{{< / highlight >}}

Multiple layers may be included as a single map layer, however, only the use of a single WMS is supported at this time.

To create a new map, simply copy and paste the relevant demo document on the file system and edit accordingly.

### Documents

Documents are simple web pages which render the page contents from markdown into a complete webpage with the appropriate style sheets etc. More advanced functionality is available with custom code blocks as displayed in the included samples.
