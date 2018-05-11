# SMTPServer
 ![PyPI - Python Version](https://img.shields.io/badge/python-3.6-blue.svg) ![PyPI - Implementation](https://img.shields.io/badge/implementation-pymysql-blue.svg) ![MySQL - Version](https://img.shields.io/badge/mysql-Ver%2014.14%20Distrib%205.7.22-lightgrey.svg) [![Python3 Status](https://caniusepython3.com/project/django-firebird.png)](https://caniusepython3.com/project/django-firebird)

This proyect provides a simple SMTP that stores mails into a database. It is connected to [this client](https://github.com/AlvaroSanchezTortola/SMTPClient), [this inbox](https://github.com/AlvaroSanchezTortola/SMTPReader) and [this logger](https://github.com/AlvaroSanchezTortola/SMTPLogger). 

## Installation
### Before Installation
It is recommended to use a `python virtual enviroment`. Create it with:
``` sh
python3 -m venv smtpserver
```
and run it with:
``` sh
source smtpserver/bin/activate
```
### General Instructions
#### MySQL
First, install `mysql`:
``` sh
sudo apt-get install mysql-server
```
then, log in with:
``` sh
mysql -u root
```
Finally, populate the database with the file `config.sql`
``` mysql
mysql> source \config.sql;
```
#### Python Dependencies
Install all project dependencies with `pip`
``` sh
pip3 install -r requirements.txt 
```
## Run
Assuming you run it from a terminal within the main folder:
```
python3 SMTPServer.py
```