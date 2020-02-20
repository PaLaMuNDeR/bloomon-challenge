# README #

### What is this repository for? ###

* This is a repository to satisfy the requirements of the Bouquet Design problem (check [reqiurements.pdf](requirements.pdf))

### How to setup ###

Install `docker` and `docker-compose`
Run `docker-compose up -d`

### How to modify the input ###
Replace the content of file [input.txt](./bouquet_design/input.txt) with new content and run the container again or:

1. Enter the container with:
`docker-compose exec bouquet_design sh`
`python bouquet_design.py`

2. Check the output that would be generated in file `output.txt`

___
Author: Martin Anev (martianev@gmail.com)