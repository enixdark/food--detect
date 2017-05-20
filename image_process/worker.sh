virtualenv venv
source venv/bin/activate
pip install -r requirements.txt

celery -A worker worker --loglevel=info