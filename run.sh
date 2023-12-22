curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
pip install pipenv
pipenv install django
pipenv shell

pip install djangorestframework
pip install djangorestframework-api-key
pip install drf-yasg

python manage.py runserver