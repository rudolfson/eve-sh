#
# PostgreSQL DB with imported EVE static data from fuzzwork
#

FROM postgres:10-alpine
MAINTAINER leonty.alkaev@gmail.com

RUN apk add --update ca-certificates openssl && update-ca-certificates && \
    wget -O staticdata.dump.bz2 https://www.fuzzwork.co.uk/dump/postgres-schema-latest.dmp.bz2  && \
    bzip2 -d staticdata.dump.bz2
RUN echo "pg_restore --clean --create --dbname=postgres --no-owner /staticdata.dump" > /docker-entrypoint-initdb.d/01_read_dump.sh

