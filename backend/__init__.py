
from flask import Flask, render_template, render_template_string, send_from_directory
from dynaconf import settings
import os

app = Flask(
        __name__,
        root_path=os.getcwd(),
        static_folder=settings.STATIC_FOLDER,
        template_folder=settings.TEMPLATE_FOLDER,
    )

@app.route("/")
def index_view():
    return render_template("index.html")


@app.route("/assets/<filename>")
def render_static_file(filename):
    return send_from_directory(settings.STATIC_FOLDER, filename)

