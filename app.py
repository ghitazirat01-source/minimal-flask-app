from flask import Flask, render_template, request

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def home():
    object_description = ""

    if request.method == "POST":
        object_description = request.form["object_description"]
        print("Object received:", object_description)

    return render_template(
        "index.html",
        object_description=object_description
    )


if __name__ == "__main__":
    app.run(debug=True, port=5001)