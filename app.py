from flask import Flask, render_template, request, redirect, url_for, session, flash
from sqlalchemy import Integer, String, Column, Boolean
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from sqlalchemy.orm import DeclarativeBase
from flask_bootstrap import Bootstrap
from wtforms.fields.simple import StringField, BooleanField, SubmitField
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cafes.db'
key = os.environ.get('key')
app.config['SECRET_KEY'] = key
Bootstrap(app)
print(key)
db = SQLAlchemy()
db.init_app(app)


class Cafe(db.Model):
    __tablename__ = 'cafe'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), unique=True, nullable=False)
    map_url = db.Column(db.String(500), nullable=False)
    img_url = db.Column(db.String(500), nullable=False)
    location = db.Column(db.String(250), nullable=False)
    has_sockets = db.Column(db.Boolean, nullable=False)
    has_toilet = db.Column(db.Boolean, nullable=False)
    has_wifi = db.Column(db.Boolean, nullable=False)
    can_take_calls = db.Column(db.Boolean, nullable=False)
    seats = db.Column(db.String(250), nullable=False)
    coffee_price = db.Column(db.String(250), nullable=True)


class CafeForm(FlaskForm):
    name = StringField('Cafe Name')
    map_url = StringField('Cafe Location on Google Maps (URL)')
    img_url = StringField('Cafe Image (URL)')
    location = StringField('Cafe Location')
    has_sockets = BooleanField('Has Sockets?')
    has_toilet = BooleanField('Has Toilets?')
    has_wifi = BooleanField('Has Wifi?')
    can_take_calls = BooleanField('Can Take Calls?')
    seats = StringField('Number of Seats')
    coffee_price = StringField('Coffee Price')
    submit = SubmitField('Submit')

@app.route('/')
def index():
    cafes = Cafe.query.all()
    return render_template('index.html', cafes=cafes)


@app.route('/list')
def cafe_list():
    cafes = Cafe.query.all()
    return render_template('cafe-list.html', cafes=cafes)

@app.route('/add', methods=['GET', 'POST'])
def add_cafe():
    form = CafeForm()

    if form.validate_on_submit():
        new_cafe = Cafe(
            name=form.name.data,
            map_url=form.map_url.data,
            img_url=form.img_url.data,
            location=form.location.data,
            has_sockets=form.has_sockets.data,
            has_toilet=form.has_toilet.data,
            has_wifi=form.has_wifi.data,
            can_take_calls=form.can_take_calls.data,
            seats=form.seats.data,
            coffee_price=form.coffee_price.data
        )
        db.session.add(new_cafe)
        db.session.commit()
        return redirect(url_for('cafe_list'))

    return render_template('add_cafe.html', form=form)


if __name__ == '__main__':
    app.run()
