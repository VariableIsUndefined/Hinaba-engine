from bottle import (run, static_file, request, view, redirect,
                    abort, get, post, ConfigDict, response, default_app, error, template, route)
from utils import file_validation, remove_media, board_directory, get_directory_size, generate_trip, dice, \
    check_admin
from functions import log_mod_action, send_private_message, get_current_user, hash_password, has_permissions
from json import loads, dumps
from os import path, mkdir, makedirs
from string import punctuation
from models import db, Post, Anon, Board, Report, Captcha, FavoritePost, Banner, News, PrivateMessage, Staff
from datetime import datetime, timedelta, UTC
from captcha.image import ImageCaptcha
from random import randint, choice
from peewee import IntegrityError
from uuid import uuid4
from typing import Optional, Dict

from middleware.middleware import fix_environ_middleware
from jobs.scheduler import start_scheduler

config = ConfigDict()
config.load_config('imageboard.conf')

basename: str = config['app.basename']

if basename[-1] == '/': basename = basename[:-1]  # remove trailing slash

STYLES: list[str] = config["style.styles"]

categories = {
    "Japanese Culture": ["a", 'c', 'w', 'm', 'cgl'],
    "Video Games": ['v', 'vg'],
}


@get('/static/<filename:path>')
def send_static(filename: path):
    return static_file(filename, root='static')


@get('/uploads/<filename:path>')
def send_upload(filename: path):
    return static_file(filename, root='uploads')


@get('/banners/<board_name>/<file_name>')
def serve_banner(board_name: str, file_name: str):
    return static_file(file_name, root=path.join("banners", board_name))


@get('/')
@view('home')
def home():
    show_nsfw: bool = ('True' == config['threads.show_nsfw'])
    active_content_size: int = get_directory_size('uploads')
    number_of_messages: int = Post.select().count()
    current_user: Anon = get_current_user(request)

    return dict(title=config['app.title'],
                welcome_message=config['app.welcome_message'],
                show_nsfw=show_nsfw, active_content_size=active_content_size,
                number_of_messages=number_of_messages, basename=basename, current_user=current_user)


@get('/captcha')
def generate_captcha():
    text = randint(10000, 99999)
    time_exp = datetime.now() + timedelta(minutes=5)

    captcha = Captcha(text=text, time_exp=time_exp)
    captcha.save()

    challenge = {
        'id': captcha.id,
        'text': text,
        'time_exp': str(time_exp)
    }

    return dumps(challenge)


@get('/captchaimg/<cha:int>')
def captcha_image(cha):
    image: ImageCaptcha = ImageCaptcha()
    code: str = Captcha.get_by_id(cha).text
    data = image.generate(code)
    response.content_type = "image/png"
    return data


