release: python manage.py migrate --noinput && python manage.py create_superuser
web: ./tailwindcss -i static/css/input.css -o static/css/output.css --minify && gunicorn nestway.wsgi --workers 2 --bind 0.0.0.0:$PORT
