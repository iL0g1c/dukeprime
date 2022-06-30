#!/usr/bin/python
import sys
import logging
logging.basicConfig(stream=sys.stderr)
sys.path.insert(0,"/var/www/backend/")

from flask_api import app as application
application.secret_key = 'password'
