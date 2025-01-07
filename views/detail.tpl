% rebase('base', board_name=board_name, title=thread.title)
% from utils import image_size

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
</head>

<body class="is_index board_{{board_name}} yotsuba_new ws">
  % include('menu')
  <div class="boardBanner">
    % if banner:
      <img alt="banner" src="{{basename}}/{{banner}}"  style="max-width: 30%;">
    % end

    % if thread.title:
      <div class="boardTitle"> {{thread.title}} </div>
    % else:
      <div class="boardTitle"> /{{board.name}}/ - {{board.title}} </div>
      % if board.nsfw:
        <div class="boardTitle"> [<span class="nsfw">NSFW</span>] </div>
      % end
    %end
  </div>
  <hr class="abovePostForm">
  <form class="Formulario" method="POST" action="{{basename}}/{{board_name}}/thread/{{thread.refnum}}" enctype="multipart/form-data">
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
        <tr data-type="Comment">
          <td>Comment</td>
          <td><textarea maxlength="{{maxlength}}" id="texta1" rows="6" name="content" required></textarea><br><small style="opacity:.5;">Max message length: <span id="count1">0</span>/{{maxlength}}</small></td>
        </tr>
        <tr data-type="File">
          <td>File</td>
          <td><small>Max file size: {{max_file_size}}MB.</small><br><input type="file" name="upload"> <input type="submit" value="Reply"></td>
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

  <hr>

  <div id="board">
    <form id="delform" action="{{basename}}/{{board_name}}/delete" method="POST">
    % include('thread', thread=thread)	
  </div>

  <div style="clear:both;"></div>
   
  <hr>

  % include('bottom')
  
  <div style="clear:both;"></div>
  
  % include('menu')

  <div style="clear:both;"></div>

  <div id="absbot" class="absBotText">
  % include('foot')
  </div>
</body>
