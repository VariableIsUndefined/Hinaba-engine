#!/bin/env python
from bottle import (run, static_file, request, view, redirect,
        abort, get, post, ConfigDict, response, default_app, error, template, route)
from utils import file_validation, remove_media, board_directory, get_directory_size, generate_trip, dice
from json import loads, dumps
from os import path, mkdir, makedirs
from string import punctuation
from waitress import serve
from models import db, Post, Anon, Board, Report, Captcha, Category, FavoritePost, Banner
from datetime import datetime,timedelta,UTC
from captcha.image import ImageCaptcha
from random import randint, choice
from peewee import IntegrityError
from uuid import uuid4

config = ConfigDict()
config.load_config('imageboard.conf')

basename = config['app.basename']

if basename[-1] == '/': basename = basename[:-1] # remove trailing slash

STYLES = config["style.styles"]

@get('/static/<filename:path>')
def send_static(filename):
    return static_file(filename, root='static')

@get('/uploads/<filename:path>')
def send_upload(filename):
    return static_file(filename, root='uploads')

@get('/banners/<board_name>/<file_name>')
def serve_banner(board_name, file_name):
    return static_file(file_name, root=path.join("banners", board_name))

def get_current_user(req):
    ip = req.get('HTTP_X_FORWARDED_FOR')
    
    if ip is None: ip = req.get('REMOTE_ADDR')

    try:
        current_user = Anon.get(Anon.ip == ip)
    except:
        anon = Anon(ip = ip)
        anon.save()

        current_user = anon

    return current_user

def check_admin(req):
    logged_cookie = req.get_cookie("logged")
    if bool(logged_cookie):
        if logged_cookie != config['admin.token']: return 1
    else: return 1

@get('/')
@view('home')
def home():
    show_nsfw = ('True' == config['threads.show_nsfw'])
    active_content_size = get_directory_size('uploads')
    number_of_messages = Post.select().count()
    return dict(title=config['app.title'],
            welcome_message=config['app.welcome_message'],
            show_nsfw=show_nsfw, active_content_size=active_content_size,
            number_of_messages=number_of_messages, basename=basename)

@get('/captcha')
def generate_captcha():

    text = randint(10000,99999)
    time_exp = datetime.now() + timedelta(minutes=5)

    captcha = Captcha(text = text, time_exp = time_exp)
    captcha.save()

    challenge = {
        'id': captcha.id,
        'text': text,
        'time_exp': str(time_exp)
    }

    return dumps(challenge)

@get('/captchaimg/<cha:int>')
def captcha_image(cha):
    image = ImageCaptcha()
    code = Captcha.get_by_id(cha).text
    data = image.generate(code)
    response.content_type = "image/png"
    return data

@get('/<board_name>/')
@get('/<board_name:re:[a-z0-9]+>')
@get('/<board_name>/<page:int>')
@view('board')
def get_board(board_name, page=1):

    try:
        board = Board.get(Board.name == board_name)
    except:
        abort(404, "This page doesn't exist.")

    current_user = get_current_user(request)

    per_page = int(config['threads.per_page'])

    query = board.posts.where(Post.is_reply == False).order_by(Post.pinned.desc(), Post.bumped_at.desc())

    threads = query.paginate(page, per_page)
    
    banners = Banner.select().where((Banner.board == board) & (Banner.archived == False))
    banner = choice(banners) if banners.exists() else None
    
    current_style = request.get_cookie('style', default='Yotsuba')
    if current_style not in STYLES:
        current_style = 'Yotsuba'
                
    return dict(
            board_name=board.name, board_title=board.title,
            threads=threads, board=board, current_page=page,
            is_detail = False, current_user = current_user,
            thread_count=query.count(),
            max_file_size=config['uploads.upload_max_size'],
            maxlength=config['threads.content_max_length'],
            per_page=per_page, basename=basename,
            banner=banner.file if banner else None,
            style=current_style,
            host='://'.join(request.urlparts[:2])
        )

