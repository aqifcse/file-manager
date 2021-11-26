# file-manager

1. Now clone the project and navigate to file-manager

git clone https://gitlab.com/aqifcse/file-manager.git
cd file-manager

2. create a virtualenvironment

virtualenv venv
source venv/bin/activate


3 . Install all the dependencies for the project.

pip install -r requirements.txt

4 . You are all setup, let’s migrate now.

python manage.py makemigrations
python manage.py migrate

5 . Create a superuser to rule the site 😎

python manage.py create superuser

6 . Let’s visit the site now

python manage.py runserver

Visit http://127.0.0.1:8000/