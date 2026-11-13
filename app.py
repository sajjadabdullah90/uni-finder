
from flask import Flask, render_template, request, jsonify
from university_api import search_universities

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/api/universities", methods=["GET"])
def universities():
    name = request.args.get("name", "").strip()
    country = request.args.get("country", "").strip()

    if not name and not country:
        return jsonify({
            "error": "Please enter a university name or country."
        }), 400

    try:
        results = search_universities(
            name=name or None,
            country=country or None
        )

        return jsonify({
            "count": len(results),
            "results": results
        })

    except Exception:
        app.logger.exception("University API request failed")

        return jsonify({
            "error": "Unable to retrieve university data. Please try again."
        }), 502


if __name__ == "__main__":
    app.run(debug=True)
