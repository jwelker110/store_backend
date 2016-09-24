#!/usr/bin/python
import sys
import logging
logging.basicConfig(stream=sys.stderr)
sys.path.insert(0, "/var/www/catalog/store_backend/")
from store_app import create_app

application = create_app()

if __name__ == '__main__':
    app.run(port=8080)
