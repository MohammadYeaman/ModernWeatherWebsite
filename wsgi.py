from app import app
from waitress import serve

if __name__ == "__main__":
  print("Starting production WSGI server on http://127.0.0.1:5000 ...")
  # Serve the Flask app using Waitress
  serve(app, host="127.0.0.1", port=5000, threads=4)