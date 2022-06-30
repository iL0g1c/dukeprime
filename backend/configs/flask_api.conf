<VirtualHost *:80>
		ServerName 45.76.164.130
		ServerAdmin email@mywebsite.com
		WSGIScriptAlias / /var/www/backend/flask_api.wsgi
		<Directory /var/www/backend/flask_api/>
			Order allow,deny
			Allow from all
		</Directory>
		Alias /static /var/www/backend/flask_api/static
		<Directory /var/www/backend/flask_api/static/>
			Order allow,deny
			Allow from all
		</Directory>
		ErrorLog ${APACHE_LOG_DIR}/error.log
		LogLevel warn
		CustomLog ${APACHE_LOG_DIR}/access.log combined
</VirtualHost>