@get('/ban_info')
@view('ban')
def ban_info():

    current_user = get_current_user(request)

    return dict(current_user=current_user, basename=basename)

@get('/<board_name>/thread/<refnum:int>')
@view('detail')
def get_thread(board_name, refnum):

    try:
        board = Board.get(Board.name == board_name)
    except:
        return abort(404, "This page doesn't exist.")

    try:
        thread = board.posts.where(Post.refnum == refnum).get()
    except:
        abort(404, "This page doesn't exist.")
        
    banners = Banner.select().where((Banner.board == board) & (Banner.archived == False))
    banner = choice(banners) if banners.exists() else None
    
    current_style = request.get_cookie('style', default='Yotsuba')
    if current_style not in STYLES:
        current_style = 'Yotsuba'

    return dict(board_name=board.name, thread=thread, board=board,
            is_detail=True, current_user=get_current_user(request),
            max_file_size=config['uploads.upload_max_size'],
            maxlength=config['threads.content_max_length'], basename=basename,
            banner=banner.file if banner else None,
            style=current_style,
            host='://'.join(request.urlparts[:2])
    )

@get('/<board_name>/catalog')
@view('catalog')
def catalog(board_name):

    try:
        board = Board.get(Board.name == board_name)
    except:
        return abort(404, "This page doesn't exist.")
    
    banners = Banner.select().where((Banner.board == board) & (Banner.archived == False))
    banner = choice(banners) if banners.exists() else None

    query = board.posts.where(Post.is_reply == False).order_by(Post.pinned.desc(), Post.bumped_at.desc())
    
    # The query search
    
    if request.query and request.query['search']:
        search = request.query['search']
        
        query = board.posts.where(Post.is_reply == False, (
        (Post.title.contains(search)) | (Post.content.contains(search))
    )).order_by(Post.pinned.desc(), Post.bumped_at.desc())
        
    current_style = request.get_cookie('style', default='Yotsuba')
    if current_style not in STYLES:
        current_style = 'Yotsuba'

    return dict(threads=query, board_name=board.name,
            board_title=board.title, board=board,
            current_user=get_current_user(request),
            banner=banner.file if banner else None,
            style=current_style, basename=basename)

@get('/<board_name>/mod')
@view('reports')
def reports(board_name):

    try:
        board = Board.get(Board.name == board_name)
    except:
        return abort(404, "This page doesn't exist.")

    current_user = get_current_user(request)
    
    if f':{board_name}:' not in current_user.mod:
        return redirect(f'{basename}/{board_name}/')

    report_reasons = loads(config['reports.reasons'])
    banners = Banner.select().where(Banner.board == board)

    return dict(board=board, bans=Anon.select().where(Anon.banned == True),
            current_user=current_user, board_name=board_name,
            reasons=report_reasons, reports=board.reports, basename=basename,
            banners=banners)

@get('/admin')
@view('admin')
def admin_panel():

    current_user = get_current_user(request)

    logged_cookie = request.get_cookie("logged")

    if bool(logged_cookie):

        if logged_cookie != config['admin.token']: return redirect(f'{basename}/')

    else: return redirect(f'{basename}/')

    return dict(boards=Board.select(), current_user=current_user,
            board_name=None, mods=Anon.select().where(Anon.mod != ""),
            categories=Category.select(),
            basename=basename)

@get('/login')
@view('login')
def login():

    current_user = get_current_user(request)

    return dict(current_user=current_user, basename=basename)


@post('/login')
def do_login():

    password = request.forms.get("password")

    if password == config['admin.password']:

        response.set_cookie("logged", config['admin.token'])

        return redirect(f'{basename}/admin')

    return redirect(f'{basename}/login')

@post('/logout')
def do_logout():

    response.delete_cookie('logged')

    return redirect(f'{basename}/')

