# DriveToday

Drive Today is a Python (Django) based car renting web application, where company users can register to list their cars to reach more clients and manage their cars. At the same time, customer users can create a "customer" account in order to rent cars listed by the company users.

## Live here:

```
http://207.154.223.6/
```

## To launch this app on your local machine:

1. Prerequisite:
```
Python: https://www.python.org/downloads/
Git: https://git-scm.com/book/en/v2/Getting-Started-Installing-Git
```
2. To create and activate a Python environment for installing required pip packages:
```
pip install virtualenv
virtualenv env_name
source env/bin/activate
```
3. To download the source code: 
```
git clone https://github.com/aykhanmv/rentcar
```
4. To apply migrations and run the project:
```
cd rentcar
python3 manage.py makemigrations
python3 manage.py migrate
python3 manage.py runserver
```
5. To create an admin user (superuser):
```
python3 manage.py createsuperuser
```
