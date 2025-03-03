% from utils import author_color, image_size, is_video, get_country_info_by_ip
% from models import Post, Board, FavoritePost
% from bottle import ConfigDict
% from json import loads

% config = ConfigDict()
% config.load_config('imageboard.conf')
% int_boards = loads(config['app.int_boards'])

<div class="thread" id="{{thread.refnum}}">
  <div class="postContainer opContainer">
    <div class="post op">
      <span id="hide-thread" title="Hide thread">
        <img alt="H" class="extButton threadHideButton" data-cmd="hide" src="{{basename}}/static/img/post_expand_minus.png" title="Hide thread">
      </span>
      <div class="file">
        <div class="fileText">File:
          <a href="{{basename}}/{{thread.image}}" title="{{thread.filename}}">
            % if len(thread.filename.split(".")[0]) > 20:
              {{thread.filename[:20]}}(...).{{thread.filename.split(".")[-1]}}
            % else:
              {{thread.filename}}
            % end
          </a>

          % if not is_video(thread.filename):
            [<a href="https://www.google.com/searchbyimage?image_url={{host}}{{basename}}/{{thread.image}}&client=app" class="gsearch">S</a>]
          % end

          ({{image_size(thread.image)}})
        </div>
        <a class="fileThumb" target="_blank">
          % if is_video(thread.filename):
            <video width="250" height="250" class="Thread-video">
            <source src="{{basename}}/{{thread.image}}" type="video/{{thread.image[-3:]}}">
            Your browser does not support the video tag.
            </video>
          % else:
            <img class="Thread-image" src="{{basename}}/uploads/{{board_name}}/{{thread.refnum}}s.jpg">
          % end
        </a>
      </div>
      <div class="postInfo">
        <input type="checkbox" name="{{thread.refnum}}" value="delete">
        <span class="subject">{{thread.title}}</span>

        % if thread.capcode == "## Mod":
        % name_class = "nameBlock capcodeMod"
        % elif thread.capcode == "## Admin":
        % name_class = "nameBlock capcodeAdmin"
        % elif thread.capcode == "## Developer":
        % name_class = "nameBlock capcodeDeveloper"
        % elif thread.capcode == "## Founder":
        % name_class = "nameBlock capcodeFounder"
        % elif thread.capcode == "## Manager":
        % name_class = "nameBlock capcodeManager"
        % elif thread.capcode == "## Verified":
        % name_class = "nameBlock capcodeVerified"
        % else:
        % name_class = "nameBlock"
        % end 

        <span class="{{name_class}}">
          <span class="name">{{thread.author_name}}</span>

          % if (not thread.capcode) and (board_name in int_boards):
            % country_name, country_code = get_country_info_by_ip(thread.author.ip)
            % if country_name and country_code:
                <span title="{{country_name}}" class="flag flag-{{country_code}}"></span>
            % end
          % end

          % if thread.capcode == "## Mod":
            <strong class="capcode hand id_mod" title="Highlight posts by Moderators">## Mod</strong>
            <img src="{{basename}}/static/img/modicon.gif" alt="Mod Icon" title="This user is a PyChan Moderator." style="margin-bottom: -3px;">
          % elif thread.capcode == "## Admin":
            <strong class="capcode hand id_admin" title="Highlight posts by Administrators">## Admin</strong>
            <img src="{{basename}}/static/img/adminicon.gif" alt="Admin Icon" title="This user is a PyChan Administrator." style="margin-bottom: -3px;">
          % elif thread.capcode == "## Developer":
            <strong class="capcode hand id_developer" title="Highlight posts by Developer">## Developer</strong>
            <img src="{{basename}}/static/img/developericon.gif" alt="Developer Icon" title="This user is a PyChan Developer." style="margin-bottom: -3px;">
          % elif thread.capcode == "## Founder":
            <strong class="capcode hand id_founder" title="Highlight posts by Founder">## Founder</strong>
            <img src="{{basename}}/static/img/foundericon.gif" alt="Founder Icon" title="This user is a PyChan Founder." style="margin-bottom: -3px;">
          % elif thread.capcode == "## Manager":
            <strong class="capcode hand id_manager" title="Highlight posts by Manager">## Manager</strong>
            <img src="{{basename}}/static/img/managericon.gif" alt="Manager Icon" title="This user is a PyChan Manager." style="margin-bottom: -3px;">
          % elif thread.capcode == "## Verified":
            <strong class="capcode hand id_verified" title="Highlight posts by Verified">## Verified</strong>
          % end

          % if thread.trip:
          <span class="postertrip">!{{thread.trip}}</span>
          % end
          % if thread.sec_trip:
          <span class="postertrip">!!{{thread.sec_trip}}</span>
          % end
        </span>

        % if f':{board_name}:' in current_user.mod:
          [{{ thread.author.ip }}]
        % end

        <span class="dateTime">{{thread.date}}</span>
        <span class="postNum">
          <a href="{{basename}}/{{board_name}}/thread/{{thread.id}}">No.</a>
          <a class="dopen">{{thread.refnum}}</a>
        </span>

        % if thread.pinned:
          <img class="pin" src="{{basename}}/static/img/sticky.gif"></img>
        % end

        % if thread.closed:
          <img class="pin" src="{{basename}}/static/img/locked.gif"></img>
        % end

        % if not is_detail:
          [<a class="btn Thread-repbtn" href="{{basename}}/{{board_name}}/thread/{{thread.refnum}}">Reply</a>]
        % end

        [<a class="btn" title="Export as JSON" href="{{basename}}/{{board_name}}/thread/{{thread.refnum}}/export">Export</a>]

        % if FavoritePost.select().where(FavoritePost.anon == current_user, FavoritePost.post == thread).exists():
          [<a href="{{basename}}/{{board_name}}/unfavorite/{{thread.refnum}}">Unfavorite</a>]
        % else:
          [<a href="{{basename}}/{{board_name}}/favorite/{{thread.refnum}}">Favorite</a>]
        % end

        % if f':{board_name}:' in current_user.mod:
          [<a class="dropin" href="{{basename}}/{{board_name}}/archive/{{thread.refnum}}">Archive</a>]
          [<a class="dropin" href="{{basename}}/{{board_name}}/thread/{{thread.refnum}}/pin">Pin</a>]
          [<a class="dropc" href="{{basename}}/{{board_name}}/thread/{{thread.refnum}}/close">Close</a>]
        % end
      </div>

      <blockquote class="postMessage">
        % include('thread_text', board_name=board_name, board=board)
      </blockquote>
    </div>

  </div>

  % query = board.posts.where(Post.replyrefnum == thread.refnum).order_by(Post.refnum.desc())
  % replies = query if is_detail else query.limit(4)
  % if not is_detail and query.count() > 4:
    <span class="load-replies btn">Load {{query.count() - 4}} replies</span>
  % end

  % for reply in reversed(replies):
  % include('reply', reply=reply)
  % end
</div>
