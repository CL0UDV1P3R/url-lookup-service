#!/usr/bin/python
from flask import Flask, request, render_template
from helpers.url_scanner_reporter import analyze_url

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("form.html")


@app.route("/submit", methods=["POST"])
def submit():
    return analyze_url(request.form["URL"])


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8080, debug=True)
