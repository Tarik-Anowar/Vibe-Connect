from flask import Flask, render_template
from db import database_connection, fetch_all_posts
from extract_topic import extract_topics_from_text

app = Flask(__name__)

# Establish the database connection
database_connection(app)

@app.route('/')
def index():
    posts = fetch_all_posts()
    for post in posts:
        post["extracted_topics"] = extract_topics_from_text(post["description"])
    return render_template('index.html',posts=posts)

if __name__ == "__main__":
    app.run(debug=True)
