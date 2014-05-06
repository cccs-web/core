CCCS website - development repository
==========



## Set up the server ##

If using the server edition of Ubuntu, [enable the universe repository](https://help.ubuntu.com/community/Repositories/CommandLine):

	~ $ sudo apt-get install libamd2.2.0 libblas3gf libc6 libgcc1 libgfortran3 \
	  liblapack3gf libumfpack5.4.0 libstdc++6 build-essential gfortran \
	  libatlas-dev libatlas3-base python python-all-dev gcc g++ libblas-dev \
	  liblapack-dev libevent-dev

## Install the geospatial libraries ##

	~ $ sudo apt-get install binutils libproj-dev gdal-bin libgeo-proj4-perl libjson0-dev

## Set up PostGIS ##

Adapted from [here](http://trac.osgeo.org/postgis/wiki/UsersWikiPostGIS20Ubuntu1204)

	~ $ sudo apt-get install postgresql-9.1 postgresql-contrib-9.1 postgresql-server-dev-9.1 libpq-dev
	...
	~ $ sudo apt-get install python-software-properties
	...
	~ $ sudo apt-add-repository ppa:ubuntugis/ubuntugis-unstable
	...
	~ $ sudo apt-get update
	...
	~ $ sudo apt-get install postgresql-9.1-postgis-2.0

## Set up the database and user

Add the database and database user:

    psql -c "CREATE USER cccs WITH PASSWORD 'password';"
    psql -c "CREATE DATABASE cccs WITH OWNER cccs;"

## Enable the database for GIS use:

    psql -c "CREATE EXTENSION postgis;"
    psql -c "CREATE EXTENSION postgis_topology;"

## Import a shp file

Change to the folder where the shp file and its related dbf file are located and:

    ogr2ogr -f PostgreSQL PG:dbname=cccs file.shp
