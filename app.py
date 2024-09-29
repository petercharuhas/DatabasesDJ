from flask import Flask, render_template, redirect, url_for, flash
from models import db, Playlist, Song, playlist_songs
from forms import PlaylistForm, SongForm, NewSongForPlaylistForm

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://username:password@localhost/playlist-app'  # Update with your credentials
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'Zozi'  # Set your secret key here

# Initialize the database
db.init_app(app)

@app.route('/')
def index():
    return render_template('index.html')  # Render the index.html template

@app.route('/playlists/new', methods=['GET', 'POST'])
def create_playlist():
    form = PlaylistForm()
    if form.validate_on_submit():
        new_playlist = Playlist(name=form.name.data, description=form.description.data)
        db.session.add(new_playlist)
        db.session.commit()
        flash('Playlist created successfully!', 'success')
        return redirect(url_for('create_playlist'))
    return render_template('create_playlist.html', form=form)

@app.route('/songs/new', methods=['GET', 'POST'])
def create_song():
    form = SongForm()
    if form.validate_on_submit():
        new_song = Song(title=form.title.data, artist=form.artist.data, album=form.album.data, release_year=form.release_year.data)
        db.session.add(new_song)
        db.session.commit()
        flash('Song added successfully!', 'success')
        return redirect(url_for('create_song'))
    return render_template('create_song.html', form=form)

@app.route("/playlists/<int:playlist_id>/add-song", methods=["GET", "POST"])
def add_song_to_playlist(playlist_id):
    """Add a song to a playlist and redirect to the playlist view."""
    playlist = Playlist.query.get_or_404(playlist_id)
    form = NewSongForPlaylistForm()

    # Restrict form to songs not already on this playlist
    curr_on_playlist = [s.id for s in playlist.songs]
    form.song.choices = [(song.id, song.title) for song in Song.query.filter(Song.id.notin_(curr_on_playlist)).all()]

    if form.validate_on_submit():
        # Add the song to the playlist
        playlist_song = playlist_songs.insert().values(playlist_id=playlist_id, song_id=form.song.data)
        db.session.execute(playlist_song)
        db.session.commit()

        flash('Song added to playlist successfully!', 'success')
        return redirect(url_for('add_song_to_playlist', playlist_id=playlist_id))

    return render_template("add_song_to_playlist.html", playlist=playlist, form=form)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Create database tables
    app.run(debug=True)