@post('/<board_name>/')
def post_thread(board_name):

    captchares = request.forms.get('captchares')
    captchaid = request.forms.get('captchaid')

    challenge = Captcha.get_by_id(captchaid)

    if (challenge.text != captchares or
    challenge.time_exp <= datetime.now()): return abort(403, "Invalid Captcha.")

    current_user = get_current_user(request)
    if get_current_user(request).banned: return redirect(f'{basename}/ban_info')

    board = Board.get(Board.name == board_name)

    title = request.forms.get('title')
    content = request.forms.get('content')
    email = request.forms.get('email')
    capcode = request.forms.get("capcode")

    upload = request.files.get('upload')
    author_name = request.forms.get('author')
    
    if not author_name: author_name = "Anonymous"

    if not all([content, upload]): return abort(400, "Incomplete post.")

    if len(content) > int(config['threads.content_max_length']):
            return abort(400, "The content exeeds the maximum length.")
        
    trip_info = generate_trip(author_name)
    author_name, trip, sec_trip = trip_info["author_name"], trip_info["trip"], trip_info["sec_trip"]
        
    author = current_user
    refnum = board.lastrefnum
    save_path = file_validation(board_name, refnum, upload)

    if len(content.split('\n')) < 10:
        short_content = ' '.join(content.split(' ')[:200])
    else:
        if any((len(item) > 200 for item in content.split(' '))):
            short_content = ' '.join(content.split(' ')[:200])
        else:
            short_content = '\n'.join(content.split('\n')[:10])

    if save_path == 1: return redirect(f'{basename}/{board_name}/')
    
    got_dice = dice(email)
    if got_dice:
        content = f"{got_dice}\n" + content
        short_content = f"{got_dice}\n" + short_content


    data = {
        "board": board,
        "author": author,
        "author_name": author_name,
        "refnum": refnum,
        "filename": upload.filename,
        "image": save_path,
        "title": title,
        "content": content,
        "short_content": short_content,
        "date": datetime.now(UTC).strftime("%m/%d/%y (%a) %H:%M:%S"),
        "trip": trip if trip != '' else None,
        "sec_trip": sec_trip if sec_trip != '' else None,
        "email": email if email else None,
        "capcode": current_user.capcode if capcode == "on" else ''
    }

    thread = Post(**data)
    thread.save()

    board.lastrefnum += 1
    board.save()

    max_active_threads = int(config['threads.max_active'])

    query = board.posts.where(Post.is_reply == False).order_by(
            Post.pinned.desc(), Post.bumped_at.desc())

    if query.count() >= max_active_threads:

        threads_to_delete = query.offset(max_active_threads)

        for thread in threads_to_delete:

            remove_textual_refs(board, thread)
            thread.delete_instance()
            remove_media(thread.image)

            for reply in board.posts.where(Post.replyrefnum == thread.refnum):

                    reply.delete_instance()
                    remove_media(reply.image)

    redirect(f'{basename}/{board_name}/')

