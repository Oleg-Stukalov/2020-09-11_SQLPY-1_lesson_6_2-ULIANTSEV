import sqlalchemy as sq
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

Base = declarative_base()

engine = sq.create_engine('postgresql+psycopg2://netology:netology@localhost:5432/media')
Session = sessionmaker(bind=engine)


class Artist(Base):
    __tablename__ = 'artist'

    id = sq.Column(sq.Integer, primary_key=True)
    name = sq.Column(sq.String)
    albums = relationship('Album', back_populates='artist')


class Album(Base):
    __tablename__ = 'album'

    id = sq.Column(sq.Integer, primary_key=True)
    title = sq.Column(sq.String)
    tracks = relationship('Track', backref='album')
    published = sq.Column(sq.Date)

    id_artist = sq.Column(sq.Integer, sq.ForeignKey('artist.id'))
    artist = relationship(Artist)


class Genre(Base):
    __tablename__ = 'genre'

    id = sq.Column(sq.Integer, primary_key=True)
    title = sq.Column(sq.String)
    tracks = relationship('Track', secondary='track_to_genre', back_populates='genres')


track_to_genre = sq.Table(
    'track_to_genre', Base.metadata,
    sq.Column('genre_id', sq.Integer, sq.ForeignKey('genre.id')),
    sq.Column('track_id', sq.Integer, sq.ForeignKey('track.id')),
)


class Track(Base):
    __tablename__ = 'track'

    id = sq.Column(sq.Integer, primary_key=True)
    title = sq.Column(sq.String)
    duration = sq.Column(sq.Integer)
    genres = relationship(Genre, secondary=track_to_genre, back_populates='tracks')

    id_album = sq.Column(sq.Integer, sq.ForeignKey('album.id'))
    # album = relationship(Album)
    def get_info(self):
        return {'g': self.genres, 'duration': self.duration}

    def __repr__(self):
        return self.title


if __name__ == '__main__':
    # Base.metadata.create_all(engine)
    session = Session()
    tracks = session.query(Track).all()
    print(tracks)
    # print([t.title for t in tracks])

    # rock = Genre(title='rock')
    # folk = Genre(title='folk')
    # genres = [Genre(title=title) for title in ['bluse', 'hip-hop', 'metal']]
    # genres = [Genre(title=title) for title in ['bluse', 'hip-hop', 'metal']]
    # tr1 = session.query(Track).filter(Track.title == 'tr1').first()
    # tr1.genres.append(folk)

    # session.add_all(genres)
    # session.add(folk)
    # session.commit()

    # tracks =  [{'title': '',
    #             'genre': '', }]
    # for t in tracks:
    #     genre = Genre(title=t['genre'])
    #     track = Track(t['title'])
    #     track.genres.append(genre)
    #
    #     session.add_all([genre, tracks])
