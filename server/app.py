#!/usr/bin/env python3

from flask import Flask, make_response, jsonify
from flask_migrate import Migrate

from models import db, Bakery, BakedGood

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/')
def index():
    return '<h1>Bakery GET API</h1>'

@app.route('/bakeries')
def bakeries():
    all_bakeries = []
    bakeries = Bakery.query.all()

    for bakery in bakeries:
        bakery_dict = bakery.to_dict()
        all_bakeries.append(bakery_dict)
        
    body = all_bakeries

    response = make_response(body, 200)
    return response

@app.route('/bakeries/<int:id>')
def bakery_by_id(id):
    bakery = Bakery.query.filter_by(id=id).first()

    if bakery:
        response = bakery.to_dict()
        status = 200
    else:
        response = {
            "message": f"Error, bakery with id {id} could not be found"
        }
        status = 404
    
    return make_response(response, status)

@app.route('/baked_goods/by_price')
def baked_goods_by_price():
    baked_goods = BakedGood.query.order_by(BakedGood.price.desc()).all()
    baked_goods_list = []

    for good in baked_goods:
        good_dict = good.to_dict()
        baked_goods_list.append(good_dict)

    return make_response(baked_goods_list, 200)


@app.route('/baked_goods/most_expensive')
def most_expensive_baked_good():
    most_expensive = BakedGood.query.order_by(BakedGood.price.desc()).first()

    baked_good = most_expensive.to_dict()
    return make_response(baked_good, 200)

if __name__ == '__main__':
    app.run(port=5555, debug=True)
