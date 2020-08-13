# START DOCKER ONLY
```
docker build .
```

# Start Compose localhost:8000

```
docker-compose build
```
# RUN APP

```
docker-compose up
```
# STOP APP

```
docker-compose down
```

# Run Compose
### START PROJECT
```
docker-compose run app sh -c "django-admin.py startproject app ."
```
### RUN TEST
```
docker-compose run app sh -c "python manage.py test"
```
### CREATE APP WITH DJANGO
```
docker-compose run app sh -c "django-admin.py startapp core"
```
- Then go to app/settings.py and add the name of the app. in thi case is called 'core' to "INSTALLED_APPS"

## Run Micrations

```
docker-compose run app sh -c "python manage.py makemigrations core"
```
### Create superuser in terminal
```
docker-compose run app sh -c  "python manage.py createsuperuser"
```
# Travis CI SET UP

go to travis website and enable the github project.
- create .travis.yml file


