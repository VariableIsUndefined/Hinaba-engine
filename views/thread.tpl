% from utils import author_color, image_size, is_video
% from models import Post, Board

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
              [<a href="https://www.google.com/searchbyimage?image_url={{host}}{{basename}}/{{thread.image}}&client=app"class="gsearch">S</a>]
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

        % if f':{board_name}:' in current_user.mod:
        % name_class = "nameBlock capcodeMod"
        % else:
        % name_class = "nameBlock"
        % end 
        <span class="{{name_class}}">
          <span class="name">{{thread.author_name}}</span>

          % if f':{board_name}:' in thread.author.mod:
            <strong class="capcode hand id_mod" title="Highlight posts by Moderators">## Mod</strong>
            <img src="{{basename}}/static/img/modicon.gif" alt="Mod Icon" title="This user is a PyChan Moderator." style="margin-bottom: -3px;">
          % end

          % if thread.trip:
          <span class="postertrip">!{{thread.trip}}</span>
          % end
          % if thread.sec_trip:
          <span class="postertrip">!!{{thread.sec_trip}}</span>
          % end
        </span>

        % if f':{board_name}:' in current_user.mod:
          (IP: {{ thread.author.ip }})
        % end 

        <span class="dateTime">{{thread.date}}</span>
        <span class="postNum">
          <a href="{{basename}}/{{board_name}}/thread/{{thread.id}}">No.</a>
          <span class="dopen">{{thread.refnum}}</span>
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

        % if f':{board_name}:' in current_user.mod:
          [<a class="dropin" href="{{basename}}/{{board_name}}/thread/{{thread.refnum}}/pin">Pin</a>]
          [<a class="dropc" href="{{basename}}/{{board_name}}/thread/{{thread.refnum}}/close">Close</a>]
        % end 
      </div>

      <blockquote class="postMessage">
        % include('thread_text', board_name=board_name, board=board)
      </blockquote>
    </div>

  </div>

  % query = board.posts.where(Post.replyrefnum == thread.refnum).order_by(Post.refnum.asc())
  % replies = query if is_detail else query.offset(query.count() - 4)
  % if not is_detail and query.count() > 4:
    <span class="load-replies btn">Load {{query.count() - 4}} replies</span>
  % end

  % for reply in replies:
  % include('reply', reply=reply)
  % end
</div>
