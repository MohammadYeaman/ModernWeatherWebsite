import os
from app import app
from waitress import serve

if __name__ == "__main__":
  # Grab Render's dynamic port, defaulting to 5000 for local testing
  port = int(os.environ.get("PORT", 5000))

  print(f"Starting production WSGI server on 0.0.0.0:{port} ...")

  # Bind to 0.0.0.0 so Render can detect the open port
  serve(app, host="0.0.0.0", port=port, threads=4)