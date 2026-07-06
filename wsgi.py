"""
WSGI Entry Point for Production Deployment
Use this with production WSGI servers like Gunicorn or Waitress
"""

from app import app

if __name__ == "__main__":
    app.run()
