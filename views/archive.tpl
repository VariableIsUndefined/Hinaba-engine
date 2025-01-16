% rebase('base', title=f"/{board_name}/ - Archive - {board_title}")
% from models import Post
% from bottle import ConfigDict
% from json import loads
% config = ConfigDict()
% config.load_config('imageboard.conf')
% styles = loads(config['style.styles'])

<head>
  % if style == "Yotsuba": 
    <link rel="stylesheet" href="{{basename}}/static/css/styles/yotsubanew.css">
  % elif style == "Yotsuba B":
    <link rel="stylesheet" href="{{basename}}/static/css/styles/yotsubluenew.css">
  % elif style == "Futaba":
    <link rel="stylesheet" href="{{basename}}/static/css/styles/futabanew.css">
  % elif style == "Burichan":
    <link rel="stylesheet" href="{{basename}}/static/css/styles/burichannew.css">
  % elif style == "Tommorow":
    <link rel="stylesheet" href="{{basename}}/static/css/styles/tommorow.css">
  % elif style == "Photon":
    <link rel="stylesheet" href="{{basename}}/static/css/styles/photon.css">
  % end
  <noscript><style type="text/css">#postForm { display: table !important; }#g-recaptcha { display: none; }</style></noscript>
</head>

<body class="is_arclist board_{{board_name}} yotsuba_new ws">
  % include('menu')
  <span id="id_css"></span>
  <div class="boardBanner">
  
    % if banner:
      <img alt="banner" src="{{basename}}/{{banner}}"  style="max-width: 30%;">
    % end

    <div class="boardTitle"> /{{board_name}}/ - {{board_title}} </div>
    % if board.nsfw:
      <div class="boardTitle"> [<span class="nsfw">NSFW</span>] </div>
    % end
  </div>

  <hr class="desktop">

  <div class="navLinks desktop">
    [<a href="{{basename}}/{{board_name}}" accesskey="{{board_name}}">Return</a>]
    [<a href="{{basename}}/{{board_name}}/catalog">Catalog</a>]
    [<a href="#bottom">Bottom</a>]
  </div>
  
  <hr>

  % archived_threads = Post.select().where(Post.board == board, Post.is_reply == False, Post.is_archived == True)

  % if archived_threads:
  <h4 class="center">Displaying {{archived_threads.count()}} expired threads from the past 7 days</h4>
  <table id="arc-list" class="flashListing">
    <thead>
      <tr>
        <td class="postblock">No.</td>
        <td class="postblock">Excerpt</td>
        <td class="postblock"></td>
        % if f':{board_name}:' in current_user.mod:
        <td class="postblock"></td>
        % end
      </tr>
    </thead>

    <tbody>
      % for thread in archived_threads:
        <tr>
          <td>{{thread.refnum}}</td>
          <td class="teaser-col">{{thread.title}}</td>
          <td>
            [<a class="quotelink" href="{{basename}}/{{board_name}}/thread/{{thread.refnum}}">View</a>]
          </td>
          % if f':{board_name}:' in current_user.mod:
            <td>
              [<a class="quotelink" href="{{basename}}/{{board_name}}/unarchive/{{thread.refnum}}">Unarchive</a>]
            </td>
          % end
        </tr>
      % end
    </tbody>
  </table>
  % else:
    <h4 class="center">No archived threads</h4>
  % end

  <hr>

  <div class="bottomCtrl">
    <div id="styleSwitcher">
      Style: <select id="styleSelector" onchange="changeStyle(this.value)">>
        % for s in styles:
          % if style == s:
            <option value="{{s}}" selected>{{s}}</option>
          % else:
            <option value="{{s}}">{{s}}</option>
          % end
        % end
      </select>
    </div>
  </div>
  
  <div style="clear:both;"></div>
  
  % include('menu')

  <div style="clear:both;"></div>

  <div id="absbot" class="absBotText">
  % include('foot')
  </div>

  <div id="bottom"></div>
</body>