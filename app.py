# THIRD-PARTY MODULES
from flask import Flask


# LOCAL MODULES
from database import setup_db

app = Flask(__name__)
setup_db(app)


@app.route("/")
def index():
    return "Welcome to API"


if __name__ == "__main__":
    app.run()
