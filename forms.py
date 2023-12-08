from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed
from wtforms import StringField, PasswordField, DateField, FileField, SelectMultipleField, widgets
from wtforms.validators import DataRequired, Email, Length, ValidationError, Optional
from models import User
from datetime import date

class RegistrationForm(FlaskForm):
    email = StringField('Email', validators=[Email(), DataRequired()])
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
    release_date = DateField('Release Date',format='%Y-%m-%d', default=date.today(), validators=[Optional()])
    audio = FileField('Audio File', validators=[DataRequired(), FileAllowed(['mp3'], 'Only MP3 images are allowed.')])
    lyrics = FileField('Lyrics File', validators=[DataRequired(), FileAllowed(['txt'], 'Only TXT images are allowed.')])
    img = FileField('Image File', validators=[DataRequired(), FileAllowed(['jpg', 'jpeg'], 'Only JPG images are allowed.')])

class UpdateSongForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    genre = StringField('Genre', validators=[DataRequired()])

class AlbumForm(FlaskForm):
    title = StringField('Album Title', validators=[DataRequired()])
    img = FileField('Image File', validators=[FileAllowed(['jpg', 'jpeg'], 'Only JPG images are allowed.')])
    release_date = DateField('Release Date',format='%Y-%m-%d', default=date.today())
    songs = SelectMultipleField('Songs', coerce=int, widget=widgets.ListWidget(prefix_label=False), option_widget=widgets.CheckboxInput())


class PlaylistForm(FlaskForm):
    title = StringField('Album Title', validators=[DataRequired()])
    img = FileField('Image File', validators=[FileAllowed(['jpg', 'jpeg'], 'Only JPG images are allowed.')])
    release_date = DateField('Release Date',format='%Y-%m-%d', default=date.today())
    songs = SelectMultipleField('Songs', coerce=int, widget=widgets.ListWidget(prefix_label=False), option_widget=widgets.CheckboxInput())



