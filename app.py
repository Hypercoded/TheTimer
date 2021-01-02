from flask import Flask, render_template

import dataHandler


app = Flask(__name__)


@app.route("/")
def home():
    endDate = dataHandler.retrieve_stats("endDate")
    endDateFormatted = dataHandler.retrieve_stats("endDateFormatted")
    return render_template("main.html", endDate=endDate, endDateFormatted=endDateFormatted)


if __name__ == "__main__":
    app.run()
