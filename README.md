# DriveToday

Drive Today is a Python (Django) based car renting application, where company users can register to list their cars to recah more clients. At the same time, customer users can create a "customer" account in order to rent a car.

## VPS, Database and Admin dashboard access:

```
Link: http://207.154.223.6/
Admin panel: http://207.154.223.6/admin

Admin user: aykhan.mv@gmail.com
Admin user passwd: aykhan123
```

## To Access to the data base:

```
1. Connect to the vps: ssh root@207.154.223.6
2. Root user password: mVaykha1n
3. sudo -u postgres psql
4. DB name: rentcardb 
5. DB user: rentcaruser
6. DB user passwd: 12345
```

## To launch this app on your local machine:
*NOTE*: Wehn you are launching this app on your local machine it will use SQLlite DB, which means you will no be able to see the contents shared on the live app. You can create your own users to test. Furthermore, there is "Car images for testing" folder which contain car images if you want to test adding car feature.

1. To install this app you need python and git first:
```
Python: https://www.python.org/downloads/
Git: https://git-scm.com/book/en/v2/Getting-Started-Installing-Git
```
2. To create and activate a python environment for installing required pip packages:
```
pip install virtualenv
virtualenv env_name
source env/bin/activate
```
3. To download the source code: 
```
git clone https://github.com/aykhanmv/rentca
```
4. To apply migirations and run the project:
```
cd rentcar
python3 manage.py makemigrations
python3 manage.py migrate
python3 manage.py runserver
```
5. To create an admin user (super user):
```
python3 manage.py createsuperuser
```
