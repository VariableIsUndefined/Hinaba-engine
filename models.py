import datetime
from peewee import *
from bottle import ConfigDict

try:
    with open('imageboard.conf') as f:
        pass
except FileNotFoundError:
    print("Config file not found.")
    exit()

config = ConfigDict()
config.load_config('imageboard.conf')

if config['database.engine'] == 'sqlite':

    db = SqliteDatabase(f'{config["database.name"]}.db')
    
elif config['database.engine'] == 'postgresql':

    db = PostgresqlDatabase(
        config['database.name'],
        user     = config['database.username'],
        password = config['database.password'],
        host     = config['database.host'],
        port     = int(config['database.port'])
    )

elif config['database.engine'] == 'mysql':

    db = MySQLDatabase(
        config['database.name'],
        user     = config['database.username'],
        password = config['database.password'],
        host     = config['database.host'],
        port     = int(config['database.port'])
    )

class Anon(Model):
    #name = CharField()
    ip = IPField()
    banned = BooleanField(default=False)
    mod = CharField(default="")
    can_capcode = BooleanField(default=False)
    capcode = CharField(default='')
    ban_reason = CharField(null=True)
    ban_date = DateTimeField(null=True)

    class Meta:
        database = db

class Board(Model):
    name = CharField()
    title = CharField()
    category = CharField(null=False)
    nsfw = BooleanField(default=False)
    lastrefnum = IntegerField(default=1)

    class Meta:
        database = db

class Post(Model):
    board = ForeignKeyField(Board, backref='posts')
    author = ForeignKeyField(Anon, backref='posts')
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
    # Add tripcodes
    trip = CharField(null=True)
    sec_trip = CharField(null=True)

    class Meta:
        database = db

class Report(Model):
    reason = CharField()
    refnum = IntegerField()
    date = DateTimeField()
    board = ForeignKeyField(Board, backref='reports')

    class Meta:
        database = db

class Captcha(Model):
    text = CharField()
    time_exp = DateTimeField()

    class Meta:
        database = db

class Category(Model):
    name = CharField(null=False)
    
    class Meta:
        database = db
        
class FavoritePost(Model):
    anon = ForeignKeyField(Anon, backref='favorites', on_delete='CASCADE')
    post = ForeignKeyField(Post, backref='favorited_by', on_delete='CASCADE')
    
    class Meta:
        database = db
        
        indexes = (
            (('anon', 'post'), True),  # Unique anon + post
        )
        
class Banner(Model):
    board = ForeignKeyField(Board, backref='banners', on_delete='CASCADE')
    file = CharField()
    file_name = CharField()
    archived = BooleanField(default=False)
    
    class Meta:
        database = db

with db:
    db.create_tables([Report, Post, Board, Anon, Captcha, Category, FavoritePost, Banner])
