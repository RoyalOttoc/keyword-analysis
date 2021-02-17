# For flask implementation
from flask import Flask, render_template, request, redirect
from pymongo import MongoClient


app = Flask(__name__)
client = MongoClient("mongodb+srv://test:test@cluster0.pkhxf.mongodb.net/ndisdata?retryWrites=true&w=majority")  # host uri
db = client.ndisdata  # Select the database
posts = db.private  # Select the collection name
posts.create_index([("post", "text")])


@app.route("/")
def home_page():
    posts_l = posts.find()
    return render_template("index.html",
                           posts=posts_l)


@app.route("/search")
def search():
    word = request.args.get('word')

    if word:
        word = word.lower()
        results = posts.find({"$text": {"$search": word}})
    else:
        return redirect("/")
    return render_template("search.html", searchingBy=word, results=results, totalNumber=results.count())


if __name__ == "__main__":

    app.run()
