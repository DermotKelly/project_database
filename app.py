from flask import Flask, render_template, flash
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from config import Config
import os

# Create Flask Instance
app = Flask(__name__)
app.config.from_object(Config)
#Add Database
app.config['SQLALCHEMY_DATABASE_URL'] ="postgresql://flask_database_xgsr_user:YKzko8LPSvHHdM3pyZIggJmUSj7NhoZL@dpg-ck6ap59i0euc73b40on0-a.oregon-postgres.render.com/flask_database_xgsr"

#app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
#app.config['SECRET_KEY'] = "my secret key"
#Initialise Database
db = SQLAlchemy(app)

# Activate Anti Cross-Site Request Forgery

app.config.update(dict(
SECRET_KEY="powerful secretkey",
WTF_CSRF_SECRET_KEY="a csrf secret key"))


def __repr_(self):
   return '<Name %r>' % self.name

# Create Model for Database
class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(150), nullable=False, unique=True)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    #Create A String
    def __repr__(self) -> str:
        return super().__repr__()

# Create a route decorator
    @app.route('/')
    def index():
        favorite_pizza = ['cheese','Ham','Mushroom']
        return render_template("index.html", favorite_pizza=favorite_pizza)

@app.route('/user/<name>')
def user(name):
    return render_template("user.html", name=name)



# Create Form Class
class UserForm(FlaskForm):
    name = StringField('What is your Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired()])
    submit = SubmitField('Submit')

# Create Form Class
class NamerForm(FlaskForm):
    name = StringField('What is your Name', validators=[DataRequired()])
    submit = SubmitField('Submit')



# Create Name Page
@app.route('/name', methods=['GET','POST'])
def name():
    name=None
    form=NamerForm()
    if form.validate_on_submit():
        name = form.name.data
        form.name.data = ''
        flash('FormSubmitted Successfully') # Submit Message

    return render_template("name.html", name=name, form=form)


@app.route('/user/add', methods=['GET','POST'])
def add_user():
    name = None
    form = UserForm()
    if form.validate_on_submit():
        user = Users.query.filter_by(email=form.email.data).first()
        if user is None:
            user = Users(name=form.name.data, email=form.email.data)
            db.session.add(user)
            db.session.commit()
            name = form.name.data
            form.name.data = ''
            form.email.data = ''
            flash ('User added Successfully')
    our_users = Users.query.order_by(Users.id)
    return render_template("add_user.html", form=form, name=name, our_users=our_users)

# Create Custom Error Pages
# Invalid URL
@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404

# Internal Server Errorvalid URL
@app.errorhandler(500)
def page_not_found(e):
    return render_template("500.html"), 500


with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)
