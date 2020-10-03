from sqlalchemy import Column, Integer, String, Boolean, Text, ARRAY, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from flask_sqlalchemy import SQLAlchemy
from flask import Flask


app = Flask(__name__)

#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app.config.from_object('config')

# connect to a local postgresql database
db = SQLAlchemy(app)

#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#

class Venue(db.Model):
    __tablename__ = 'Venue'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    city = Column(String(120))
    state = Column(String(120))
    address = Column(String(120))
    phone = Column(String(120))
    website = Column(String(120))
    image_link = Column(String(500))
    facebook_link = Column(String(120))
    seeking_talent = Column(Boolean)
    seeking_description = Column(Text)
    genres = Column(ARRAY(String(120), dimensions=1)) # genres separated by comma, items imploded
    shows = relationship("Show", backref='venue', lazy=True)

    # for debug
    def __repr__(self):
        return 'Venue: {}-{}-{}-{}'.format(self.id, self.name, self.city, self.sate)

class Artist(db.Model):
    __tablename__ = 'Artist'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    city = Column(String(120))
    state = Column(String(120))
    phone = Column(String(120))
    genres = Column(ARRAY(String(120), dimensions=1)) # genres separated by comma, items imploded
    image_link = Column(String(500))
    facebook_link = Column(String(120))
    website = Column(String(120))
    seeking_venue = Column(Boolean)
    seeking_description = Column(Text)
    shows = relationship("Show", backref='artist', lazy=True)

    # for debug
    def __repr__(self):
        return 'Artist: {}-{}-{}-{}'.format(self.id, self.name, self.city, self.sate)

class Show(db.Model):
    __tablename__ = 'Show'

    id = Column(Integer, primary_key=True)
    artist_id = Column(Integer, ForeignKey('Artist.id'), nullable=False)
    venue_id = Column(Integer, ForeignKey('Venue.id'), nullable=False)
    start_time = Column(DateTime)

    # for debug
    def __repr__(self):
        return 'Show: artist_id: {}- venue_id: {}- start_time: {}'.format(self.artist_id, self.venue_id, self.start_time)
