set -o errexit

pip install 
python manage.py collectstatic --no-input
python manage.py migrate
