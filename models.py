''' MODELS MODULE'''

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def setup_db(app):
    app.config['SQLALCHEMY_DATABASE_URI']='postgresql://valerian@localhost:5432/capstone-ardelean'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=True
    db.app = app


'''IMPLEMENT PROVIDERS CLASS WITH ALOCATED FUNCTIONS'''
class Providers(db.Model):
    __tablename__ = 'providers'
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(200))
    services_offered = db.Column(db.String(200))
    city = db.Column(db.String())
    adress = db.Column(db.String(150))
    phone = db.Column(db.String(30))
    website = db.Column(db.String(120))
    social_media = db.Column(db.String(500))
    image_link = db.Column(db.String(700))
    events = db.relationship('Events',backref='providers')

    def insert(self):
      db.session.add(self)
      db.session.commit()

    def update(self):
      db.session.commit()

    def delete(self):
      db.session.delete(self)
      db.session.commit()

    def sesion_close(self):
        db.session.close()

    def format(self):
      return {
        'id': self.id,
        'name': self.name,
        'services_offered':self.services_offered,
        'city': self.city,
        'adress': self.adress,
        'phone': self.phone,
        'website':self.website,
        'social_media':self.social_media,
        'image_link':self.image_link,

      }

'''IMPLEMENT EVENTS CLASS WITH ALOCATED FUNCTIONS'''
class Events(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    event_name = db.Column(db.String())
    event_type = db.Column(db.String())
    date = db.Column(db.DateTime)
    rating = db.Column(db.Integer)
    customer_id = db.Column(db.Integer,db.ForeignKey('customers.id'))
    provider_id = db.Column(db.Integer,db.ForeignKey('providers.id'))

    def insert(self):
      db.session.add(self)
      db.session.commit()

    def update(self):
      db.session.commit()

    def delete(self):
      db.session.delete(self)
      db.session.commit()

    def sesion_close(self):
        db.session.close()

    def format(self):
      return {
        'id': self.id,
        'event_name': self.event_name,
        'event_type': self.event_type,
        'date': self.date,
        'rating': self.rating,
        'customer_id':self.customer_id,
        'provider_id':self.provider_id
      }

'''IMPLEMENT CUSTOMERS CLASS WITH ALOCATED FUNCTIONS'''
class Customers(db.Model):
    __tablename__ = 'customers'
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(200))
    city = db.Column(db.String)
    adress = db.Column(db.String(150))
    phone = db.Column(db.String(30))
    social_media = db.Column(db.String(100))
    image_link = db.Column(db.String(500))
    events = db.relationship('Events',backref='customers')

    def insert(self):
      db.session.add(self)
      db.session.commit()

    def update(self):
      db.session.commit()

    def delete(self):
      db.session.delete(self)
      db.session.commit()

    def sesion_close(self):
        db.session.close()

    def format(self):
      return {
        'id': self.id,
        'name': self.name,
        'city': self.city,
        'adress': self.adress,
        'phone': self.phone,
        'social_media':self.social_media,
        'image_link':self.image_link,
      }
