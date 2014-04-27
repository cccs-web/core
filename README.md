production
==========

CCCS website production repository

SERVER IP (testing only)
- 54.243.193.28, via [production.crossculturalconsult.com](http://production.crossculturalconsult.com)

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
- PostgreSQL


PROCESS

*Configuration*

- Cloned current production API and re-deployed as a micro-instance on 'fr' subdomain (linked above)
- Added 'paul' user, enabled ssh access in /etc/ssh/sshd_config
  - created 'webadmin' user, enabled ssh access in /etc/ssh/sshd_config [*no key yet made for user*]
- Changed Apache settings to re-route incoming traffic to beta WordPress site to verify routing from A record changes to new test instance  
- [installed virtualenwrapper](http://virtualenvwrapper.readthedocs.org/en/latest/install.html)
- [installed PostGIS](http://postgis.net/install/) via the [UbuntuGIS repository](https://wiki.ubuntu.com/UbuntuGIS) ([used unstable repo](https://launchpad.net/~ubuntugis/+archive/ubuntugis-unstable)) by `sudo apt-add-repository ppa:ubuntugis/ubuntugis-unstable && sudo apt-get update` then `sudo apt-get install postgis`
- [installed git](http://git-scm.com/book/en/Getting-Started-Installing-Git) by installing dependencies: `apt-get install libcurl4-gnutls-dev libexpat1-dev gettext libz-dev libssl-dev` then running `apt-get install git`
- installed PostgreSQL: `sudo apt-get install postgresql`
- [installed Django](https://www.digitalocean.com/community/articles/installing-django-on-ubuntu-12-04--4) first by `sudo apt-get install python-imaging python-pythonmagick python-markdown python-textile python-docutils` then `sudo apt-get install python-django`
- initialized empty Git repository in /var/www/ by running `git init`
- [attempted to link repositories](https://help.github.com/articles/create-a-repo) using `git remote add origin https://github.com/cccs-web/production.git`
  - error: src refspec master does not match any.
  - error: failed to push some refs to 'https://github.com/cccs-web/production.git'
- [attempted to import and link](https://help.github.com/articles/importing-an-external-git-repository) 'production' repo using `git clone --bare https://githost.org/extuser/repo.git` followed by `git push --mirror https://github.com/ghuser/repo.git`
  - remote: error: refusing to delete the current branch: refs/heads/master To https://github.com/cccs-web/production.git ! [remote rejected] master (deletion of the current branch prohibited)
  - error: failed to push some refs to 'https://github.com/cccs-web/production.git'
- cloned 'production' repo using `git clone git://github.com/cccs-web/production.git`
  - Success.
- [installed Mezzanine](https://www.digitalocean.com/community/articles/how-to-install-and-get-started-with-django-based-mezzanine-cms-on-ubuntu) to /var/www/production/mezzanine_env/
  - QUESTION: Can I change and move this directory name just as any other?
- removed Apache and installed nginx
  - was unsuccessful in setting up a working configuration to display our [current WordPress development site](http://en.crossculturalconsult.com); [production](http://production.crossculturalconsult.com) is now showing the default ngnix welcome message
