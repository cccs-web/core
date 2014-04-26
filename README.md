production
==========

CCCS website production repository

SERVER IP (testing only)
- 54.243.193.28, via [fr.crossculturalconsult.com](http://fr.crossculturalconsult.com)

TOOLS:
- [git](https://github.com/cccs-web/production/edit/master/README.md)
- pycharm [locally]
  - [quick installation guide for newer Ubuntu](http://cheparev.com/pycharm-installation-on-ubuntu-13-10/)
- virtualenvwrapper [server]
  - [installation guide](http://virtualenvwrapper.readthedocs.org/en/latest/install.html)

ENVIRONMENT:
- ngnix
- Django
- [Mezzanine](http://mezzanine.jupo.org/)
- PostGIS


PROCESS

*Setup*

- Cloned current production API and re-deployed as a micro-instance on 'fr' subdomain (linked above)
- Added 'paul' user, enabled ssh access in /etc/ssh/sshd_config
- Changed Apache settings to re-route incoming traffic to beta WordPress site to verify routing from A record changes to new test instance  
- [installed virtualenwrapper](http://virtualenvwrapper.readthedocs.org/en/latest/install.html)
- [installed PostGIS](http://postgis.net/install/) via the [UbuntuGIS repository](https://wiki.ubuntu.com/UbuntuGIS) ([used unstable repo](https://launchpad.net/~ubuntugis/+archive/ubuntugis-unstable))
- [installed git](http://git-scm.com/book/en/Getting-Started-Installing-Git) by installing dependencies: `apt-get install libcurl4-gnutls-dev libexpat1-dev gettext libz-dev libssl-dev` then running `apt-get install git`
- initialized empty Git repository in /var/www/fr/.git/ by running `git init`
