import os
import re
import random
import hashlib, base64
import shutil
import filetype
from string import ascii_lowercase
from PIL import Image
from tripcode import tripcode
from bottle import ConfigDict
from typing import Optional, Dict, Any

config = ConfigDict()
config.load_config('imageboard.conf')

def thumbnail(path: str, refnum: int, ext: str, is_reply: bool = False) -> None:
    """Creates a thumbnail for an image."""
    save_path = f"{'/'.join(path.split('/')[:2])}/{refnum}s.jpg"

    with Image.open(path) as im:

        if im.height < im.width:

            thumb_width = 125 if is_reply else 250
            thumb_height = round(im.height * (thumb_width / im.width))

            im = im.resize((thumb_width, thumb_height))
        else:
            thumb_height = 125 if is_reply else 250
            thumb_width = round(im.width * (thumb_height / im.height))

            im = im.resize((thumb_width, thumb_height))

        if ext == '.png' and im.mode == "RGBA":

            bg = Image.new("RGB", (thumb_width, thumb_height), (255, 255, 255))

            bg.paste(im, im)
            bg.save(save_path)
        elif ext == '.gif':
            im.seek(0)
            im = im.convert('RGB')
            im.save(save_path)
        else:
            im.save(save_path)

def file_validation(board_name: str, refnum: int, upload: Any, is_reply: bool = False) -> Optional[str | int]:
    """Validates uploaded file and creates a thumbnail if valid."""
    name, ext = os.path.splitext(upload.filename)

    valid_ext = ('png', 'jpg', 'jpeg', 'gif', 'mp4', 'webm', 'ogg')

    if ext[1:] not in valid_ext:
        return 1

    save_path = f"uploads/{board_name}/{refnum}{ext}"
    upload.save(save_path)

    mime = filetype.guess(save_path)
    if mime.EXTENSION not in valid_ext or mime.EXTENSION != ext[1:]:
        os.remove(save_path)
        return 1

    thumbnail(save_path, refnum, ext, is_reply)

    return save_path

def remove_media(path: str) -> None:
    """Removes a file and its associated thumbnail."""
    name, ext = os.path.splitext(path)

    if ext not in ('.mp4', '.webm', '.ogg'):
        os.remove(name + "s.jpg")

    os.remove(path)

def random_name() -> str:
    """Generates a random name."""
    return ''.join(random.choices(ascii_lowercase, k=8))

def board_directory(name: str, remove: bool = False) -> None:
    """Creates or removes a board directory."""
    if remove:
        shutil.rmtree(f"uploads/{name}")
    else:
        os.makedirs(f"uploads/{name}", exist_ok=True)

def get_size_format(b: int, factor: int = 1024, suffix: str = 'B') -> str:
    """
    Scale bytes to its proper byte format
    e.g:
        1253656 => '1.20MB'
        1253656678 => '1.17GB'
    """
    for unit in ["", "K", "M", "G", "T", "P", "E", "Z"]:
        if b < factor:
            return f"{b:.2f}{unit}{suffix}"
        b /= factor
    return f"{b:.2f}Y{suffix}"

def get_directory_size(directory: str) -> int:
    """Returns the `directory` size in bytes."""
    total = 0
    try:
        # print("[+] Getting the size of", directory)
        for entry in os.scandir(directory):
            if entry.is_file():
                # if it's a file, use stat() function
                total += entry.stat().st_size
            elif entry.is_dir():
                # if it's a directory, recursively call this function
                total += get_directory_size(entry.path)
    except NotADirectoryError:
        # if `directory` isn't a directory, get the file size then
        return os.path.getsize(directory)
    except PermissionError:
        # if for whatever reason we can't open the folder, return 0
        return 0
    return total

def author_color(author: str) -> str:
    """Generates a consistent color for an author."""
    return '#' + hashlib.blake2b(author.encode()).hexdigest()[:6]

def image_size(path: str) -> str:
    """Returns the size and dimensions of an image or video."""
    size = os.stat(path).st_size

    if not is_video(path):
        with Image.open(path) as im:
            width, height = im.size
        return f"{get_size_format(size)}, {width} x {height}"
    else:
        return get_size_format(size)

def is_video(filename: str) -> bool:
    """Checks if a file is a video based on its extension."""
    name, ext = os.path.splitext(filename)

    if ext in ('.webm', '.mp4', '.ogg'): return True

    return False

def short_msg(string: str) -> str:
    """Trims a message to a short preview."""
    words = string.split()
    return ' '.join(words[:22]) + (' ...' if len(words) > 22 else '')

def generate_trip(name: str) -> Dict[str, Optional[str]]:
    """Generates tripcodes for a user."""
    name = re.sub(r"\#+$", "", re.sub(r"[\r\n]", "", name.strip()))
    info = {
        "author_name": name,
        "trip": "",
        "sec_trip": "",
    }

    if '#' in name:
        name = name.replace("&#", "&&")
        parts = name.replace("&&", "&#").split("#", 2)

        name_temp = parts[0]
        trip = parts[1] if len(parts) > 1 else ""
        sec_trip = parts[2] if len(parts) > 2 else ""

        info["author_name"] = name_temp

        if trip != "":
            info["trip"] = tripcode(trip)

        if sec_trip != "":
            salt = config.get("security.trip_salt", "ofTSVIrPGK")
            sha = base64.b64encode(hashlib.sha1((sec_trip + salt).encode()).digest()).decode()[:11]
            info["sec_trip"] = sha

    return info

def dice(email: Optional[str]) -> Optional[str] | None:
    """Simulates dice rolls based on the email field."""
    if email:
        match = re.search(r"dice[ +](\d+)[ d+](\d+)(([ +-]+?)(-?\d+))?", email)
        if match:
            dice_txt = "rolled "
            dice_num = min(25, int(match.group(1)))
            dice_side = int(match.group(2))
            dice_add_expr = match.group(3)
            dice_sign = match.group(4)
            dice_add = int(match.group(5)) if match.group(5) else 0

            dice_sum = 0
            for i in range(dice_num):
                dice_rand = random.randint(1, dice_side)
                if i:
                    dice_txt += ", "
                dice_txt += str(dice_rand)
                dice_sum += dice_rand

            if dice_add_expr:
                if "-" in dice_sign:
                    dice_add *= -1
                dice_txt += (" + " if dice_add >= 0 else " - ") + str(abs(dice_add))
                dice_sum += dice_add

            dice_txt += f" = {dice_sum}"

            return dice_txt

    return None
