from flask import Flask, render_template
from flask import jsonify, make_response

app = Flask(__name__)
from app.dash_application import build_dash

@app.route("/")
def home():
    """Landing page."""
    return render_template(
        'index.jinja2',
        title='Stocks Dashboard',
        description='Stock dashboard to assist trading',
        template='home-template',
        body="This is a homepage served with Flask."
    )

build_dash(app)