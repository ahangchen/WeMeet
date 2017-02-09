mkdir log/team
mkdir student/migrations
mkdir team/migrations
touch student/migrations/__init__.py
touch team/migrations/__init__.py
makemigrations
migrate
python3 manage.py runserver 0.0.0.0:8081 --insecure


