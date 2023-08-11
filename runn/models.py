#import dateTime as dateTime
from DateTime import DateTime
from sqlalchemy import func
from itsdangerous import URLSafeTimedSerializer as serializer
from sqlalchemy.dialects.mysql import LONGTEXT

from runn import db, login_manager, app
from flask_login import UserMixin, LoginManager
import datetime


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(UserMixin ,db.Model):
    @property
    def is_authenticated(self):
        return True
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(25), nullable=False)
    email = db.Column(db.String(125), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    #this function takes user and creates token that is used to verify which user need to reset password
    def get_reset_token(self):
        s=serializer(app.config['SECRET_KEY'],salt='ps-reset')
        return s.dumps({'user_id':self.id})
    #This function takes the token and returns the user that has this token
    @staticmethod
    def verify_reset_token(token,age=3600):
        s=serializer(app.config['SECRET_KEY'],salt='ps-reset')
        try:
            user_id=s.loads(token,max_age=age)['user_id']
        except:
            return None
        return User.query.get(user_id)

    def __repr__(self):
        return f"User('{self.id}', '{self.name}', '{self.email}')"


class Info(db.Model):
    name=db.Column(db.String(100) ,primary_key=True)
    common_name=db.Column(db.String(100))
    how_to_control=db.Column(LONGTEXT,nullable=False)
    damage=db.Column(LONGTEXT,nullable=False)

    def __repr__(self):
        return f"info('{self.name}', '{self.common_name}', '{self.how_to_control}','{self.damage}')"

class Image_User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    value=db.Column(db.String(120),nullable =False)
    userid=db.Column(db.Integer,db.ForeignKey('user.id'),nullable=False)
    result=db.Column(db.String(50))
    created_date = db.date = db.Column(db.Date,default=func.current_date())
    created_at = db.Column(db.DateTime, default=func.current_timestamp())
    def __repr__(self):
        return f"Image('{self.id}', '{self.userid}', '{self.value}', '{self.created_date}', '{self.result}')"

