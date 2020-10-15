from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def setup_db(app):
    app.config['SQLALCHEMY_DATABASE_URI']='postgresql://valerian@localhost:5432/capstone-ardelean'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=True
    db.app = app


class Providers(db.Model):
    __tablename__ = 'providers'
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(200))
    area = db.Column(db.String())
    adress = db.Column(db.String(150))
    phone = db.Column(db.String(30))
    website = db.Column(db.String(120))
    social_media = db.Column(db.String(500))
    image_link = db.Column(db.String(500))
    events = db.relationship('Events',backref='providers')


class Events(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    event_name = db.Column(db.String())
    event_type = db.Column(db.String())
    date = db.Column(db.DateTime)
    rating = db.Column(db.Integer)
    customer_id = db.Column(db.Integer,db.ForeignKey('customers.id'))
    provider_id = db.Column(db.Integer,db.ForeignKey('providers.id'))


class Customers(db.Model):
    __tablename__ = 'customers'
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(200))
    area = db.Column(db.String)
    adress = db.Column(db.String(150))
    phone = db.Column(db.String(30))
    social_media = db.Column(db.String(100))
    image_link = db.Column(db.String(500))
    events = db.relationship('Events',backref='customers')
