% rebase('base', title=f"/{board_name}/ - {board_title}")
<body class="is_index board_{{board_name}} yotsuba_new ws">
  <span id="id_css"></span>
  <div class="boardBanner">
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

  <hr>

  <div id="ctrl-top" class="desktop">
  [<a class="{{basename}}/{{board_name}}/catalog">Catalog</a>]
  </div>

  <hr>
  
  <div id="board">
    <form id="delform" action="{{basename}}/{{board_name}}/delete" method="POST">
    % for thread in threads:
    % include('thread', thread=thread, board_name=board_name, board=board)
    % end
  </div>

  <div style="clear:both;"></div>

  <hr>

  % include('pagination', current_page=current_page, board_name=board_name)
  % include('bottom')
  
  <div style="clear:both;"></div>
  
  % include('menu')

  <div style="clear:both;"></div>

  <div id="absbot" class="absBotText">
  % include('foot')
  </div>
</body>