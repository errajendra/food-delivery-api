# food-delivery
,
Food Delivery Application using Django, (Python), Django Rest Framwork(DRF), Postgres and React.

1. clone the project using 
```console
git clone https://github.com/Wooshelf/food-delivery.git
```

2. Install all the dependies using this command
```console
pip install -r req.txt
```

3. create ```.env``` file, where manage.py file is located and add this code.
```
DB_NAME='food_delivery'
DB_HOST='localhost'
DB_PORT='5432'
DB_USER='postgres'
DB_PASSWORD='12345'

EMAIL_HOST = "smtp.gmail.com"
EMAIL_PORT = "587"
EMAIL_HOST_USER = " freakydiv@gmail.com"
EMAIL_HOST_PASSWORD = 'zaugyicvsoflxdvv'
DEFAULT_FROM_EMAIL = " freakydiv@gmail.com"

```
change your database credentials with mine.

4. open pgadmin4 and create a database called ```food_delivery```
