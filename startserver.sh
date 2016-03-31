/etc/init.d/nginx restart
python manage.py deploy
supervisord -c supervisor.conf
supervisorctl -c supervisor.conf reload
supervisorctl -c supervisor.conf start all
