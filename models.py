import datetime
from peewee import *
from bottle import ConfigDict
from typing import Optional

# Load configuration
try:
    with open('imageboard.conf') as f:
        pass
except FileNotFoundError:
    print("Config file not found.")
    exit()

config = ConfigDict()
config.load_config('imageboard.conf')

# Database initialization
if config['database.engine'] == 'sqlite':
    db = SqliteDatabase(f'{config["database.name"]}.db')
elif config['database.engine'] == 'postgresql':
    db = PostgresqlDatabase(
        config['database.name'],
        user=config['database.username'],
        password=config['database.password'],
        host=config['database.host'],
        port=int(config['database.port'])
    )
elif config['database.engine'] == 'mysql':
    db = MySQLDatabase(
        config['database.name'],
        user=config['database.username'],
        password=config['database.password'],
        host=config['database.host'],
        port=int(config['database.port'])
    )


# Models
class BaseModel(Model):
    class Meta:
        database = db


class Anon(BaseModel):
    ip = IPField()
    banned = BooleanField(default=False)
    mod = CharField(default="")
    can_capcode = BooleanField(default=False)
    capcode = CharField(default='')
    ban_reason = CharField(null=True)
    ban_date = DateTimeField(null=True)


class Board(BaseModel):
    name = CharField()
    title = CharField()
    nsfw = BooleanField(default=False)
    lastrefnum = IntegerField(default=1)


class Post(BaseModel):
    board = ForeignKeyField(Board, backref='posts')
    author = ForeignKeyField(Anon, backref='posts')
    is_archived = BooleanField(default=False)
    author_name = CharField()
    refnum = IntegerField()
    replyrefnum = IntegerField(null=True)
    date = DateTimeField(default=datetime.datetime.now)
    bumped_at = DateTimeField(null=True, default=datetime.datetime.now)
    filename = CharField()
    image = CharField()
    email = TextField(null=True)
    title = CharField(null=True)
    content = TextField()
    short_content = TextField()
    is_reply = BooleanField(default=False)
    closed = BooleanField(default=False)
    pinned = BooleanField(default=False)
    replylist = CharField(default="[]")
    capcode = CharField(default='')
    trip = CharField(null=True)
    sec_trip = CharField(null=True)


class Report(BaseModel):
    reason = CharField()
    refnum = IntegerField()
    date = DateTimeField()
    board = ForeignKeyField(Board, backref='reports')


class Captcha(BaseModel):
    text = CharField()
    time_exp = DateTimeField()


class FavoritePost(BaseModel):
    anon = ForeignKeyField(Anon, backref='favorites', on_delete='CASCADE')
    post = ForeignKeyField(Post, backref='favorited_by', on_delete='CASCADE')

    class Meta:
        indexes = (
            (('anon', 'post'), True),  # Unique anon + post
        )


class Banner(BaseModel):
    board = ForeignKeyField(Board, backref='banners', on_delete='CASCADE')
    file = CharField()
    file_name = CharField()
    archived = BooleanField(default=False)


class News(BaseModel):
    name = CharField(null=True)
    time = DateTimeField(default=datetime.datetime.now)
    subject = CharField(null=True)
    body = TextField(null=True)


class ModLogs(BaseModel):
    ip = IPField()
    board = CharField(null=True)
    time = DateTimeField(default=datetime.datetime.now)
    text = TextField()


class PrivateMessage(BaseModel):
    sender = IntegerField()
    to = IntegerField()
    message = CharField()
    time = DateTimeField(default=datetime.datetime.now)
    unread = BooleanField(default=True)


# Create tables
with db:
    db.create_tables([Report, Post, Board, Anon, Captcha, FavoritePost, Banner, News, ModLogs, PrivateMessage])