@get('/<board_name>/')
@get('/<board_name:re:[a-z0-9]+>')
@get('/<board_name>/<page:int>')
@view('board')
def get_board(board_name: str, page: int = 1):
    try:
        board: Board = Board.get(Board.name == board_name)
    except:
        abort(404, "This page doesn't exist.")

    current_user: Anon = get_current_user(request)

    per_page: int = int(config['threads.per_page'])

    query = board.posts.where(Post.is_reply == False, Post.is_archived == False).order_by(Post.pinned.desc(),
                                                                                          Post.bumped_at.desc())
    threads = query.paginate(page, per_page)

    banners = Banner.select().where((Banner.board == board) & (Banner.archived == False))
    banner: Banner | None = choice(banners) if banners.exists() else None

    current_style: str = request.get_cookie('style', default='Yotsuba')
    if current_style not in STYLES:
        current_style = 'Yotsuba'

    return dict(
        board_name=board.name, board_title=board.title,
        threads=threads, board=board, current_page=page,
        is_detail=False, current_user=current_user,
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
    current_user: Anon = get_current_user(request)

    return dict(current_user=current_user, basename=basename)


@get('/<board_name>/thread/<refnum:int>')
@view('detail')
def get_thread(board_name: str, refnum: int):
    try:
        board: Board = Board.get(Board.name == board_name)
    except:
        return abort(404, "This page doesn't exist.")

    try:
        thread = board.posts.where(Post.refnum == refnum).get()
    except:
        abort(404, "This page doesn't exist.")

    banners = Banner.select().where((Banner.board == board) & (Banner.archived == False))
    banner: Banner | None = choice(banners) if banners.exists() else None

    current_style: str = request.get_cookie('style', default='Yotsuba')
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
def catalog(board_name: str):
    try:
        board: Board = Board.get(Board.name == board_name)
    except:
        return abort(404, "This page doesn't exist.")

    banners = Banner.select().where((Banner.board == board) & (Banner.archived == False))
    banner: Banner | None = choice(banners) if banners.exists() else None

    query = board.posts.where(Post.is_reply == False, Post.is_archived == False).order_by(Post.pinned.desc(),
                                                                                          Post.bumped_at.desc())

    # The query search

    if request.query and request.query['search']:
        search: str = request.query['search']

        query = board.posts.where(Post.is_reply == False, (
                (Post.title.contains(search)) | (Post.content.contains(search))
        )).order_by(Post.pinned.desc(), Post.bumped_at.desc())

    current_style: str = request.get_cookie('style', default='Yotsuba')
    if current_style not in STYLES:
        current_style = 'Yotsuba'

    return dict(threads=query, board_name=board.name,
                board_title=board.title, board=board,
                current_user=get_current_user(request),
                banner=banner.file if banner else None,
                style=current_style, basename=basename)


@get('/<board_name>/mod')
@view('reports')
def reports(board_name: str):
    try:
        board = Board.get(Board.name == board_name)
    except:
        return abort(404, "This page doesn't exist.")

    current_user: Anon = get_current_user(request)

    if f':{board_name}:' not in current_user.mod:
        return redirect(f'{basename}/{board_name}/')

    report_reasons: list[str] = loads(config['reports.reasons'])
    banners = Banner.select().where(Banner.board == board)

    return dict(board=board, bans=Anon.select().where(Anon.banned == True),
                current_user=current_user, board_name=board_name,
                reasons=report_reasons, reports=board.reports, basename=basename,
                banners=banners)


@get('/login')
@view('login')
def login():
    current_user: Anon = get_current_user(request)

    # Creates Default ADMIN User
    if not Staff.select().where(Staff.username == "admin").exists():
        Staff(username="admin", password=hash_password("password"), type="Admin",
              anon=get_current_user(request)).save()

    return dict(current_user=current_user, basename=basename, error=None)


@get('/admin')
@view('admin')
def admin_panel():
    current_user: Anon = get_current_user(request)
    staff: Staff = Staff.get(Staff.anon == current_user)

    logged_cookie: str = request.get_cookie("logged")

    if bool(logged_cookie):
        if logged_cookie != config['admin.token']:
            return redirect(f'{basename}/')
    else:
        return redirect(f'{basename}/')

    return dict(boards=Board.select(), current_user=current_user,
                board_name=None, staff_type=staff.type,
                basename=basename)


@get('/admin/edit/<board_name>')
@view('mod/edit')
def edit_board(board_name: str):
    if check_admin(request) == 1:
        return abort(403, "You are not allowed to do this.")

    board: Board = Board.get(Board.name == board_name)

    return dict(board=board, basename=basename)


@post('/admin/edit/<board_name>')
def do_edit(board_name: str):
    if check_admin(request) == 1:
        return abort(403, "You are not allowed to do this.")

    board: Board = Board.get(Board.name == board_name)

    if not board:
        return abort(404, "This board doesn't exist.")

    if request.forms.get('delete'):
        # Clicked "Delete board"

        for anon in Anon.select().where(Anon.mod != ""):
            anon.mod = anon.mod.replace(f':{board_name}:', '')
            anon.save()

        Post.delete().where(Post.board_id == board.id).execute()

        board.delete_instance()
        board_directory(board_name, remove=True)
        print(f"Successfully deleted board {board.name}")
    else:
        # Clicked "Save changes"
        title = request.forms.get('title')

        if board and title:
            board.title = title
            board.nsfw = bool(request.forms.get("nsfw"))
            board.save()
            print(f"Changed /{board.name}/ title to {title}")

    return redirect(f'{basename}/admin')


@get('/admin/new-board')
@view('mod/new_board')
def edit_board():
    if check_admin(request) == 1:
        return abort(403, "You are not allowed to do this.")

    return dict(basename=basename)


@post('/admin/new-board')
def do_new_board():
    if check_admin(request) == 1:
        return abort(403, "You are not allowed to do this.")

    uri = request.forms.get('uri')
    title = request.forms.get('title')

    if not all([uri, title]):
        return abort(404, "URI and title are required.")

    if any(char in list(punctuation + ' ') for char in title):
        return abort(400, "Boards can't have symbols in their title.")

    if Board.select().where(Board.name == uri).exists():
        return abort(400, "A board with this uri already exists.")

    data = {
        "name": uri,
        "nsfw": bool(request.forms.get("nsfw")),
        "title": title.strip(),
    }

    board: Board = Board(**data)
    board.save()
    board_directory(uri)

    print(f"New board /{board.name}/ successfully created.")

    return redirect(f'{basename}/admin')


@post('/login')
def do_login():
    current_user: Anon = get_current_user(request)

    username: str = request.forms.get('username')
    password: str = request.forms.get("password")

    staff = Staff.select().where(Staff.username == username)
    if staff.exists() and hash_password(password) == staff.get().password:
        response.set_cookie("logged", config['admin.token'])
        log_mod_action(get_current_user(request).ip, None, "Logged in")
        return redirect(f'{basename}/admin')
    return template('login.tpl', current_user=current_user, basename=basename,
                    error='Invalid username and/or password.')


@post('/logout')
def do_logout():
    response.delete_cookie('logged')
    log_mod_action(get_current_user(request).ip, None, "Logged out")

    return redirect(f'{basename}/')


@post('/<board_name>/')
def post_thread(board_name: str):
    captchares: str = request.forms.get('captchares')
    captchaid: str = request.forms.get('captchaid')

    challenge: Captcha = Captcha.get_by_id(captchaid)

    if (challenge.text != captchares or
            challenge.time_exp <= datetime.now()): return abort(403, "Invalid Captcha.")

    current_user: Anon = get_current_user(request)
    if get_current_user(request).banned: return redirect(f'{basename}/ban_info')

    board: Board = Board.get(Board.name == board_name)

    title: str = request.forms.get('title')
    content: str = request.forms.get('content')
    email: str = request.forms.get('email')
    capcode: str = request.forms.get("capcode")

    upload: str = request.files.get('upload')
    author_name: str | None = request.forms.get('author')

    if not author_name: author_name = "Anonymous"

    if not all([content, upload]): return abort(400, "Incomplete post.")

    if len(content) > int(config['threads.content_max_length']):
        return abort(400, "The content exeeds the maximum length.")

    trip_info: Dict[str, Optional[str]] = generate_trip(author_name)
    author_name, trip, sec_trip = trip_info["author_name"], trip_info["trip"], trip_info["sec_trip"]

    author: Anon = current_user
    refnum: int = board.lastrefnum
    save_path: Optional[str | int] = file_validation(board_name, refnum, upload)

    if len(content.split('\n')) < 10:
        short_content = ' '.join(content.split(' ')[:200])
    else:
        if any((len(item) > 200 for item in content.split(' '))):
            short_content = ' '.join(content.split(' ')[:200])
        else:
            short_content = '\n'.join(content.split('\n')[:10])

    if save_path == 1: return redirect(f'{basename}/{board_name}/')

    got_dice: str | None = dice(email)
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
        "capcode": current_user.capcode if capcode == "on" else '',
        "is_archived": False,
    }

    thread: Post = Post(**data)
    thread.save()

    board.lastrefnum += 1
    board.save()

    max_active_threads: int = int(config['threads.max_active'])

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
def post_reply(board_name: str, refnum: int):
    current_user: Anon = get_current_user(request)
    if get_current_user(request).banned: return redirect(f'{basename}/ban_info')

    board: Board = Board.get(Board.name == board_name)
    thread: Post = board.posts.where(Post.refnum == refnum).get()

    if thread.closed:
        return abort(423, "You cannot reply because this thread is locked.")

    if thread.is_archived:
        return abort(423, "You cannot reply because this thread is archived.")

    content: str = request.forms.get('content')
    author_name: str | None = request.forms.get('author')
    email: str = request.forms.get('email')
    capcode: str = request.forms.get("capcode")

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

    got_dice: str | None = dice(email)
    if got_dice:
        content = f"{got_dice}\n" + content
        short_content = f"{got_dice}\n" + short_content

    upload = request.files.get('upload')

    trip_info: Dict[str, Optional[str]] = generate_trip(author_name)
    author_name, trip, sec_trip = trip_info["author_name"], trip_info["trip"], trip_info["sec_trip"]

    author: Anon = current_user
    no: int = board.lastrefnum

    filename: str = ""
    save_path: str = ""

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
        "is_archived": False,
    }

    reply: Post = Post(**data)
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
                except:
                    pass

    # sage: if "email" field is a sage, then thread won't get bumped
    if email != "sage":
        thread.bumped_at = datetime.now().replace(microsecond=0)
        thread.save()

    board.lastrefnum += 1
    board.save()

    ## -- Auto archive --

    bump_limit: int = int(config['threads.bump_limit'])

    replies: list[Post] = board.posts.where(Post.is_reply == True, Post.refnum == refnum)

    if replies.count() >= bump_limit:
        thread.is_archived = True
        thread.save()

    # noko: if you type it in email field, you wont get redirect back to board, you will stay in thread
    if email == 'noko':
        redirect(f'{basename}/{board_name}/thread/{refnum}')
    else:
        redirect(f'{basename}/{board_name}/')


