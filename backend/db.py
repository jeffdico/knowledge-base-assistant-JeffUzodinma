import logging
from contextlib import contextmanager
from pytz import timezone
from datetime import datetime
from sqlalchemy import (
    create_engine,
    Index,
    PrimaryKeyConstraint,
    ForeignKeyConstraint,
    update, Update
)
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    Session,
    mapped_column,
    sessionmaker,
)
from pgvector.sqlalchemy import Vector
from dynaconf import settings

# +-------------------------++-------------------------+
# +-------------------------++-------------------------+

class ModelObject(DeclarativeBase):

    @staticmethod
    def get_timeaware(dateobj: datetime, timez=None) -> datetime:
        return dateobj.astimezone(timezone(timez))

    @classmethod
    def get_timenow(cls, timez=None) -> datetime:
        time_zone = timez or settings.TZ or 'UTC'
        return cls.get_timeaware(datetime.now(), time_zone)

    @classmethod
    @contextmanager
    def sql_cursor(cls, echo=False) -> None:
        engine = create_engine(
            settings.DATABASE_URI,
            echo=echo,
            pool_recycle=1800,
            pool_size=5,
            max_overflow=3
        )

        CursorObj = sessionmaker(bind=engine)
        cursor = CursorObj()

        try:
            yield cursor
            cursor.commit()

        except Exception as e:
            cursor.rollback()
            logger = logging.getLogger(settings.DBLOGGER)
            logger.exception(" ")
            raise e
        finally:
            cursor.close()

    @classmethod
    def create_tables(cls) -> None:
        engine = create_engine(settings.DATABASE_URI, echo=True)
        cls.metadata.create_all(engine)

    @classmethod
    def drop_tables(cls) -> None:
        engine = create_engine(settings.DATABASE_URI, echo=True)
        cls.metadata.drop_all(engine)

    def pre_save(self) -> None:
        if hasattr(self, 'date_created') and self.date_created is None:
            self.date_created = self.get_timenow()


    def save(self, dbins:Session|None=None) -> int:

        _id = 0
        self.pre_save()
        if dbins is not None:
            dbins.add(self)
            dbins.flush()
            return self.id

        with self.sql_cursor() as db:
            db.add(self)
            db.flush()
            _id = self.id

        return _id

    @classmethod
    def update_columns(cls, *condition, **fields) -> "Update":
        return update(
            cls
        ).where(*condition).values(fields)



# +-------------------------++-------------------------+
# +-------------------------++-------------------------+

class Author(ModelObject):
    __tablename__ = "authors"
    __table_args__ = (
        PrimaryKeyConstraint("id"),
        Index("authors_seq_idx", "id", "name")
    )

    id: Mapped[int]
    name: Mapped[str]
    bio: Mapped[str]
    date_created: Mapped[datetime]
    date_updated: Mapped[datetime]

# +-------------------------++-------------------------+
# +-------------------------++-------------------------+

class Category(ModelObject):

    __tablename__ = "categories"
    __table_args__ = (
        PrimaryKeyConstraint("id"),
        Index("category_seq_idx", "id", "name")
    )
    id: Mapped[int]
    name: Mapped[str]
    date_created: Mapped[datetime]
    date_updated: Mapped[datetime]

# +-------------------------++-------------------------+
# +-------------------------++-------------------------+

class Article(ModelObject):
    __tablename__ = "articles"
    __table_args__ = (
        PrimaryKeyConstraint("id"),
        ForeignKeyConstraint(["author_id"], ["authors.id"]),
        ForeignKeyConstraint(["category_id"], ["categories.id"]),
        Index("articles_seq_idx", "id", "title"),
        Index("articles_seq_fk_idx", "id", "author_id", "category_id"),
        Index(
            'articles_embedding_seq_idx',
            "embedding",
            postgresql_using='ivfflat',
            postgresql_with={'lists': 100},
            postgresql_ops={'embedding': 'vector_l2_ops'}
        )
    )

    id: Mapped[int]
    title: Mapped[str]
    content: Mapped[str]
    publish_date: Mapped[datetime]
    author_id: Mapped[int]
    category_id: Mapped[int]
    date_updated: Mapped[datetime]
    embedding = mapped_column(Vector(dim=1536))

# +-------------------------++-------------------------+
# +-------------------------++-------------------------+

class Tag(ModelObject):
    __tablename__ = "tags"
    __table_args__ = (
        PrimaryKeyConstraint("id"),
        ForeignKeyConstraint(["article_tags"], ["articles.id"]),
        Index("tags_seq_idx", "id", "name", "article_tags")
    )

    id: Mapped[int]
    name: Mapped[str]
    article_tags : Mapped[int]
    date_created: Mapped[datetime]
    date_updated: Mapped[datetime]

# +-------------------------++-------------------------+
# +-------------------------++-------------------------+