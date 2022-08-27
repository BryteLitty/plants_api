import os
from flask import Flask
# from flask_sqlalchemy import SQLAlchemy
from flask_sqlalchemy import SQLAlchemy
import json


 
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://postgres@localhost:5432/parch"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# @app.route('/')
# def testdb():
#     try:
#         db.session.query("1").from_statement("SELECT 1").all()
#         return '<h1>It works.</h1>'
#     except:
#         return '<h1>Something is broken.</h1>'

"""Plant class"""


class Plant(db.Model):
    __tablename__ = "plants"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    scientific_name = db.Column(db.String)
    is_poisonous = db.Column(db.Boolean)
    primary_color = db.Column(db.String)

    db.create_all()

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