def remove_textual_refs(board: str, thread: str):
    for word in thread.content.split():
        if word[:2] == ">>":
            ref = word[2:]
            if ref.rstrip().isdigit():
                thread_ref: Post | None = board.posts.where(Post.refnum == ref).get_or_none()
                if thread_ref is None: continue
                replylist = loads(thread_ref.replylist)
                if thread.refnum in replylist:
                    replylist.remove(thread.refnum)
                    thread_ref.replylist = dumps(replylist)
                    thread_ref.save()


@post('/<board_name>/delete')
def delete_post(board_name: str):
    current_user: Anon = get_current_user(request)

    board: Board = Board.get(Board.name == board_name)
    form = dict(request.forms)

    if bool(form.get('report')):
        reason: list[str] = form.get('report')
        report_reasons = loads(config['reports.reasons'])
        if reason not in report_reasons: return redirect(f'{basename}/{board_name}/')
        for refnum in list(form)[:-1]:
            report: Report = Report(reason=reason, refnum=refnum, board=board,
                                    date=datetime.now().replace(microsecond=0))
            report.save()
    else:
        for refnum in form:
            thread: Post = board.posts.where(Post.refnum == refnum).get()
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
def ban(board_name: str):
    if f':{board_name}:' not in get_current_user(request).mod:
        return abort(403, "You are not allowed to do this.")

    form = dict(request.forms)

    reason: str = form.get('reason')

    user: str = form.get('user').strip()

    Anon.update(banned=True, ban_reason=reason, ban_date=datetime.now().replace(microsecond=0)).where(
        Anon.id == int(user)).execute()

    log_mod_action(get_current_user(request).ip, board_name, f"Banned user ID:{user} for {reason}")

    return redirect(f'{basename}/{board_name}/mod')


