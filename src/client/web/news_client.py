import os
import csv

from flask import Flask, render_template, request

app = Flask(__name__)


@app.route("/")
def show_startpage():
    return render_template("start.html")


@app.route("/list")
def list_news():
    print(request.args)
    news = read_data()
    return render_template("list_news.html", news=news)

@app.route("/statistics")
def show_stats():
    return render_template("analyse_news.html")


# Einlesen der Datenfiles aus /data
def read_data():

    news = []
    app_dir = os.path.dirname(os.path.dirname(__file__))
    data_dir = os.path.join(app_dir, "data")
    print(data_dir)

    for file in os.listdir(data_dir):

        print(file)
        print(file.title())

        if file.title().endswith('.Csv'):

            with open(os.path.join(data_dir, file), 'r', newline='', encoding='utf-8') as data_file:

                csv_reader = csv.reader(data_file, delimiter=';', quotechar='"')
                for row in csv_reader:
                    news.append(row)
                    #print(row)

    # nach Datum sortieren
    news.sort(key=lambda item: item[0], reverse=True)

    return news

