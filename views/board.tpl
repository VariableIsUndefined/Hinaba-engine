% rebase('base', title=f"/{board_name}/ - {board_title}")

% from bottle import ConfigDict
% from json import loads

% config = ConfigDict()
% config.load_config('imageboard.conf')
% int_boards = loads(config['app.int_boards'])

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

  % if (board_name in int_boards):
    <link rel="stylesheet" href="{{basename}}/static/css/flags.css">
  % end
</head>

<body class="is_index board_{{board_name}} yotsuba_new ws">
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

  <hr class="abovePostForm">

  <form class="Formulario" method="POST" action="{{basename}}/{{board_name}}/" enctype="multipart/form-data">
    <table class="postForm" id="postForm" style="display: table;">
      <tbody>
        <tr data-type="Name">
          <td>Name</td>
          <td>
            <input type="text" name="author">
          </td>
        </tr>

        % if current_user.can_capcode:
        <tr data-type="Capcode">
          <td>Capcode</td>
          <td>
            <input type="checkbox" name="capcode" value="on" checked="checked" size="35"> ({{current_user.capcode}})
          </td>
        </tr>
        % end

        <tr data-type="Email">
          <td>Email</td>
          <td>
            <input name="email" type="text" tabindex="2">
          </td>
        </tr>

        <tr data-type="Title">
          <td>Title</td>
          <td>
            <input type="text" name="title" required> <button id="btnPost">Post</button>
          </td>
        </tr>

        <tr data-type="Comment">
          <td>Comment</td>
          <td><textarea id="texta1" maxlength="{{maxlength}}" rows="6" name="content" required></textarea><br><small style="opacity:.5;">Max message length: <span id="count1">0</span>/{{maxlength}}</small></td>
        </tr>

        <tr data-type="File">
          <td>File</td>
          <td><small id="max-size">Max file size: {{max_file_size}}MB.</small><br><input type="file" name="upload" required></td>
        </tr>

        <tr class="rules">
          <td colspan="2">
            <ul class="rules">
              <li> Please read the Rules and FAQ before posting. </li>
            </ul>
          </td>
        </tr>
      </tbody>
    </table>
  </form>

  <div id="ctrl-top" class="desktop">
    <hr>
      <form action="{{basename}}/{{board_name}}/catalog" method="GET">
        <input name="search" type="text" id="search-box" placeholder="Search OPs…" />
        [<a href="{{basename}}/{{board_name}}/catalog">Catalog</a>]
        [<a href="{{basename}}/{{board_name}}/archive">Archive</a>]
      </form>
  </div>

  <hr>
  
  <div id="board">
    <form id="delform" action="{{basename}}/{{board_name}}/delete" method="POST">
    % for thread in threads:
    % include('thread', thread=thread, board_name=board_name, board=board)
    <div style="clear:both;"></div>
    <hr>
    % end
  </div>

  <div style="clear:both;"></div>

  % include('pagination', current_page=current_page, board_name=board_name)
  % include('bottom')
  
  <div style="clear:both;"></div>
  
  % include('menu')

  <div style="clear:both;"></div>

  <div id="absbot" class="absBotText">
  % include('foot')
  </div>
</body>