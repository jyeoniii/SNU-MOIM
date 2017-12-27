[![Build Status](https://travis-ci.org/swsnu/swpp17-team9.svg?branch=master)](https://travis-ci.org/swsnu/swpp17-team9) [![Coverage Status](https://coveralls.io/repos/github/swsnu/swpp17-team9/badge.svg?branch=master)](https://coveralls.io/github/swsnu/swpp17-team9?branch=master)
# SNU Moim

## Contributors
- Team9
  - Jiyun Jeong
  - Seungchan Kim
  - Pimon Atipatyakul
  - Jaeyeon Kim

## Project Abstract
This project aims to create service that can help SNU students to find other students to arrange some meeting for any purpose. It categorizes meetings into several categories (i.e. Study, a student club, performance) so that users can easily find the meetings they want. The two primary features of this project are creating a new meeting & participating in an existing meeting (which is already created by other users). Also, this service can recommend some meetings that the user might like based on user information. It can also connect to Facebook to get much information of the user.

## Features
- Various options for each categories
- User friendly interface
- Search function
- SNU Member Authentication (by SNU mail)
- Comment (Private / Public)
- Home interface

More details are written in [Final Report](https://github.com/swsnu/swpp17-team9/blob/master/report/Final%20Report%20_%20Team%209.pdf)

## Project Architecture
- Frontend : Angular2 + Typescript
- Backend : Django + Python
- Design : Bootstrap

## Documents
[Requirements and Specifications](https://github.com/swsnu/swpp17-team9/wiki/Requirement-and-Specification)  
[Design and Planning](https://github.com/swsnu/swpp17-team9/wiki/Design-and-Planning) 

## Progress
| Sprint | Date | Report |
|--------|------|--------|
| 1 | 10/10-10/23 | [Sprint 1 report](https://github.com/swsnu/swpp17-team9/wiki/Sprint-1-Progress-Report) |
| 2 | 10/24-11/6 | [Sprint 2 report](https://github.com/swsnu/swpp17-team9/wiki/Sprint-2-Progress-Report) |
| 3 | 11/7-11/20 | [Sprint 3 report](https://github.com/swsnu/swpp17-team9/wiki/Sprint-3-Progress-Report) |
| 4 | 11/21-12/4 | [Sprint 4 report](https://github.com/swsnu/swpp17-team9/wiki/Sprint-4-Progress-Report) |
| 5 | 12/5-12/18 | [Sprint 5 report](https://github.com/swsnu/swpp17-team9/wiki/Sprint-5-Progress-Report) |

Project milestone per each sprint can be seen [here](https://github.com/swsnu/swpp17-team9/wiki/Project-milestone).

## How To Run
* Angular2
```shell
$ cd snumeeting-front/
$ npm install           // install dependencies
$ npm start
```
* Django
```shell
$ cd snumeeting_back/
$ python3 manage.py runserver --setting=snumeeting_back.settings_div.debug
```

* Dependencies
```shell
$ npm install ngx-pagination --save
$ npm install ngx-chips --save

$ pip3 install social-auth-app-django
$ pip3 install urllib3
$ pip3 install pymysql
```