@post('/<board_name>/thread/<refnum:int>')
def post_reply(board_name, refnum):

    current_user = get_current_user(request)
    if get_current_user(request).banned: return redirect(f'{basename}/ban_info')

    board = Board.get(Board.name == board_name)
    thread = board.posts.where(Post.refnum == refnum).get()

    if thread.closed:
        return abort(423, "You cannot reply because this thread is locked.")

    content = request.forms.get('content')
    author_name = request.forms.get('author')
    email = request.forms.get('email')
    capcode = request.forms.get("capcode")
    
    if not author_name: author_name = "Anonymous"

    if not bool(content): return redirect(f'{basename}/{board_name}/')

    if len(content) > int(config['threads.content_max_length']):
            return abort(400, "The content exeeds the maximum length.")

    if len(content.split('\n')) < 10:
        short_content = ' '.join(content.split(' ')[:200])
    else:
        if any((len(item) > 200 for item in content.split(' '))):
            short_content = ' '.join(content.split(' ')[:200])
        else:
            short_content = '\n'.join(content.split('\n')[:10])
    
    got_dice = dice(email)
    if got_dice:
        content = f"{got_dice}\n" + content
        short_content = f"{got_dice}\n" + short_content

    upload = request.files.get('upload')
        
    trip_info = generate_trip(author_name)
    author_name, trip, sec_trip =  trip_info["author_name"], trip_info["trip"], trip_info["sec_trip"]

    author = current_user
    no = board.lastrefnum

    filename = ""
    save_path = ""
    
    if upload is not None:
        if upload.content_type.startswith('image') or upload.content_type.startswith('video'):

            save_path = file_validation(board_name, no, upload, is_reply=True)
            if save_path == 1: return redirect(f'{basename}/{board_name}/thread/{refnum}')
            filename = upload.filename
    
    data = {
        "board": board,
        "author": author,
        "author_name": author_name,
        "refnum": no,
        "is_reply": True,
        "replyrefnum": refnum,
        "filename": filename,
        "image": save_path,
        "content": content,
        "short_content": short_content,
        "date": datetime.now(UTC).strftime("%m/%d/%y (%a) %H:%M:%S"),
        "trip": trip if trip != '' else None,
        "sec_trip": sec_trip if sec_trip != '' else None,
        "email": email if email else None,
        "capcode": current_user.capcode if capcode == "on" else '',
    }

    reply = Post(**data)
    reply.save()

    for word in content.split():
        if word[:2] == ">>":
            ref = word[2:]
            if ref.rstrip().isdigit():
                ref = int(ref)
                try:
                    thread_ref = board.posts.where(Post.refnum == ref).get()
                    replylist = loads(thread_ref.replylist)
                    if no not in replylist:
                        replylist.append(no)
                        thread_ref.replylist = dumps(replylist)
                        thread_ref.save()
                except: pass

    #sage: if "email" field is a sage, then thread won't get bumped
    if email != "sage":
        thread.bumped_at = datetime.now().replace(microsecond=0)
        thread.save()

    board.lastrefnum += 1
    board.save()

    # noko: if you type it in email field, you wont get redirect back to board, you will stay in thread
    if email == 'noko':
        redirect(f'{basename}/{board_name}/thread/{refnum}')
    else:
        redirect(f'{basename}/{board_name}/')

def remove_textual_refs(board, thread):
    for word in thread.content.split():
        if word[:2] == ">>":
            ref = word[2:]
            if ref.rstrip().isdigit():
                thread_ref = board.posts.where(Post.refnum == ref).get_or_none()
                if thread_ref is None: continue
                replylist = loads(thread_ref.replylist)
                if thread.refnum in replylist:
                    replylist.remove(thread.refnum)
                    thread_ref.replylist = dumps(replylist)
                    thread_ref.save()

@post('/<board_name>/delete')
def delete_post(board_name):

    current_user = get_current_user(request)

    board = Board.get(Board.name == board_name)
    form = dict(request.forms)
    
    if bool(form.get('report')):
        reason = form.get('report')
        report_reasons = loads(config['reports.reasons'])
        if reason not in report_reasons: return redirect(f'{basename}/{board_name}/')
        for refnum in list(form)[:-1]:
            report = Report(reason=reason, refnum=refnum, board=board, date=datetime.now().replace(microsecond=0))
            report.save()
    else:
        for refnum in form:
            thread = board.posts.where(Post.refnum == refnum).get()
            if (thread.author == current_user or
                f':{board_name}:' in current_user.mod):

                remove_textual_refs(board, thread)
                
                if thread.image: remove_media(thread.image)

                if not thread.is_reply:

                    for reply in board.posts.where(Post.replyrefnum == thread.refnum):

                        if reply.image: remove_media(reply.image)
                        reply.delete_instance()

                thread.delete_instance()
                Report.delete().where(refnum == thread.refnum).execute()

    redirect(f'{basename}/{board_name}/')

