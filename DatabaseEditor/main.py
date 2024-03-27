from flask import Flask, render_template, request, jsonify, redirect, url_for
from config import app, db
from models import MenuItem
import sqlite3

@app.route('/admin')
def admin():

    return render_template('admin.html')

@app.route('/', methods=['GET','POST'])
def add_food_item():
    data = request.get_json()

    if 'name' not in data or 'price' not in data or 'category' not in data:
        return jsonify({"error": "Missing data for name, price or category"}), 400
    con = sqlite3.connect('mydatabase.db')
    cur = con.cursor()
    # new_item = MenuItem(name=data['name'], id=data['id'], price=data['price'], category=data['category'])
    cur.execute("INSERT INTO menu_item (id, name, price, category) VALUES( id=data['id'], name=data['name'], price=data['price'], category=data['category'] ")
    #cur.execute("SELECT id, name, price, category FROM menu_item;")
    db.session.commit()
    return jsonify({"message": "Food item added successfully."}), 201

#@app.route('/menu')
#def menu():
 #   return render_template('index.html')

@app.route('/menu-item/<int:item_id>')
def get_menu_item(id):
    item = MenuItem.query.get(id)
    if item:
        return jsonify(item.to_json()), 200
    else:
        return jsonify({"error": "Item not found."}), 404


if __name__ == "__main__":
    with app.app_context():
        db.create_all()

    app.run(debug=True)