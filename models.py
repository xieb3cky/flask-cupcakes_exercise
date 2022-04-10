"""Models for Cupcake app."""

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

DEFAULT_IMAGE_URL = "https://tinyurl.com/demo-cupcake"

class Cupcake(db.Model):
    """Adoptable pet."""

    __tablename__ = "cupcakes"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    flavor = db.Column(db.Text, nullable=False)
    size = db.Column(db.Text, nullable=False)
    rating = db.Column(db.Integer)
    image = db.Column(db.Text, nullable=False, default=DEFAULT_IMAGE_URL)



def connect_db(app):

    db.app = app
    db.init_app(app)
