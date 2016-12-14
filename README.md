# NYU Devops Class, Ice cream flavors

## Team members are Ilana, Mohammad, Nishma, and Soumie

[![Build Status](https://travis-ci.org/ilanasufrin/nyu-devops-homework-1.svg?branch=master)](https://travis-ci.org/ilanasufrin/nyu-devops-homework-1)
[![codecov](https://codecov.io/gh/ilanasufrin/nyu-devops-homework-1/branch/master/graph/badge.svg)](https://codecov.io/gh/ilanasufrin/nyu-devops-homework-1)


# Ice-cream REST API

The icecream API can be used to find information about different types of icecream, such as it's rating, the cost, the ingredients, and an additional status flag to know if it's melted or frozen.

The sample is using [Flask microframework](http://flask.pocoo.org/) and is intented to test the Python support on [IBM's Bluemix](https://bluemix.net/) environment which is based on Cloud Foundry.

## Run Locally

From a terminal navigate to a location where you want this application code to be downloaded to and issue:
```bash
$ git clone https://github.com/ilanasufrin/nyu-devops-homework-1.git
$ cd nyu-devops-homework-1
$ vagrant up
$ vagrant ssh ## to enter the VM
$ cd /vagrant
$ python icecream.py
```
and point your browser to localhost:5000

You may also use IBM Bluemix by setting VCAP_SERVICES env vars; uses redis on port 6379 (by default)

## Public URL and Documentation

To view the documentation of this application and know everything about the various endpoints:

locally: http://localhost:5000/

Bluemix URL: http://devops-icecream.mybluemix.net/