@post('/<board_name>/unban/<id>')
def unban(board_name: str, id: int):
    if f':{board_name}:' not in get_current_user(request).mod:
        return abort(403, "You are not allowed to do this.")

    form = dict(request.forms)

    anon = Anon.get(Anon.id == id)

    if bool(form.get("dall")):
        Post.delete().where(Post.author_id == anon.id).execute()

    if bool(form.get("unban")):
        Anon.update(banned=False, ban_reason=None, ban_date=None).where(Anon.id == id).execute()
        log_mod_action(get_current_user(request).ip, board_name, f"Unbanned user ID:{id}")

    return redirect(f'{basename}/{board_name}/mod')


@get('/<board_name>/thread/<refnum:int>/pin')
def thread_pin(board_name: str, refnum: int):
    if f':{board_name}:' not in get_current_user(request).mod:
        return abort(404, "This page doesn't exist.")

    board: Board = Board.get(Board.name == board_name)

    thread: Post = board.posts.where(Post.refnum == refnum).get()

    if thread.pinned:
        thread.pinned = False
        log_mod_action(get_current_user(request).ip, board_name, f"Unpinned thread {refnum}")
    else:
        log_mod_action(get_current_user(request).ip, board_name, f"Pinned thread {refnum}")
        thread.pinned = True

    thread.save()

    return redirect(f'{basename}/{board_name}/')


