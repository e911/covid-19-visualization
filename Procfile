release: python manage.py migrate
web: gunicorn covidData.wsgi:application --log-file -
