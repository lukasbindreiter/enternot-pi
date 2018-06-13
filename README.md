# Enternot - PI [![GitHub license](http://img.shields.io/badge/license-MIT-blue.svg?style=flat-square)](https://github.com/lukasbindreiter/enternot-pi/blob/master/LICENSE)

Enternot is a home security system powered by the Raspberry PI.

Check out the corresponding Android client: [enternot-app](https://github.com/Shynixn/enternot-app).

## API Documentation
Documentation is provided by the `docs/swagger.yaml` file. You can view it using Swagger UI using [this link](http://petstore.swagger.io?url=https://raw.githubusercontent.com/lukasbindreiter/enternot-pi/master/docs/swagger.yaml)

## Build status

| Branch        | Status        | Information |
| ------------- | --------------| ------- |
| **master**        | [![Build Status](https://img.shields.io/travis/lukasbindreiter/enternot-pi/master.svg?style=flat-square)](https://travis-ci.org/lukasbindreiter/enternot-pi) | [![Coverage Status](https://img.shields.io/coveralls/lukasbindreiter/enternot-pi/master.svg?style=flat-square)](https://coveralls.io/github/lukasbindreiter/enternot-pi?branch=master) |

## Getting started
The following steps are required to ge the application up and running.
```bash
git clone git@github.com:lukasbindreiter/enternot-pi.git
cd enternot-pi
pipenv install --dev
pipenv run flask run
```

Now you should be able to connect to the webserver on localhost:5000

