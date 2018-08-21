export FLASK_APP=scap_registry/app.py
export FLASK_DEBUG=1
python -m flask run

echo '';
echo 'Shut Down';

unset FLASK_APP
unset FLASK_DEBUG
