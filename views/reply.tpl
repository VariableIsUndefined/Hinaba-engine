% from utils import author_color
% from json import loads
% from models import Post
<div id="{{reply.refnum}}" class="postContainer replyContainer">
  <div class="sideArrows">&gt;&gt;</div>
  <div class="post reply">
    <div class="postInfo">
      <input type="checkbox" name="{{reply.refnum}}" value="delete">

      % if reply.capcode == "## Mod":
      % name_class = "nameBlock capcodeMod"
      % elif reply.capcode == "## Admin":
      % name_class = "nameBlock capcodeAdmin"
      % elif reply.capcode == "## Developer":
      % name_class = "nameBlock capcodeDeveloper"
      % elif reply.capcode == "## Founder":
      % name_class = "nameBlock capcodeFounder"
      % elif reply.capcode == "## Manager":
      % name_class = "nameBlock capcodeManager"
      % elif reply.capcode == "## Verified":
      % name_class = "nameBlock capcodeVerified"
      % else:
      % name_class = "nameBlock"
      % end 

      <span class="{{name_class}}">
        <span class="name">{{reply.author_name}}</span>

        % if reply.capcode == "## Mod":
          <strong class="capcode hand id_mod" title="Highlight posts by Moderators">## Mod</strong>
          <img src="{{basename}}/static/img/modicon.gif" alt="Mod Icon" title="This user is a PyChan Moderator." style="margin-bottom: -3px;">
        % elif reply.capcode == "## Admin":
          <strong class="capcode hand id_admin" title="Highlight posts by Administrators">## Admin</strong>
          <img src="{{basename}}/static/img/adminicon.gif" alt="Admin Icon" title="This user is a PyChan Administrator." style="margin-bottom: -3px;">
        % elif reply.capcode == "## Developer":
          <strong class="capcode hand id_developer" title="Highlight posts by Developer">## Developer</strong>
          <img src="{{basename}}/static/img/developericon.gif" alt="Developer Icon" title="This user is a PyChan Developer." style="margin-bottom: -3px;">
        % elif reply.capcode == "## Founder":
          <strong class="capcode hand id_founder" title="Highlight posts by Founder">## Founder</strong>
          <img src="{{basename}}/static/img/foundericon.gif" alt="Founder Icon" title="This user is a PyChan Founder." style="margin-bottom: -3px;">
        % elif reply.capcode == "## Manager":
          <strong class="capcode hand id_manager" title="Highlight posts by Manager">## Manager</strong>
          <img src="{{basename}}/static/img/managericon.gif" alt="Manager Icon" title="This user is a PyChan Manager." style="margin-bottom: -3px;">
        % elif reply.capcode == "## Verified":
          <strong class="capcode hand id_verified" title="Highlight posts by Verified">## Verified</strong>
        % end

        % if reply.trip:
        <span class="postertrip">!{{reply.trip}}</span>
        % end
        % if reply.sec_trip:
        <span class="postertrip">!!{{reply.sec_trip}}</span>
        % end
      </span>

      % if f':{board_name}:' in current_user.mod:
      (IP: {{ thread.author.ip }})
      % end 

      <span class="dateTime">{{reply.date}}</span>

      <span class="postNum">
        <a href="{{basename}}/{{board_name}}/thread/{{reply.replyrefnum}}#{{reply.refnum}}">No.</a>
        <span class="dopen">{{reply.refnum}}</span>
      </span>

      % if reply.image:
        <div class="file">
          <div class="fileText">File:
            <a href="{{basename}}/{{reply.image}}" title="{{reply.filename}}">
            % if len(reply.filename.split(".")[0]) > 20:
            {{reply.filename[:20]}}(...).{{reply.filename.split(".")[-1]}}
            % else:
            {{reply.filename}}
            % end
            </a>
            % if not is_video(reply.filename):
              [<a href="{{basename}}https://www.google.com/searchbyimage?image_url=http://192.168.1.104/{{reply.image}}"class="gsearch">S</a>]
            % end
            % if not is_video(reply.filename):
              ({{image_size(reply.image)}})
            % end
          </div>
          <a class="fileThumb">
          % if is_video(reply.filename):
            <video class="Reply-video" width="250" height="250">
              <source src="{{basename}}/{{reply.image}}" type="video/{{reply.image[-3:]}}">
              Your browser does not support the video tag.
            </video>
          % else:
            <img class="Reply-image" src="{{basename}}/uploads/{{board_name}}/{{reply.refnum}}s.jpg">
          % end
          </a>
        </div>
      % end
    </div>

    <blockquote class="postMessage">
      % include('thread_text', thread=reply)
    </blockquote>
    <div style="clear:both;"></div>

    <div>
      % replylist = loads(reply.replylist)
      % if replylist:
        <div class="Reply-list">
          <span class="reps">Replies:</span>
          % for i in range(len(replylist)):
            <a href="{{basename}}/{{board_name}}/thread/{{reply.replyrefnum}}#{{replylist[i]}}" class="reps reference">>>{{replylist[i]}}</a>
          % end
        </div>
      % end
    </div>

  </div>
</div>
