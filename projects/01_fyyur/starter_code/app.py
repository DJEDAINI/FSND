#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

import json
import dateutil.parser
import babel
from flask import Flask, render_template, request, Response, flash, redirect, url_for
from flask_moment import Moment
from flask_migrate import Migrate
import logging
from logging import Formatter, FileHandler
from flask_wtf import Form
from forms import *
from flask_wtf.csrf import CSRFProtect
from datetime import datetime
from sqlalchemy.sql.functions import func
from itertools import groupby
from models import *

#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

moment = Moment(app)

# handles database migrations through Flask-Migrate
migrate = Migrate(app, db)

#----------------------------------------------------------------------------#
# CSRF Protection.
#----------------------------------------------------------------------------#
csrf = CSRFProtect(app)
csrf.init_app(app)

#----------------------------------------------------------------------------#
# Filters.
#----------------------------------------------------------------------------#

def format_datetime(value, format='medium'):
   # Bug, the value maybe is a datetime object
  if (isinstance(value, datetime)):
    date = value
  else:
    date = dateutil.parser.parse(value)
  if format == 'full':
    format="EEEE MMMM, d, y 'at' h:mma"
  elif format == 'medium':
      format="EE MM, dd, y h:mma"
  return babel.dates.format_datetime(date, format)

app.jinja_env.filters['datetime'] = format_datetime

#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#

@app.route('/')
def index():
  return render_template('pages/home.html')


#  Venues
#  ----------------------------------------------------------------

@app.route('/venues')
def venues():
  items = Venue.query.\
    with_entities(Venue.city, Venue.state, Venue.id, Venue.name, func.count(Show.id).label('num_shows'))\
    .join(Show, (Show.venue_id==Venue.id) & (Show.start_time < datetime.now()), isouter=True )\
    .group_by(Venue).all()
  data = []
  func_filter =  lambda item: (item.city, item.state)
  for key, venues in groupby(sorted(items, key= func_filter) , func_filter):
      tmp_venue = dict(zip(['city', 'state'], key))
      tmp_venue["venues"] = list({'id': venue.id, 'name': venue.name, 'num_upcomping_shows': venue.num_shows } for venue in venues)
      data.append(tmp_venue)
  return render_template('pages/venues.html', areas=data);

@app.route('/venues/search', methods=['POST'])
# Disable CSRF for this route.
@csrf.exempt
def search_venues():
  search_for = request.form.get('search_term', '')
  # seach for Hop should return "The Musical Hop".
  # search for "Music" should return "The Musical Hop" and "Park Square Live Music & Coffee"
  venues = Venue.query.filter(Venue.name.ilike('%' + search_for + '%')).all()
  response = {
    "count": len(list(venues)),
    "data": list(venues)
  }
  return render_template('pages/search_venues.html', results=response, search_term=search_for)

@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
  # shows the venue page with the given venue_id
  venue = Venue.query.get(venue_id).__dict__
  shows = Show.query.with_entities(Show.artist_id, Show.start_time, Artist.name.label('artist_name'), Artist.image_link.label('artist_image_link'))\
    .filter(Show.venue_id==venue_id)\
    .join(Venue, Venue.id==Show.venue_id, isouter=True)\
    .join(Artist, Artist.id==Show.artist_id, isouter=True)\
    .all()
  venue['upcoming_shows'] = list(filter(lambda show: show.start_time < datetime.now(), shows))
  venue['past_shows'] = list(filter(lambda show: show.start_time >= datetime.now(), shows))
  venue['upcoming_shows_count'] = len(venue['upcoming_shows'])
  venue['past_shows_count'] = len(venue['past_shows'])
  return render_template('pages/show_venue.html', venue=venue)

#  Create Venue
#  ----------------------------------------------------------------

@app.route('/venues/create', methods=['GET'])
def create_venue_form():
  form = VenueForm()
  return render_template('forms/new_venue.html', form=form)

@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
  form = VenueForm(request.form)
  if form.validate_on_submit():
    venue = Venue()
    form.populate_obj(venue)
    db.session.add(venue)
    db.session.commit()
    # on successful db insert, flash success
    flash('Venue ' + request.form['name'] + ' was successfully listed!')
    return redirect(url_for('index'))
  else:
    flash('An error occurred. Venue ' +  request.form['name'] + ' could not be listed.', 'error')
    return render_template('forms/new_venue.html', form=form)

@app.route('/venues/<venue_id>/delete', methods=['POST'])
def delete_venue(venue_id):
  try:
    db.session.query(Venue).filter(Venue.id==venue_id).delete()
    db.session.commit()
    flash('Venue ' + venue_id + ' was successfully deleted!')
  except Exception as e:
    db.session.rollback()
    db.session.flush() # for resetting non-commited .add()
    flash('An error occurred. Venue ' +  venue_id + ' could not be deleted.', 'error')
  finally:
    return redirect(url_for('index'))