@get('/<board_name>/thread/<refnum:int>/close')
def thread_close(board_name: str, refnum):
    if f':{board_name}:' not in get_current_user(request).mod:
        return abort(404, "This page doesn't exist.")

    board: Board = Board.get(Board.name == board_name)

    thread: Post = board.posts.where(Post.refnum == refnum).get()

    if thread.closed:
        thread.closed = False
        log_mod_action(get_current_user(request).ip, board_name, f"Unclosed thread {refnum}")
    else:
        thread.closed = True
        log_mod_action(get_current_user(request).ip, board_name, f"Closed thread {refnum}")

    thread.save()

    return redirect(f'{basename}/{board_name}/')


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
def add_to_favorites(board_name: str, refnum: int):
    anon: Anon = get_current_user(request)
    thread: Post = Post.select().where(Post.refnum == refnum, Post.is_reply == False).get()

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
def remove_from_favorites(board_name: str, refnum: int):
    anon: Anon = get_current_user(request)
    thread: Post = Post.select().where(Post.refnum == refnum, Post.is_reply == False).get()

    query = FavoritePost.delete().where(
        (FavoritePost.anon == anon) & (FavoritePost.post == thread)
    )

    if query.execute() == 0:
        response.status = 404

    return redirect(f'{basename}/{board_name}/')


@get('/favorites')
def get_favorites():
    anon: Anon = get_current_user(request)
    favorites = (FavoritePost
                 .select(FavoritePost, Post)
                 .join(Post)
                 .where(FavoritePost.anon == anon))

    return {"favorites": [
        {"id": fav.post.id, "title": fav.post.title, "board_name": fav.post.board.name, "board_id": fav.post.board.id}
        for fav in favorites]}


# -- Banners -- #

@post('/<board_name>/upload_banner')
def upload_banner(board_name: str):
    if f':{board_name}:' not in get_current_user(request).mod:
        return abort(403, "You are not allowed to do this.")

    upload = request.files.get('upload')
    if not upload:
        return abort(400, "Please upload banner file!")

    file_ext = path.splitext(upload.filename)[1].lower()
    if file_ext not in ['.jpg', '.jpeg', '.png', '.gif']:
        return abort(400, "Unacceptable file extension. Please use: .jpg, .jpeg, .png, .gif")

    try:
        board: Board = Board.get(Board.name == board_name)
    except:
        return abort(400, "The board does not exist.")

    board_folder = path.join("banners", board_name)
    makedirs(board_folder, exist_ok=True)

    unique_name = f"{uuid4().hex}{file_ext}"
    file_path = path.join(board_folder, unique_name)
    upload.save(file_path)

    Banner.create(board=board, file=file_path, file_name=upload.filename)

    log_mod_action(get_current_user(request).ip, board_name, f"Uploaded banner {upload.filename}")

    return redirect(f"{basename}/{board_name}/mod")


@post('/<board_name>/del_banner/<banner_id>')
def del_banner(board_name: str, banner_id: int):
    if f':{board_name}:' not in get_current_user(request).mod:
        return abort(403, "You are not allowed to do this.")

    try:
        board: Board = Board.get(Board.name == board_name)
    except:
        return abort(400, "The board does not exist.")

    banner: Banner = Banner.get((Banner.board == board) & (Banner.id == banner_id))
    banner.delete_instance()

    log_mod_action(get_current_user(request).ip, board_name, f"Deleted banner {banner.file_name}")

    return redirect(f"{basename}/{board_name}/mod")


