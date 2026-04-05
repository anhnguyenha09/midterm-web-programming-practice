#CAU 5 - VIET CLIENT FLASK
from flask import Flask, render_template
import urllib.request
import json

app = Flask(__name__)

API_URL = "http://127.0.0.1:5000/Employee"

@app.route("/")
def index():
    #goi API GET de lay danh sach employee
    with urllib.request.urlopen(API_URL) as response:
        data = json.loads(response.read().decode())
    return render_template("index.html", employees=data)

if __name__ == "__main__":
    app.run(debug=True, port=5001) #chay cong khac voi api
