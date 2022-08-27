from operator import methodcaller
from re import S
from urllib import request
from flask import Flask, jsonify, request, abort
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
import os
import sys
from flask_migrate import Migrate
    
     
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://postgres@localhost:5432/plantsdb"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)


"""Plant class"""


class Plant(db.Model):
    __tablename__ = "plants"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    scientific_name = db.Column(db.String)
    is_poisonous = db.Column(db.Boolean)
    primary_color = db.Column(db.String)


    def __init__(self, name, scientific_name, is_poisonous, primary_color):
        self.name = name
        self.scientific_name = scientific_name
        self.is_poisonous = is_poisonous
        self.primary_color = primary_color


    def insert(self):
        db.session.add(self)
        db.session.commit()


    def update(self):
        db.session.commit()


    def delete(self):
        db.session.delete(self)
        db.session.commit()


    def format(self):
        return {
            "id": self.id,
            "name": self.name,
            "scientific_name": self.scientific_name,
            "is_poisonous": self.is_poisonous,
            "primary_color": self.primary_color,
        }

@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization')
    response.headers.add('Access-Control-Allow-Headers', 'GET, POST, PATCH, DELETE, OPTIONS')
    return response


# @cross_origin
@app.route('/plants', methods=['GET', 'POST'])
def get_plants():
    page = request.args.get('page', 1, type=int)
    start = (page - 1) * 10
    end = start + 10
    plants = Plant.query.all()
    formatted_plants = [plant.format() for plant in plants]

    return jsonify({
        "success": True,
        "plants": formatted_plants[start:end],
        "total_plants": len(formatted_plants)
    })

@app.route('/plants/<int:plant_id>')
def get_specific_plant(plant_id):
    plant = Plant.query.filter(Plant.id == plant_id).one_or_none()

    if plant is None:
        abort(404)

    else:

        return jsonify({
            'success': True,
            'plant': plant.format()
        })



    return app