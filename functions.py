from models import ModLogs, PrivateMessage, Anon

GROUPS = ["JANITOR", "MOD", "ADMIN"]
PERMISSIONS = {
    "show_ip": "MOD", # View IP address
    "delete": "JANITOR", # Delete a post
    "ban": "MOD", # Ban a user for a post
    "bandelete": "MOD", # Ban and delete (one click; instant)
    "unban": "MOD", # Unban a user
    "deletebyip": "MOD", # Delete all posts by IP
    "deletebyip_global": "ADMIN", # Delete all posts by IP across all boards
    "sticky": "MOD", # Sticky a thread
    "lock": "MOD", # Lock a thread
    "postinlocked": "MOD", # Post in a locked thread
    "bumplock": "MOD", # Prevent a thread from being bumped
    "view_bumplock": "MOD", # View whether a thread has been bumplocked ("-1" to allow non-mods to see too)
    "editpost": "ADMIN", # Edit a post

    # Administration

    "reports": "JANITOR", # View reports
    "report_dismiss": "JANITOR", # Dismiss an abuse report
    "report_dismiss_ip": "JANITOR", # Dismiss an abuse report by IP
    "view_banlist": "MOD", # View banlist
    "view_banstaff": "MOD", # View the username of the mod who made a ban
    "view_banquestionmark": False, # If the moderator doesn't fit the ['view_banstaff''] (previous) permission, show him just a "?" instead. Otherwise, it will be "Mod" or "Admin".
    "view_banexpired": True, # Show expired bans in the ban list
    "view_ban": "MOD", #  View ban for IP address
    "newboard": "ADMIN", # Create a new board
    "manageboards": "ADMIN", # Manage existing boards (change title, etc)
    "deleteboard": "ADMIN", # Delete a board
    "managestaff": "MOD", # Manage staff
    "promoteusers": "ADMIN", # Promote/demote users
    "editusers": "ADMIN", # Edit any users' login information
    "change_password": "JANITOR", # Change user's own password
    "deleteusers": "ADMIN", # Delete users
    "createusers": "ADMIN", # Create users
    "modlog": "ADMIN", # View moderation log
    "show_ip_modlog": "ADMIN", # View IP addresses in moderation log
    "create_pm": "JANITOR", # Create a PM (viewing mod usernames)
    "master_pm": "ADMIN", # Read any PM, sent to or from anybody
    "noticeboard": "JANITOR", # Read the moderator noticeboard
    "noticeboard_post": "MOD", # Post in the moderator noticeboard
    "noticeboard_delete": "ADMIN", # Delete entries from the noticeboard
    "news": "ADMIN", # Post news entries
    "news_custom": "ADMIN", # Custom name when posting news
    "news_delete": "ADMIN", # Delete news entries
    "view_ban_appeals": "MOD", # View ban appeals
    "ban_appeals": "ADMIN", # Accept and deny ban appeals

    # ETC

    "archive": "ADMIN", # Archive threads
    "unarchive": "ADMIN", # Unarchive threads
    "banners": "ADMIN", # Manage banners for board
    "capcode": "ADMIN", # Able to use capcodes
}

CUSTOM_CAPCODES = {
    "MOD": [
        'color:purple', # Change name style; optional
        'color:purple', # Change tripcode style; optional
    ],
    "ADMIN": [
        'color:red;font-weight:bold', # Change name style; optional
        'color:red;font-weight:bold', # Change tripcode style; optional
    ]
}

def get_current_user(req):
    ip = req.get('HTTP_X_FORWARDED_FOR')

    if ip is None: ip = req.get('REMOTE_ADDR')

    try:
        current_user = Anon.get(Anon.ip == ip)
    except:
        anon = Anon(ip=ip)
        anon.save()

        current_user = anon

    return current_user


def log_mod_action(ip: str, board: str | None, action: str) -> None:
    try:
        data = {
            "ip": ip,
            "board": board,
            "text": action
        }

        mod_logs = ModLogs(**data)
        mod_logs.save()
    except Exception as e:
        print(f"Error: {e}")


def send_private_message(sender: int, reciever: int, message: str) -> None:
    try:
        data = {
            "sender": sender,
            "to": reciever,
            "message": message
        }

        private_message = PrivateMessage(**data)
        private_message.save()
    except Exception as e:
        print(f"Error: {e}")

def custom_capcode_info(group: str) -> tuple[str, str] | None:
    if group not in CUSTOM_CAPCODES: return None

    return CUSTOM_CAPCODES[group][0], CUSTOM_CAPCODES[group][1]


def get_group_number(group: str) -> int | None:
    if group not in GROUPS: return None
    return GROUPS.index(group) + 1

def get_group_name(index: int) -> str | None:
    if index > len(GROUPS): return None
    if index < 1: return None
    return GROUPS[index - 1]

def compare_groups(current_group: str, required_group: str) -> bool:
    return get_group_number(current_group) >= get_group_number(required_group)

def has_permissions(group: str, action: str) -> bool:
    if not action in PERMISSIONS.keys(): return False
    if PERMISSIONS[action] == -1: return True
    if isinstance(PERMISSIONS[action], bool): return PERMISSIONS[action]

    return compare_groups(group, PERMISSIONS[action])