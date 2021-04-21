from flask import Flask, render_template
import os

app = Flask(__name__)

@app.route('/', methods=['GET', "POST"])
def index():
  return render_template('index.html')

  # Didier makes a API here
  # Didier sends mail to client

if __name__ == '__main__':
  port = int(os.environ.get('PORT', 5000))
  app.run(host = '0.0.0.0', port = port)