from flask import Flask, render_template, request
import wikipedia

app = Flask(__name__)
app.secret_key = "development-key"   # 简单用法，方便运行（课程允许）


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        query = request.form.get("query").strip()

        if not query:
            return render_template("index.html", error="Please enter a search term.")

        try:
            page = wikipedia.page(query, auto_suggest=False)
            return render_template("result.html", title=page.title,
                                   summary=wikipedia.summary(query, sentences=5),
                                   url=page.url)

        except wikipedia.exceptions.DisambiguationError as e:
            return render_template("index.html", options=e.options[:10],
                                   error="Too many results — please choose a more specific title.")

        except wikipedia.exceptions.PageError:
            return render_template("index.html", error="Page not found — try a different search.")

    return render_template("index.html")