@post('/<board_name>/arch_banner/<banner_id>')
def archive_banner(board_name: str, banner_id: int):
    if f':{board_name}:' not in get_current_user(request).mod:
        return abort(403, "You are not allowed to do this.")

    try:
        board: Board = Board.get(Board.name == board_name)
    except:
        return abort(400, "The board does not exist.")

    try:
        banner: Banner = Banner.get((Banner.board == board) & (Banner.id == banner_id))
    except:
        return abort(400, "The banner does not exist.")

    if banner.archived:
        log_mod_action(get_current_user(request).ip, board_name, f"Unarchived banner {banner.file_name}")
        banner.archived = False
    else:
        log_mod_action(get_current_user(request).ip, board_name, f"Archived banner {banner.file_name}")
        banner.archived = True

    banner.save()

    return redirect(f"{basename}/{board_name}/mod")


# -- Styles -- #

@route('/set_style/<style_name>')
def set_style(style_name: str):
    if style_name in STYLES:
        response.set_cookie('style', style_name, path="/", max_age=3600)
    return ''


# -- Thread Archive -- #
@get('/<board_name>/archive')
@view('archive')
def get_archive(board_name: str):
    try:
        board: Board = Board.get(Board.name == board_name)
    except:
        return abort(404, "This page doesn't exist.")

    banners: list[Banner] = Banner.select().where((Banner.board == board) & (Banner.archived == False))
    banner: Banner = choice(banners) if banners.exists() else None

    current_style: str = request.get_cookie('style', default='Yotsuba')
    if current_style not in STYLES:
        current_style = 'Yotsuba'

    return dict(board_name=board.name, board=board,
                board_title=board.title,
                current_user=get_current_user(request),
                basename=basename,
                banner=banner.file if banner else None,
                style=current_style,
                )


# -- Thread archiving -- #

@get('/<board_name>/archive/<refnum:int>')
def archive_thread(board_name: str, refnum: int):
    if f':{board_name}:' not in get_current_user(request).mod:
        return abort(403, "You are not allowed to do this.")

    try:
        Post.update(is_archived=True).where(Post.refnum == refnum, Post.is_reply == False).execute()
        log_mod_action(get_current_user(request).ip, board_name, f"Archived thread {refnum}")
    except Post.DoesNotExist:
        response.status = 404
    except IntegrityError:
        response.status = 409

    return redirect(f'{basename}/{board_name}/')


@get('/<board_name>/unarchive/<refnum:int>')
def unarchive_thread(board_name: str, refnum: int):
    if f':{board_name}:' not in get_current_user(request).mod:
        return abort(403, "You are not allowed to do this.")

    try:
        Post.update(is_archived=False).where(Post.refnum == refnum, Post.is_reply == False).execute()
        log_mod_action(get_current_user(request).ip, board_name, f"Unarchived thread {refnum}")

    except Post.DoesNotExist:
        response.status = 404
    except IntegrityError:
        response.status = 409

    return redirect(f'{basename}/{board_name}/thread/{refnum}')


# -- Exporting thread -- #
@get('/<board_name>/thread/<refnum:int>/export')
def export_thread(board_name: str, refnum: int):
    try:
        board = Board.get(Board.name == board_name)
        thread = Post.get(Post.board == board, Post.refnum == refnum, Post.is_reply == False)

        replies = Post.select().where(Post.board == board, Post.replyrefnum == refnum, Post.is_reply == True)

        thread_data = {
            "id": thread.refnum,
            "board": board.name,
            "author": thread.author_name,
            "title": thread.title,
            "content": thread.content,
            "file": f"{basename}/{thread.image}" if thread.image else "",
            "is_archived": thread.is_archived,
            "replies_amount": replies.count(),
            "replies": [
                {
                    "id": reply.refnum,
                    "author": reply.author_name,
                    "title": reply.title,
                    "content": reply.content,
                    "file": f"{basename}/{thread.image}" if reply.image else ""
                }
                for reply in replies
            ]
        }

        now = datetime.now()
        filename = f"thread-id{refnum}-{now.strftime('%m-%d-%Y-%H:%M:%S')}.json"

        response.content_type = 'application/json'
        response.headers['Content-Disposition'] = f'attachment; filename="{filename}"'
        return dumps(thread_data, ensure_ascii=False, indent=4)
    except Board.DoesNotExist:
        abort(404, "Board not found.")
    except Post.DoesNotExist:
        abort(404, "Thread not found.")


