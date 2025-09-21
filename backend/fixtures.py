
import json
from db import Article, Author, Tag, Category

def read_json(filename) -> dict[str, str]:
    with open(f"data/{filename}.json") as fl:
        content = json.loads(fl.read())
    return content

def add_categories():

    cat_data = {}
    with Category.sql_cursor(echo=True) as db:
        for row in read_json("categories"):
            category = Category()
            category.name = row['name'].lower()
            qry = db.query(Category.id).filter(
                Category.name == category.name
            ).first()

            if not qry:
                cat_data[category.name] = category.save(db)
            else:
                cat_data[category.name] = qry.id

    return cat_data


def seed_knowledge_base():

    file_src = ['python-tutorials', "golang"]
    cat_data = add_categories()

    with Article.sql_cursor(echo=True) as db:

        for _fl in file_src:
            data = read_json(_fl)
            for row in data:
                author = Author()
                author.name = row['author'].lower()
                author.bio = row['bio'][:280]

                is_exist = db.query(Author.id).filter_by(name=author.name).first()
                if not is_exist:
                    author_id = author.save(db)
                else:
                    author_id = is_exist.id

                article = Article()
                article.title = row['title'].lower()
                article.content = row['data']
                article.embedding = row['embedding']
                article.publish_date = article.get_timenow()
                article.author_id = author_id
                article.category_id = cat_data.get(row['category'].lower())

                is_exist = db.query(Article.id).filter(Article.title==article.title).first()
                if not is_exist:
                    article.save(db)
                else:
                    _changes = Article.update_columns(
                        Article.id == is_exist.id,
                        title=row['title'].lower(),
                        content=article.content,
                        embedding=article.embedding,
                        author_id=author_id,
                        category_id=article.category_id,
                        date_updated=article.get_timenow()
                    )
                    db.execute(_changes)



if __name__ == "__main__":
    seed_knowledge_base()
