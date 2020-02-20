FROM python:3.6-alpine
COPY bouquet_design /bouquet_design/

WORKDIR ./bouquet_design
CMD tail -f /dev/null