@post('/<board_name>/ban')
def ban(board_name):

    if f':{board_name}:' not in get_current_user(request).mod:
        return abort(403, "You are not allowed to do this.")

    form = dict(request.forms)

    reason = form.get('reason')

    user = form.get('user').strip()

    Anon.update(banned=True, ban_reason=reason, ban_date=datetime.now().replace(microsecond=0)).where(Anon.name == user).execute()

    return redirect(f'{basename}/{board_name}/mod')

@post('/<board_name>/unban/<name>')
def unban(board_name, name):

    if f':{board_name}:' not in get_current_user(request).mod:
        return abort(403, "You are not allowed to do this.")

    form = dict(request.forms)

    anon = Anon.get(Anon.name == name)

    if bool(form.get("dall")):
        Post.delete().where(Post.author_id == anon.id).execute()

    if bool(form.get("unban")):
        Anon.update(banned=False, ban_reason=None, ban_date=None).where(Anon.name == name).execute()

    return redirect(f'{basename}/{board_name}/mod')

@post('/add_board')
def add_board():

    if check_admin(request) == 1:
        return abort(403, "You are not allowed to do this.")

    name = request.forms.get("name").strip().lower()
    category = request.forms.get("category")

    if any( char in list(punctuation + ' ') for char in name ):
        return abort(400, "Boards can't have symbols in their name.")

    if Board.select().where(Board.name == name).exists():
        return abort(400, "A board with this name already exists.")

    if not category:
        return abort(400, "Please select a category.")
    
    data = {
        "name": name,
        "nsfw": bool(request.forms.get("nsfw")),
        "title": request.forms.get("title").strip(),
        "category": category,
    }

    board = Board(**data)
    board.save()
    board_directory(name)

    return redirect(f'{basename}/admin')

@post('/del_board/<board_name>')
def del_board(board_name):

    if check_admin(request) == 1:
        return abort(403, "You are not allowed to do this.")

    for anon in Anon.select().where(Anon.mod != ""):
        anon.mod = anon.mod.replace(f':{board_name}:', '')
        anon.save()

    board = Board.get(Board.name == board_name)

    Post.delete().where(Post.board_id == board.id).execute()

    board.delete_instance()
    board_directory(board_name, remove=True)

    return redirect(f'{basename}/admin')

@post('/mod')
def mod():

    if check_admin(request) == 1:
        return abort(403, "You are not allowed to do this.")

    ip = request.forms.get("ip").strip()
    board = request.forms.get("board")
    opts = request.forms

    anon = Anon.get(Anon.ip == ip)

    if bool(opts.get("add")) and f':{board}:' not in anon.mod:
        anon.mod += f':{board}:'

    if bool(opts.get("rm")): anon.mod = anon.mod.replace(f':{board}:', '')

    if bool(opts.get("rmall")): anon.mod = ""

    anon.save()

    return redirect(f'{basename}/admin')

@post('/new_mod')
def add_mod():

    if check_admin(request) == 1:
        return abort(403, "You are not allowed to do this.")

    ip = request.forms.get("ip")
    board = request.forms.get("board")
    can_capcode = request.forms.get("can_capcode")
    capcode = request.forms.get("capcode")
        
    try:
        anon = Anon.get(Anon.ip == ip)
    except:
        return abort(404, "User does not exist.")

    if f':{board}:' not in anon.mod: anon.mod += ":"+board+":"
    anon.can_capcode = can_capcode
    anon.capcode = capcode
    
    anon.save()

    return redirect(f'{basename}/admin')

