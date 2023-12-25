curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
pip install pipenv
pipenv install django
pipenv shell

pip install djangorestframework
pip install djangorestframework-api-key
pip install djangorestframework-simplejwt
pip install drf-yasg
pip install django-cors-headers


python manage.py runserver 