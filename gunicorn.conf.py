import os

bind = f"0.0.0.0:{os.environ.get('PORT', 8080)}"
workers = 1
timeout = 120
preload_app = True
wsgi_app = "app:app"
