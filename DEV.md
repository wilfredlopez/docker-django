# START
```
docker build .
```

# Start Compose

```
docker-compose build
```

# Run Compose
### START
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

# Travis CI SET UP

go to travis website and enable the github project.
- create .travis.yml file


