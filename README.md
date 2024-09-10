# call-center-scheduler

## Overview

This project is a shift planning and time-off management system for employees working in a Call Center environment. The goal is to create an efficient tool for managing work schedules, vacations, days off, and on-demand leave requests, while ensuring adequate staff coverage in a 24/7 operation.

## Frontend Project setup
```
npm install
```

### Compiles and hot-reloads for development
```
npm run serve
```

### Compiles and minifies for production
```
npm run build
```

### Lints and fixes files
```
npm run lint
```

### Customize configuration
See [Configuration Reference](https://cli.vuejs.org/config/).

## Backend Project setup

For little to no changes required install postrgreSQL, leave every value default, password is root ( you can customise it in database.py)


install requirements.txt
run with python 3.x, tested on 3.10, 3.6
check if database got created properly, login using command line (psql program for postgre)
Using `\dt` command you should see 3 tables

I forgot about adding default user so you need to do it manually:
```sql
INSERT INTO employees (first_name, last_name, email, password, is_admin)
VALUES 
('John', 'Doe', 'john.doe@example.com', 'ff2f12ec5c6a2e9ef6b61c958ed701c327469190a18075fd909ec2a9b42b94f2', true);
```

this creates admin user who can log in with login: `lohn.doe@example.com` password: `secure_password`



