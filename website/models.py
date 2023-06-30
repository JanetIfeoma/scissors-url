from . import db 
from flask_login import UserMixin
from  sqlalchemy.sql import func
from datetime import datetime
import string
import qrcode
from random import choices
import os

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False, unique=True)
    password = db.Column(db.String(100), nullable=False)
    email= db.Column(db.String(120), nullable=False, unique= True)
    date_created = db.Column(db.DateTime(timezone=True), default= func.now())
    links =db.relationship('Link', backref='user', passive_deletes= True)



class Link(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    short_url = db.Column(db.String(5), unique=True)
    original_url = db.Column(db.String(512))
    visits = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime() , default=datetime.now)
    qr_code_path = db.Column(db.String(128), unique=True)
    user_id=db.Column(db.Integer,db.ForeignKey('user.id'), nullable=False)


    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.short_url= self.generate_short_link()
        self.generate_qr()


    def generate_short_link(self):
        characters= string.digits + string.ascii_letters
        short_url = ''.join(choices(characters, k=5))

        link=self.query.filter_by(short_url=short_url).first()
        if link:
            return self.generate_short_link()
        
        return short_url
    
    def generate_qr(self):
        qr = qrcode.QRCode(version=1, box_size=10, border=5)
        qr.add_data(self.short_url)
        qr.make(fit=True)
        qr_image = qr.make_image(fill="black", back_color="white")
        qr_code_path = f"static/qr_codes/{self.short_url}.png"
        qr_image.save(qr_code_path)
        self.qr_code_path = qr_code_path

    def get_qr_code_url(self):
        return os.path.join("/", self.qr_code_path)





        