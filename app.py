from flask import Flask, render_template, url_for, request, jsonify
import os, json

app = Flask(__name__)

@app.route('/', methods=['GET', "POST"])
def index():
  return render_template('index.html')

  # Didier makes a API here
@app.route('/api/v1/firmware', methods=['GET'])
def api_all():
  SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
  json_url = os.path.join(SITE_ROOT, "static/js", "data.json")
  data = json.load(open(json_url))
  return jsonify(data)

  # Didier sends mail to client

if __name__ == '__main__':
  port = int(os.environ.get('PORT', 5000))
  app.run(host = '0.0.0.0', port = port)