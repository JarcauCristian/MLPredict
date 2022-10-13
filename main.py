import csv
import json
from pprint import pprint

from flask import Flask, request, render_template
from methodes import get_one_prediction, get_all_prediction, get_one_prediction_all_data

app = Flask(__name__)


@app.route('/', methods=["GET", "POST"])
def first_page():
    return render_template("base.html")


@app.route('/predict', methods=["POST"])
def get_predictions():
    if request.method == "POST":
        pat_id = request.form.get("name")
        model_version = request.form.get("model_version")
        all_pts = request.form.get("all")
        data = {}
        if all_pts == "one":
            data = get_one_prediction(model_version, int(pat_id))
        elif all_pts == "all":
            data = get_all_prediction(model_version)
        elif all_pts == "graph":
            data = get_one_prediction_all_data(model_version, int(pat_id))
            return render_template("graphs.html", data=data, list_of_items=data[int(pat_id)][1], letters=data[int(pat_id)][0])
        return render_template("prediction.html", data=data)


@app.route('/data', methods=["GET"])
def get_data():
    with open('patData.csv', 'r') as csv_in:
        csv_reader = csv.reader(csv_in)
        data = {}
        for index, row in enumerate(csv_reader):
            if index == 0:
                continue
            else:
                data[row[0]] = row[1]

    return render_template("scenario1.html", data=data)


@app.context_processor
def my_utility_processor():
    def round_number(number):
        return round(number, 5)

    def array_len(array):
        return len(array)

    def round_to_int(number):
        return int(round(number, 2) * 100)

    def return_pat_id(pat_id):
        return "Patient id:" + str(pat_id)

    def print_data(data):
        print(data)

    return dict(round=round_number, len=array_len, id=return_pat_id, rnd=round_to_int, print_data=print_data)


if __name__ == '__main__':
    app.run(debug=True)
