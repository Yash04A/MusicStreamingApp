from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed
from wtforms import StringField, PasswordField,DateTimeField, DateField, FileField
from wtforms.validators import DataRequired, Email, Length, ValidationError, Optional
from models import User
from datetime import datetime

class RegistrationForm(FlaskForm):
    email = StringField('Email', validators=[Email(), DataRequired()])
    username = StringField('Display Name', validators=[Length(max=15), DataRequired()])
    fname = StringField('First Name', validators=[DataRequired(), Length(min=1, max=25)])
    lname = StringField('Last Name', validators=[DataRequired(), Length(min=1, max=25)])
    dob = DateField('Birthdate', format='%Y-%m-%d', default=None,  validators=[Optional()])
    password = PasswordField('Password', validators=[Length(min=8), DataRequired()])

    def validate_email(self, email):
        if User.query.filter_by(email=email.data).first():
            raise ValidationError("User already exists! Try different email?")
        
class LoginForm(FlaskForm):
    email = StringField('Email', validators=[Email(), DataRequired()])
    password = PasswordField('Password', validators=[Length(min=8), DataRequired()])

class UpdateProfileForm(FlaskForm):
    first_name = StringField('First Name', validators=[DataRequired(), Length(min=1, max=25)])
    last_name = StringField('Last Name', validators=[DataRequired(), Length(min=1, max=25)])
    username = StringField('Display Name', validators=[Length(max=15), DataRequired()])
    dob = DateField('Birthdate', format='%Y-%m-%d', validators=[Optional()])
    password = PasswordField('Password', validators=[Length(min=8), DataRequired()])
    img = FileField('Image File', 
                    default=None,  
                    validators=[Optional(), FileAllowed(['jpg', 'jpeg'], 'Only JPEG images are allowed.')]
                    )

class CreatorForm(FlaskForm):
    username = StringField('Display Name', validators=[Length(max=15), DataRequired()])
    password = PasswordField('Password', validators=[Length(min=8), DataRequired()])

class SongForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    genre = StringField('Genre', validators=[DataRequired()])
    release_date = DateTimeField('Release Date', default=datetime.utcnow)
    audio = FileField('Audio File', validators=[DataRequired(), FileAllowed(['mp3'], 'Only MP3 audio file are allowed.')])
    lyrics = FileField('Lyrics File', validators=[DataRequired(), FileAllowed(['txt'], 'Only TXT files are allowed.')])
    img = FileField('Image File', validators=[DataRequired(), FileAllowed(['jpg', 'jpeg'], 'Only JPG images are allowed.')])

class UpdateSongForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    genre = StringField('Genre', validators=[DataRequired()])

class AlbumForm(FlaskForm):
    title = StringField('Album Title', validators=[DataRequired()])
    img = FileField('Image File', validators=[FileAllowed(['jpg', 'jpeg'], 'Only JPG images are allowed.')])
    released_date = DateTimeField('Release Date', default=datetime.utcnow)


class PlaylistForm(FlaskForm):
    title = StringField('Album Title', validators=[DataRequired()])
    img = FileField('Image File', validators=[FileAllowed(['jpg', 'jpeg'], 'Only JPG images are allowed.')])
    created_on = DateTimeField('Release Date', default=datetime.utcnow)
    



