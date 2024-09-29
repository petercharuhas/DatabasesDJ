from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, SelectField
from wtforms.validators import DataRequired

class PlaylistForm(FlaskForm):
    name = StringField('Playlist Name', validators=[DataRequired()])
    description = TextAreaField('Description')
    submit = SubmitField('Create Playlist')

class SongForm(FlaskForm):
    title = StringField('Song Title', validators=[DataRequired()])
    artist = StringField('Artist', validators=[DataRequired()])
    album = StringField('Album')
    release_year = StringField('Release Year')
    submit = SubmitField('Add Song')

class NewSongForPlaylistForm(FlaskForm):
    song = SelectField('Select a Song', validators=[DataRequired()])
    submit = SubmitField('Add Song to Playlist')
