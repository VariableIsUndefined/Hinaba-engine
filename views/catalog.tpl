% rebase('base.tpl', board_name=board_name, title=f"Catalog of /{board_name}/")
% from models import Post, Board

<head>
  <link rel="stylesheet" href="{{basename}}/static/css/catalog_yotsubanew.css">
</head>

<body class="is_index board_{{board_name}} yotsuba_new ws">
  % include('menu')
  <div class="boardBanner">
    % if banner:
      <img alt="banner" src="{{basename}}/{{banner}}"  style="max-width: 30%;">
    % end
    
    <div class="boardTitle"> /{{board_name}}/ - {{board_title}} </div>
    % if board.nsfw:
      <div class="boardTitle"> [<span class="nsfw">NSFW</span>] </div>
    % end
  </div>
  <hr>
  <div id="content">
    <div id="ctrl">
      <div id="info">
        <span class="navLinks mobilebtn">
          <span class="btn-wrap"><a href="./" class="button">Return</a></span>
          <span class="btn-wrap"><a id="refresh-btn" href="./catalog" class="button">Refresh</a></span>
        </span>
      </div>
      <div id="settings" class="mobilebtn">
        <span style="display: inline;" id="qf-cnt"  data-built="1">
          <form action="{{basename}}/{{board_name}}/catalog" method="GET">
            [Seach] <input name="search" type="text" id="qf-box" wfd-id="id9" />
          </form>
        </span>
      </div>
      <div class="clear"></div>
    </div>

    <hr>

    <div id="threads" class="extended-small" contextmenu="ctxmenu-main">
      % for thread in threads:
      % file_ext = thread.filename.split(".")[1]
        <div id="thread-{{thread.id}}" class="thread">
          <a href="{{basename}}/{{board_name}}/thread/{{thread.refnum}}">
            % if  file_ext == "mp4" or file_ext == "webm":
              <video width="250">
              <source src="{{basename}}/uploads/{{board_name}}/{{thread.refnum}}.{{file_ext}}" type="video/{{file_ext}}">
              Your browser does not support the video tag.
              </video>
            % else:
              <img loading="lazy" alt class="thumb" src="{{basename}}/uploads/{{board_name}}/{{thread.refnum}}s.jpg">
            % end
          </a>

          <div title="(R)eplies / (I)mage Replies" class="meta">
            R: <b>{{board.posts.where(Post.replyrefnum == thread.refnum).count()}}</b>
            / I: <b>{{board.posts.where((Post.replyrefnum == thread.refnum) & (Post.image != "")).count()}}</b> 
          </div>

          <div class="teaser">
            % if thread.title:
            <b>{{thread.title}}:</b>
            % end
            {{thread.short_content}}        	
          </div>

        </div>
      % end
    </div>
  </div>

  <div style="clear:both;"></div>

  <hr>
  
  % include('menu')

  <div style="clear:both;"></div>

  <div id="absbot" class="absBotText">
  % include('foot')
  </div>
</body>