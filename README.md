# Webiste_2023

```pip install -r requirements.txt```

## How to create a webpage

To create a webpage, create a new .md file with the metadata structure in the ```/markdown``` directory.

```
---
title: (O)MACHINE1
year: 2023
cover_img_path: ./assets/imgs/omachine/cover.gif
page_img_path: ./assets/imgs/omachine/d_om-01.png
section: 0
width: 200
height: 80
subpage: /o-machine.html
draft: true
---
```

List of attributes you can use in the markdown file:

- ```# text```: creates a text block
- ```# imgw```: creates a image which spans the width of the div
- ```# imgdbl```: creates a div which consists of two images side by side. seperated by ```\```
- ```# video```: creates a div which consists of a video element
- ```# showcase```: creates a div which displays the year, title, and place. seperated by ```\```
- ```(text)[link]```: creates a href tag in a text block

## Utilities

- ```dither.py```: dithers all images in the ```public/assets/img``` folder, and copies all of the unprocessed images into the ```pre-dither_imgs``` folder.
- ```md-converter.py```: converts all .md files in ```/markdown``` to html elements, inserting that html into ```index.html``` using regexpressions. It also creates subpages for each file, which are accessible from ```public/works/```

