import json
import os
from dynaconf import settings
from flask import (
    Flask, request, jsonify,
    render_template, Response
)
from sqlalchemy import func
from flask_cors import CORS


from .helpers import setup_logging
from .llm import get_embedding, ask_ai
from .db import Article, Tag, Category, Author


# +-------------------------++-------------------------+
# +-------------------------++-------------------------+
app = Flask(
    __name__,
    static_url_path="/assets/",
    static_folder=settings.STATIC_FOLDER,
    template_folder=settings.TEMPLATE_FOLDER,
    root_path=os.getcwd(),
)

if settings.ENV == 'dev':
    CORS(app)

setup_logging(settings.DBLOGGER)
setup_logging(settings.APPLOGGER)

# +-------------------------++-------------------------+
# +-------------------------++-------------------------+
@app.route("/")
def index_view() -> Response:
    return render_template("index.html")

# +-------------------------++-------------------------+
# +-------------------------++-------------------------+

def success_response(output:list[dict[str,any]]|dict[str,any]) -> Response:
    return jsonify({"data": output})

# +-------------------------++-------------------------+
# +-------------------------++-------------------------+

@app.route("/categorylist")
def fetch_category_list() -> Response:

    with Category.sql_cursor() as db:
        cats = db.query(
            Category.name,
            Category.id
        ).all()
    cat_data = [{'id': cat.id, "value": cat.name.title()} for cat in cats]
    return success_response(cat_data)

# +-------------------------++-------------------------+
# +-------------------------++-------------------------+
@app.route("/api/search")
def query_base_view() -> Response:

    query = request.args.get("query")
    category = request.args.get("category", 0, int)
    search_data = get_embedding(query)
    score = 0.8

    with Article.sql_cursor(echo=True) as db:
        tags = db.query(
            func.array_agg(Tag.name).label("tag_list"),
            Tag.article_tags
        ).group_by(Tag.article_tags).subquery()

        qry = db.query(
            (1 - Article.embedding.cosine_distance(search_data)).label("similarity"),
            Article.id,
            Article.content,
            Article.publish_date,
            Author.name,
            Author.bio,
            tags.c.tag_list,
            Category.name.label("category")
        ).join(
            Author, Author.id == Article.author_id
        ).join(
            Category, Category.id == Article.category_id
        ).outerjoin(
            tags, tags.c.article_tags == Article.id
        ).filter(
            (1 - Article.embedding.cosine_distance(search_data)) >= score
        ).order_by(
            (1 - Article.embedding.cosine_distance(search_data)).desc(),
            Article.publish_date.desc()
        ).distinct()

        if category > 0:
            qry.filter(
                Category.id == category
            )
        qry_data = qry.all()

    retv = []
    for row in qry_data:
        print('\n', row.similarity, ", id: ", row.id, "\n\n")
        retv.append({
            "id": row.id,
            'article': row.content,
            "result": row.content[:400],
            "aurthor": row.name.title(),
            "bio": row.bio,
            "date": row.publish_date.strftime("%Y-%m-%d T %H:%M:%S %p"),
            "tags": row.tag_list,
            'category': row.category,
            "search_type": "local"
        })

    return success_response(retv)


# +-------------------------++-------------------------+
# +-------------------------++-------------------------+

@app.route("/api/ask", methods=['POST'])
def query_ai_view():
    post_data = json.loads(request.data)
    resp = ask_ai(post_data['question'])

    retv = {
        "search_type": "ai",
        "question": post_data['question'],
        "result": resp,
        'aurthor': "AI Response",
        "date": Article.get_timenow().strftime("%Y-%m-%d T %H:%M:%S %p")
    }

    return success_response([retv])
