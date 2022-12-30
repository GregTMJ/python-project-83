### Hexlet tests, linter status and CI :
[![Actions Status](https://github.com/GregTMJ/python-project-83/workflows/hexlet-check/badge.svg)](https://github.com/GregTMJ/python-project-83/actions)
[![Page Analyzer CI](https://github.com/GregTMJ/python-project-83/actions/workflows/page_analyzer.yml/badge.svg?branch=main)](https://github.com/Gregtmj/python-project-83/actions/workflows/page_analyzer.yml)
[![Maintainability](https://api.codeclimate.com/v1/badges/76d09bb269a5e483ef27/maintainability)](https://codeclimate.com/github/GregTMJ/python-project-83/maintainability)


## Getting Started

#### Clone the current repository via command:
```git clone https://github.com/GregTMJ/python-project-83.git```

***

## Requirements
* python >= 3.8
* Poetry >= 1.14
***

## Required packages
* Flask ^2.2.2
* Python-dotenv  ^0.21
* to avoid psycopg problems with different OS, install psycopg2-binary ^2.9.4
* Every other packages are shown inside pyproject.toml

***

#### Check your pip version with the following command:
```python -m pip --version```

#### Make sure that pip is always up-to-date. If not, use the following:
```python -m pip install --upgrade pip```

#### Next install poetry on your OS. (the link is below)
[Poetry installation](https://python-poetry.org/docs/)
##### don't forget to init poetry packages with command ```poetry init```

### We will be also working with postgreSQL, so make sure that you have installed it on your OS

*** 

## Makefile 
#### For every project should be configured a Makefile to initiate the project without requiring manual commands
#### Current project starts after typing ```make setup```
#### Inside our ```make setup``` we have 3 commands hidden:
* ``` make install```, which makes poetry install packages from pyproject.toml
* ```make lock```, which locks poetry packages inside poetry.lock
***

#### After configuration, you should use ```make dev``` to start your flask app
#### This app is made to analyze certain URLs

***
### Make sure than everything works, if you have something to add, remove or update, keep in touch "gregtmj@gmail.com"