@get('/<board_name>/thread/<refnum:int>/pin')
def thread_pin(board_name, refnum):

    if f':{board_name}:' not in get_current_user(request).mod:
        return abort(404, "This page doesn't exist.")

    board = Board.get(Board.name == board_name)

    thread = board.posts.where(Post.refnum == refnum).get()

    if thread.pinned: thread.pinned = False
    else: thread.pinned = True

    thread.save()

    return redirect(f'{basename}/{board_name}/')

@get('/<board_name>/thread/<refnum:int>/close')
def thread_close(board_name, refnum):

    if f':{board_name}:' not in get_current_user(request).mod:
        return abort(404, "This page doesn't exist.")

    board = Board.get(Board.name == board_name)

    thread = board.posts.where(Post.refnum == refnum).get()

    if thread.closed: thread.closed = False
    else: thread.closed = True

    thread.save()

    return redirect(f'{basename}/{board_name}/')

@post('/add_category')
def add_category():

    if check_admin(request) == 1:
        return abort(403, "You are not allowed to do this.")

    name = request.forms.get("name").strip()

    if Board.select().where(Board.name == name).exists():
        return abort(400, "A category with this name already exists.")

    data = {
        "name": name,
    }

    category = Category(**data)
    category.save()

    return redirect(f'{basename}/admin')

@post('/del_category/<category_name>')
def del_category(category_name):

    if check_admin(request) == 1:
        return abort(403, "You are not allowed to do this.")

    category = Category.get(Category.name == category_name)

    Board.update(category='').where(Board.category == category).execute()

    category.delete_instance()

    return redirect(f'{basename}/admin')

@error(404)
def error404(error):
    return template("error.tpl", basename=basename)

@get('/rules')
@view('rules')
def rules():
    return dict(rules=config['app.rules'], basename=basename)

@get('/faq')
@view('faq')
def rules():
    return dict(faq=config['app.faq'], basename=basename)

# -- Favorite posts -- #

@get('/<board_name>/favorite/<refnum:int>')
def add_to_favorites(board_name, refnum):
    anon = get_current_user(request)
    thread = Post.select().where(Post.refnum == refnum, Post.is_reply == False).get()
    
    try:
        data = {
            "anon": anon,
            "post": thread,
        }
        
        favorite_post = FavoritePost(**data)
        favorite_post.save()
    except Post.DoesNotExist:
        response.status = 404
    except IntegrityError:
        response.status = 409
    
    return redirect(f'{basename}/{board_name}/')

@get('/<board_name>/unfavorite/<refnum:int>')
def remove_from_favorites(board_name, refnum):
    anon = get_current_user(request)
    thread = Post.select().where(Post.refnum == refnum, Post.is_reply == False).get()
    
    query = FavoritePost.delete().where(
        (FavoritePost.anon == anon) & (FavoritePost.post == thread)
    )
    
    if query.execute() == 0:
        response.status = 404
    
    return redirect(f'{basename}/{board_name}/')

@get('/favorites')
def get_favorites():
    anon = get_current_user(request)
    if not anon:
        response.status = 403
        return {"error": "Unauthorized"}

    favorites = (FavoritePost
                .select(FavoritePost, Post)
                .join(Post)
                .where(FavoritePost.anon == anon))
    
    return {"favorites": [{"id": fav.post.id, "title": fav.post.title, "board_name": fav.post.board.name, "board_id": fav.post.board.id} for fav in favorites]}

# -- Banners -- #

@post('/<board_name>/upload_banner')
def upload_banner(board_name):
    if f':{board_name}:' not in get_current_user(request).mod:
        return abort(403, "You are not allowed to do this.")
    
    upload = request.files.get('upload')
    print(upload)
    if not upload:
         return abort(400, "Please upload banner file!")
     
    file_ext = path.splitext(upload.filename)[1].lower()
    if file_ext not in ['.jpg', '.jpeg', '.png', '.gif']:
        return abort(400, "Unacceptable file extension. Please use: .jpg, .jpeg, .png, .gif")
    
    try:
        board = Board.get(Board.name == board_name)
    except:
        return abort(400, "The board does not exist.")
    
    board_folder = path.join("banners", board_name)
    makedirs(board_folder, exist_ok=True)

    unique_name = f"{uuid4().hex}{file_ext}"
    file_path = path.join(board_folder, unique_name)
    upload.save(file_path)

    Banner.create(board=board, file=file_path, file_name=upload.filename)
    
    return redirect(f"{basename}/{board_name}/mod")

