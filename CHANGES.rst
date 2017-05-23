===========
Change log
===========

v0.1.0
-----------
* Start project

v0.1.1
-----------
* Update README
* Add codeship badge
* Fix setup.py syntax error

v0.1.2
-----------
* Add pillow as dep
* Upgrade to ovp-users 1.0.7
* Include UploadedImage viewset
* Include tests

v0.1.3
-----------
* Assert that url methods return something()
* Add django-storages
* Fix wrong dep on setup.py

v0.1.4
-----------
* Drop distutils in favor of setuptools

v0.1.4b
-----------
* Add .egg-info to .gitignore

v0.1.5
-----------
* Move image url methods from models to serializers

v0.1.6
-----------
* Return null on URL if no image file is associated with UploadedImage model(fix unexpected exception)

v0.1.7
-----------
* Fix 'self' reference inside function

v1.0.0
-----------
* Add serializer test cases to assure url format is OK

v1.0.1
-----------
* Use MEDIA_URL setting in test cases

v1.0.2
-----------
* Remove ovp_users as dependency
* Upgrade all dependencies

v1.0.3
-----------
* Fix issues with deepcopy

v1.0.4[unreleased]
-----------
* Implments image gallery, with admin and viewset
* Add filtering to gallery endpoint by query param 'category'
* Add pt_BR translations