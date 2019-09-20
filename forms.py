from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField, IntegerField
from wtforms.fields.html5 import TelField
from wtforms.validators import DataRequired, Length,Email
class AddDataForm(FlaskForm):


    uname=StringField('uname', validators=[DataRequired(),Length(min=2, max=20)])
    email=StringField('email', validators=[DataRequired(),Email()])
    phno= IntegerField('phno',validators=[DataRequired(),Length(10)])
    add=SubmitField('AddUser')


class RemoveUser(FlaskForm):
    snoo= IntegerField('snoo',validators=[DataRequired(),Length(10)])
    Remove=SubmitField('Removeuser')


class UpdateUser(FlaskForm):
    sno= IntegerField('sno',validators=[DataRequired(),Length(10)])
    uname=StringField('uname', validators=[Length(min=2, max=20)])
    email=StringField('email', validators=[Email()])
    phno= IntegerField('phno',validators=[Length(10)])
    update=SubmitField('UpdateUser')