@post('/<board_name>/del_banner/<banner_id>')
def del_banner(board_name, banner_id):

    if f':{board_name}:' not in get_current_user(request).mod:
        return abort(403, "You are not allowed to do this.")
    
    try:
        board = Board.get(Board.name == board_name)
    except:
        return abort(400, "The board does not exist.")

    banner = Banner.get((Banner.board == board) & (Banner.id == banner_id))
    banner.delete_instance()

    return redirect(f"{basename}/{board_name}/mod")

@post('/<board_name>/unarch_banner/<banner_id>')
def unarchive_banner(board_name, banner_id):
    if f':{board_name}:' not in get_current_user(request).mod:
        return abort(403, "You are not allowed to do this.")
    
    try:
        board = Board.get(Board.name == board_name)
    except:
        return abort(400, "The board does not exist.")

    try:
        banner = Banner.get((Banner.board == board) & (Banner.id == banner_id))
    except:
        return abort(400, "The banner does not exist.")
    
    Banner.update(archived = False).where(Banner.id == banner_id).execute()
    
    return redirect(f"{basename}/{board_name}/mod")

@post('/<board_name>/arch_banner/<banner_id>')
def archive_banner(board_name, banner_id):
    if f':{board_name}:' not in get_current_user(request).mod:
        return abort(403, "You are not allowed to do this.")
    
    try:
        board = Board.get(Board.name == board_name)
    except:
        return abort(400, "The board does not exist.")

    try:
        banner = Banner.get((Banner.board == board) & (Banner.id == banner_id))
    except:
        return abort(400, "The banner does not exist.")
    
    Banner.update(archived = True).where(Banner.id == banner_id).execute()
    
    return redirect(f"{basename}/{board_name}/mod")

# -- Styles -- #

@route('/set_style/<style_name>')
def set_style(style_name):
    if style_name in STYLES:
        response.set_cookie('style', style_name, path="/", max_age=3600)
        
    return ''

if __name__ == '__main__':

    db.connect()

    if not path.isdir('uploads'): mkdir('uploads')
    if not path.isdir('banners'): mkdir('banners')
    
    url_prefix = basename

    def fix_environ_middleware(app):
      def fixed_app(environ, start_response):
        path = environ['PATH_INFO']
        if path.startswith("/"):
            # strip extra slashes at the beginning of a path that starts
            # with any number of slashes
            path = "/" + path.lstrip("/")

        if url_prefix:
            # NB: url_prefix is guaranteed by the configuration machinery to
            # be either the empty string or a string that starts with a single
            # slash and ends without any slashes
            if path == url_prefix:
                # if the path is the same as the url prefix, the SCRIPT_NAME
                # should be the url_prefix and PATH_INFO should be empty
                path = ""
            else:
                # if the path starts with the url prefix plus a slash,
                # the SCRIPT_NAME should be the url_prefix and PATH_INFO should
                # the value of path from the slash until its end
                url_prefix_with_trailing_slash = url_prefix + "/"
                if path.startswith(url_prefix_with_trailing_slash):
                    path = path[len(url_prefix) :]
        environ['SCIPT_NAME'] = url_prefix
        environ['PATH_INFO'] = path
        return app(environ, start_response)
      return fixed_app

    app = default_app()
    app.wsgi = fix_environ_middleware(app.wsgi)

    production = bool(int(config['app.production']))

    run(
        debug    = not production,
        reloader = not production,
        host     = config['app.host'],
        port     = config['app.port']
    )