# -- Staff Management -- #

@get('/admin/staff')
@view('mod/manage_staff')
def manage_staff():
    return dict(basename=basename)


@get('/admin/staff/<id>')
@view('mod/staff')
def staff(id: int):
    staff: Staff = Staff.get(Staff.anon == get_current_user(request))
    if not has_permissions(staff.type, "managestaff"):
        return redirect(f"{basename}/admin")

    c_staff = Staff.get(Staff.id == id)
    anon = Anon.select().where(Anon.id == staff.anon.id).get()
    return dict(basename=basename, anon=anon, staff=c_staff, staff_type=staff.type)


@post('/admin/staff/<id>')
def do_staff(id: int):
    staff = Staff.get(Staff.id == id)
    anon = Anon.select().where(Anon.id == staff.anon.id).get()

    username = request.forms.get('username')
    password = request.forms.get('password')
    board = request.forms.get('board')

    if request.forms.get('add') and f':{board}:' not in anon.mod:
        anon.mod += f':{board}:'
        print(f"Adding ID:{anon.id} as mod to /{board}/")
    elif request.forms.get('rm'):
        anon.mod = anon.mod.replace(f':{board}:', '')
        print(f"Removing ID:{anon.id} as mod from /{board}/")
    elif request.forms.get('delete'):
        anon.mod = ''
        anon.capcode = ''
        anon.can_capcode = False
        Staff.delete().where(Staff.id == id).execute()
        print(f"Removing ID:{anon.id} as mod from database")
    else:
        anon.capcode = request.forms.get('capcode') if request.forms.get('capcode') else ''
        anon.can_capcode = bool(request.forms.get('can_capcode'))
        staff.username = username
        staff.password = hash_password(password)
        staff.save()
        print(f"Saving changes to ID:{anon.id}")

    anon.save()

    return redirect(f'{basename}/admin/staff')


@get('/admin/staff/new')
@view('mod/new_staff')
def new_staff():
    staff: Staff = Staff.get(Staff.anon == get_current_user(request))
    if not has_permissions(staff.type, "managestaff"):
        return redirect(f"{basename}/admin")

    if check_admin(request) == 1:
        return abort(403, "You are not allowed to do this.")

    return dict(basename=basename)


@post('/admin/staff/new')
def do_new_staff():
    staff: Staff = Staff.get(Staff.anon == get_current_user(request))
    if not has_permissions(staff.type, "managestaff"):
        return redirect(f"{basename}/admin")

    ip = request.forms.get('ip')
    username = request.forms.get('username')
    password = request.forms.get('password')
    type = request.forms.get('type')
    can_capcode = bool(request.forms.get('can_capcode'))
    capcode = request.forms.get('capcode')
    board = request.forms.get('board')

    if not all([username, password, type]):
        return abort(403, "Username/Password and Group is required.")

    if Staff.select().where(Staff.username == username).exists():
        return abort(403, "User with that name is a staff arleady.")

    anon = Anon.select().where(Anon.ip == ip)
    if anon.exists():
        anon = anon.get()
    else:
        anon = Anon(ip=ip)
    if board:
        anon.mod = f":{board}:"

    anon.capcode = capcode
    anon.can_capcode = can_capcode
    anon.save()

    new_staff = Staff(username=username, password=hash_password(password), type=type, anon=anon)
    new_staff.save()

    return redirect(f'{basename}/admin/staff')


# -- News (for staff) -- #

@get('/admin/edit_news')
@view('mod/edit_news')
def edit_news():
    if check_admin(request) == 1:
        return abort(403, "You are not allowed to do this.")

    return dict(basename=basename)


