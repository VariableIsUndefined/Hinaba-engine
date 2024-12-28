% rebase('base', board_name=board_name, title=thread.title)
% from utils import image_size

<body class="is_index board_{{board_name}} yotsuba_new ws">
  <div class="boardBanner">
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

  <form id="delform" action="{{basename}}/{{board_name}}/delete" method="POST">
  <div id="board">
    <div style="clear:both;"></div>
    % include('thread', thread=thread)	
  </div>
  <hr>
  </form>

  <footer>
  % include('bottom')
  </footer>
</body>
