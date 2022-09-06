from flask import Flask, request, render_template
from methodes import get_one_prediction, get_all_prediction

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
        return render_template("prediction.html", data=data)


@app.context_processor
def my_utility_processor():
    def round_number(number):
        return round(number, 5)

    return dict(round=round_number)


if __name__ == '__main__':
    app.run(debug=True)