@post('/admin/edit_news')
def do_edit_news():
    if check_admin(request) == 1:
        return abort(403, "You are not allowed to do this.")

    name = request.forms.get('name')
    subject = request.forms.get('subject')
    body = request.forms.get('body')

    if not all([name, body]):
        return abort(400, "You need to enter all fields.")

    data = {
        "name": name,
        "subject": subject,
        "body": body,
    }

    board: News = News(**data)
    board.save()

    log_mod_action(get_current_user(request).ip, None, f"Posted a news entry")

    return redirect(f'{basename}/admin/edit_news')


@get('/admin/edit_news/delete/<id:int>')
def delete_news(id: int):
    if check_admin(request) == 1:
        return abort(403, "You are not allowed to do this.")

    News.delete().where(News.id == id).execute()
    log_mod_action(get_current_user(request).ip, None, f"Deleted a news entry")

    return redirect(f'{basename}/admin/edit_news')


# -- Mod actions logging -- #

@get('/admin/log')
@view('mod/mod_log')
def mod_log():
    staff: Staff = Staff.get(Staff.anon == get_current_user(request))
    if has_permissions(staff.type, "modlog"):
        return dict(basename=basename)
    return redirect(f'{basename}/admin')


# -- Private Messages -- #

@get('/admin/inbox')
@view('mod/inbox')
def inbox():
    if check_admin(request) == 1:
        return abort(403, "You are not allowed to do this.")

    return dict(basename=basename, current_user=get_current_user(request))


# View PM

@get('/admin/PM/<message_id>')
@view('mod/PM')
def PM(message_id):
    if check_admin(request) == 1:
        return abort(403, "You are not allowed to do this.")

    message: PrivateMessage = PrivateMessage.select().where(PrivateMessage.id == message_id)

    if not message.exists():
        return abort(404, "Message not found.")

    message = message.get()

    if message.unread:
        message.unread = False
        message.save()

    return dict(basename=basename, message=message)


# PM delete

@post('/admin/PM/<message_id>')
def do_PM(message_id):
    if check_admin(request) == 1:
        return abort(403, "You are not allowed to do this.")

    if request.forms.get('delete'):
        PrivateMessage.delete().where(PrivateMessage.id == message_id,
                                      PrivateMessage.to == get_current_user(request).id).execute()

    return redirect(f'{basename}/admin/inbox')


# PM reply

@get('/admin/PM/<message_id>/reply')
def PM_reply(message_id):
    if check_admin(request) == 1:
        return abort(403, "You are not allowed to do this.")

    message: PrivateMessage = PrivateMessage.select().where(PrivateMessage.id == message_id)

    if not message.exists():
        return abort(404, "Message not found.")

    reciever: Anon = Anon.select().where(Anon.id == message.get().sender).get()

    return template('mod/new_PM.tpl', basename=basename, reciever=reciever,
                    reply=f">{message.get().message}\n")


# New PM

@get('/admin/new_PM/<reciever_id>')
@view('mod/new_PM')
def new_PM(reciever_id):
    if check_admin(request) == 1:
        return abort(403, "You are not allowed to do this.")

    reciever: Anon = Anon.select().where(Anon.id == reciever_id).get()

    return dict(basename=basename, reciever=reciever, reply='')


@post('/admin/new_PM/<reciever_id>')
def do_new_PM(reciever_id):
    if check_admin(request) == 1:
        return abort(403, "You are not allowed to do this.")

    message = request.forms.get('message')

    if not message:
        return abort(400, "You need to enter message.")

    sender: Anon = get_current_user(request)

    send_private_message(sender.id, reciever_id, message)

    return redirect(f'{basename}/admin')


if __name__ == '__main__':

    db.connect()

    if not path.isdir('uploads'): mkdir('uploads')
    if not path.isdir('banners'): mkdir('banners')

    url_prefix: str = basename

    app = default_app()
    app.wsgi = fix_environ_middleware(app.wsgi, url_prefix)
    start_scheduler()
    production = bool(int(config['app.production']))

    run(
        debug=not production,
        reloader=not production,
        host=config['app.host'],
        port=config['app.port']
    )
