production
==========

CCCS website production repository

SERVER (testing only)
- 54.243.193.28, via [core.crossculturalconsult.com](http://production.crossculturalconsult.com)
- Ubuntu 12.04.4

TOOLS
- [git](https://github.com/cccs-web/production/edit/master/README.md)
- pycharm [locally]
  - [quick installation guide for newer Ubuntu](http://cheparev.com/pycharm-installation-on-ubuntu-13-10/)
- virtualenvwrapper [server]
  - [installation guide](http://virtualenvwrapper.readthedocs.org/en/latest/install.html)

ENVIRONMENT
- ngnix
- Django
- [Mezzanine](http://mezzanine.jupo.org/)
- PostGIS
- PostgreSQL


PROCESS

*Configuration:*

- Cloned current production API and re-deployed as a micro-instance on 'fr' subdomain (linked above)
- Added 'paul' user, enabled ssh access in /etc/ssh/sshd_config
  - created 'webadmin' user, enabled ssh access in /etc/ssh/sshd_config [*no key yet made for user*]
- Changed Apache settings to re-route incoming traffic to beta WordPress site to verify routing from A record changes to new test instance
- [installed virtualenwrapper](http://virtualenvwrapper.readthedocs.org/en/latest/install.html)
- [installed PostGIS](http://postgis.net/install/) via the [UbuntuGIS repository](https://wiki.ubuntu.com/UbuntuGIS) ([used unstable repo](https://launchpad.net/~ubuntugis/+archive/ubuntugis-unstable)) by `sudo apt-add-repository ppa:ubuntugis/ubuntugis-unstable && sudo apt-get update` then `sudo apt-get install postgis`
- [installed git](http://git-scm.com/book/en/Getting-Started-Installing-Git) by installing dependencies: `apt-get install libcurl4-gnutls-dev libexpat1-dev gettext libz-dev libssl-dev` then running `apt-get install git`
- installed PostgreSQL: `sudo apt-get install postgresql`
- [installed Django](https://www.digitalocean.com/community/articles/installing-django-on-ubuntu-12-04--4) first by `sudo apt-get install python-imaging python-pythonmagick python-markdown python-textile python-docutils` then `sudo apt-get install python-django`
- removed Apache and installed nginx
  - was unsuccessful in setting up a working configuration to display the [WordPress development site](http://en.crossculturalconsult.com); our new ['production' site](http://production.crossculturalconsult.com) is now showing the default ngnix welcome message
  - Success: followed Step 5 [in this article](https://www.digitalocean.com/community/articles/how-to-install-linux-nginx-mysql-php-lemp-stack-on-ubuntu-12-04) by `sudo vi /etc/php5/fpm/php.ini`  then setting `cgi.fix_pathinfo=0` followed by `sudo vi /etc/php5/fpm/pool.d/www.conf` and replacing `listen = /var/run/php5-fpm.sock` with `listen = /var/run/php5-fpm.sock`; this changed my error message to 'cannot connect to database'; restarted mysql - everything running smoothly.


*Build:*

- initialized empty Git repository in /var/www/ by running `git init`
- [attempted to link server and GitHub repositories](https://help.github.com/articles/create-a-repo) using `git remote add origin https://github.com/cccs-web/core.git`
  - error: src refspec master does not match any.
  - error: failed to push some refs to 'https://github.com/cccs-web/production.git'
- [attempted to import and link](https://help.github.com/articles/importing-an-external-git-repository) 'core' repo using `git clone --bare https://githost.org/extuser/repo.git` followed by `git push --mirror https://github.com/ghuser/repo.git`
  - remote: error: refusing to delete the current branch: refs/heads/master To https://github.com/cccs-web/production.git ! [remote rejected] master (deletion of the current branch prohibited)
  - error: failed to push some refs to 'https://github.com/cccs-web/production.git'
- cloned 'production' repo using `git clone git://github.com/cccs-web/core.git`
  - Success.
- [installed Mezzanine](https://www.digitalocean.com/community/articles/how-to-install-and-get-started-with-django-based-mezzanine-cms-on-ubuntu) to /var/www/production/mezzanine_env/


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
