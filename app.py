"""Flask app for Cupcakes"""

from flask import Flask, render_template, redirect, request, flash, jsonify
from flask_cors import CORS
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, Cupcake


app = Flask(__name__)
CORS(app)

app.config['SECRET_KEY'] = "abcdef"

app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql:///cupcakes"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config["CORS_SUPPORTS_CREDENTIALS"]=True

toolbar = DebugToolbarExtension(app)

connect_db(app)
db.create_all()


def serialize_cupcake(cupcake):
    """Serialize a cupcake SQLAlchemy obj to dictionary."""

    return {
        "id": cupcake.id,
        "flavor": cupcake.flavor,
        "size": cupcake.size,
        "rating": cupcake.rating,
         "image": cupcake.image,
    }

@app.route('/')
def homepage():
    """render home page"""
    return render_template('index.html')

@app.route('/api/cupcakes')
def show_cupcakes():
    """Get data about all cupcakes"""

    cupcakes = [ serialize_cupcake(cupcake) for cupcake in Cupcake.query.all()]
    return jsonify(cupcakes=cupcakes)

@app.route('/api/cupcakes', methods=["POST"])
def create_cupcake():
    """Add cupcake and return data about new cupcake"""

    data = request.json

    cupcake = Cupcake(flavor=data['flavor'],
                    rating=data['rating'],
                    size=data['size'],
                    image=data['image' or None])
    db.session.add(cupcake)
    db.session.commit()

    return (jsonify(cupcake=serialize_cupcake(cupcake)), 201)

@app.route('/api/cupcakes/<int:cupcake_id>')
def show_cupcake(cupcake_id):
    """Get data about a single cupcake"""

    cupcake = Cupcake.query.get_or_404(cupcake_id)
    serialized = serialize_cupcake(cupcake)

    return jsonify(cupcake=serialized)

@app.route('/api/cupcakes/<int:cupcake_id>', methods=['PATCH'])
def update_cupcake(cupcake_id):
    """update a cupcake"""

    cupcake = Cupcake.query.get_or_404(cupcake_id)
    data = request.json

    cupcake.flavor = data.get('flavor', cupcake.flavor)
    cupcake.rating = data.get('rating', cupcake.rating)
    cupcake.size = data.get('size', cupcake.size)
    cupcake.image = data.get('image', cupcake.image)

    db.session.add(cupcake)
    db.session.commit()
    
    return jsonify(cupcake=serialize_cupcake(cupcake))

@app.route('/api/cupcakes/<int:cupcake_id>', methods=['DELETE'])
def delete_cupcake(cupcake_id):
    """delete a cupcake"""

    cupcake = Cupcake.query.get_or_404(cupcake_id)
    db.session.delete(cupcake)
    db.session.commit()

    return jsonify(message="deleted")