#  Artists
#  ----------------------------------------------------------------
@app.route('/artists')
def artists():
  data = Artist.query.with_entities(Artist.id, Artist.name).all()
  return render_template('pages/artists.html', artists=data)

@app.route('/artists/search', methods=['POST'])
# Disable CSRF for this route.
@csrf.exempt
def search_artists():
  search_for = request.form.get('search_term', '')
  # seach for "A" should return "Guns N Petals", "Matt Quevado", and "The Wild Sax Band".
  # search for "band" should return "The Wild Sax Band".
  artists = Artist.query.filter(Artist.name.ilike('%' + search_for + '%')).all()
  response = {
    "count": len(list(artists)),
    "data": list(artists)
  }
  return render_template('pages/search_artists.html', results=response, search_term=search_for)

@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
  artist = Artist.query.get(artist_id).__dict__
  shows = Show.query.with_entities(Show.venue_id, Show.start_time, Venue.name.label('venue_name'), Venue.image_link.label('venue_image_link'))\
    .filter(Show.artist_id==artist_id)\
    .join(Venue, Venue.id==Show.venue_id, isouter=True)\
    .join(Artist, Artist.id==Show.artist_id, isouter=True)\
    .all()
  artist['upcoming_shows'] = list(filter(lambda show: show.start_time < datetime.now(), shows))
  artist['past_shows'] = list(filter(lambda show: show.start_time >= datetime.now(), shows))
  artist['upcoming_shows_count'] = len(artist['upcoming_shows'])
  artist['past_shows_count'] = len(artist['past_shows'])
  return render_template('pages/show_artist.html', artist=artist)

#  Update
#  ----------------------------------------------------------------
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
  artist = Artist.query.get(artist_id)
  form = ArtistForm(obj=artist)
  return render_template('forms/edit_artist.html', form=form, artist=artist)

@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
  form = ArtistForm(request.form)
  if form.validate_on_submit():
    artist = Artist.query.get(artist_id)
    form.populate_obj(artist)
    db.session.commit()
    # on successful db insert, flash success
    flash('Artist ' + request.form['name'] + ' was successfully updated!')
    return redirect(url_for('show_artist', artist_id=artist_id))
  else:
    flash('An error occurred. Artist ' +  request.form['name'] + ' could not be updated.', 'error')
    return redirect(url_for('edit_artist', artist_id=artist_id))

@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
  venue = Venue.query.get(venue_id)
  form = VenueForm(obj=venue)
  return render_template('forms/edit_venue.html', form=form, venue=venue)

@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
  form = VenueForm(request.form)
  if form.validate_on_submit():
    venue = Venue.query.get(venue_id)
    form.populate_obj(venue)
    db.session.commit()
    # on successful db insert, flash success
    flash('Venue ' + request.form['name'] + ' was successfully updated!')
    return redirect(url_for('show_venue', venue_id=venue_id))
  else:
    flash('An error occurred. Venue ' +  request.form['name'] + ' could not be updated.', 'error')
    return redirect(url_for('edit_venue', venue_id=venue_id))

#  Create Artist
#  ----------------------------------------------------------------

@app.route('/artists/create', methods=['GET'])
def create_artist_form():
  form = ArtistForm()
  return render_template('forms/new_artist.html', form=form)

@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
  form = ArtistForm(request.form)
  if form.validate_on_submit():
    artist = Artist()
    form.populate_obj(artist)
    db.session.add(artist)
    db.session.commit()
    # on successful db insert, flash success
    flash('Artist ' + request.form['name'] + ' was successfully listed!')
    return redirect(url_for('index'))
  else:
    flash('An error occurred. artist ' +  request.form['name'] + ' could not be listed.', 'error')
    return render_template('forms/new_artist.html', form=form)


#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():
  # displays list of shows at /shows
  data = Show.query.with_entities(Show.artist_id, Show.venue_id, Show.start_time, Artist.name.label('artist_name'), Artist.image_link.label('artist_image_link'), Venue.name.label('venue_name'))\
    .join(Venue, Venue.id==Show.venue_id, isouter=True)\
    .join(Artist, Artist.id==Show.artist_id, isouter=True)\
    .all()
  return render_template('pages/shows.html', shows=data)

@app.route('/shows/create')
def create_shows():
  # renders form. do not touch.
  form = ShowForm()
  return render_template('forms/new_show.html', form=form)

@app.route('/shows/create', methods=['POST'])
def create_show_submission():
  # called to create new shows in the db, upon submitting new show listing form
  form = ShowForm(request.form)
  if form.validate_on_submit():
    show = Show()
    form.populate_obj(show)
    db.session.add(show)
    db.session.commit()
    # on successful db insert, flash success
    flash('Show was successfully listed!')
    return redirect(url_for('index'))
  else:
    flash('An error occurred. Show could not be listed.', 'error')
    return render_template('forms/new_show.html', form=form)

@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def server_error(error):
    return render_template('errors/500.html'), 500


if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#

# Default port:
if __name__ == '__main__':
    app.run()

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''
