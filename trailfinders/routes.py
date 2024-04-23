from flask import render_template, request, redirect, url_for
from trailfinders import app, db
from trailfinders.models import User, Hike, Category


@app.route("/")
def home():
    return render_template("index.html")
