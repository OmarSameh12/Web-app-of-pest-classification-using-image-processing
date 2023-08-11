import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
import tensorflow as tf
from keras.models import Sequential
from keras.models import Model
from keras import layers
from keras.layers import Dense
from flask_sqlalchemy import SQLAlchemy
import pymysql
from flask_mail import Mail

pymysql.install_as_MySQLdb()

app = Flask(__name__)


model=Sequential()
base_model = tf.keras.applications.DenseNet121( include_top = False, weights = 'imagenet', input_shape=(224,224,3))
for layer in base_model.layers:
  layer.trainable = False
x = base_model.output
x = layers.GlobalAveragePooling2D()(x)
x = layers.Dense(1024, activation='relu')(x)
x = layers.BatchNormalization()(x)  # Add batch normalization for regularization
x = layers.Dropout(0.5)(x)  # Increase dropout rate for regularization
x = layers.Dense(512, activation='relu')(x)  # Add an additional dense layer
x = layers.BatchNormalization()(x)  # Add batch normalization
x = layers.Dropout(0.5)(x)  # Increase dropout rate
predictions = Dense(31, activation='softmax')(x)
# Model to be trained
model = Model(inputs=base_model.input, outputs=predictions)


model.load_weights('modeel.h5')



app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:1234@127.0.0.1/BugBust'

db = SQLAlchemy(app)
app.config['SECRET_KEY'] = 'dfb31de557a0d8c2a7012709e744001bd0c01975fc900c4916c9e0c6ce556885'
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

app.config['MAIL_SERVER']='smtp.googlemail.com'
app.config['EMAIL_PORT']=587
app.config['MAIL_USE_TLS']=True
app.config['MAIL_USERNAME']='bugbustt@gmail.com '
app.config['MAIL_PASSWORD']='zqmgemhwrmshcpot'
mail=Mail(app)


from runn import routes

