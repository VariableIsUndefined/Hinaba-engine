% from models import Board
<div id="boardNavDesktop" class="desktop">
  <div class="boardList">
    % if Board.select().count() > 0:
      [
        % for board in Board.select():
          <a href="{{basename}}/{{board.name}}/" title="{{board.title}}">{{board.name}}</a>
          % if Board.select()[-1].name != board.name:
          /
          % end
        % end
      ]
    % end
  </div>

  <span id="navtopright">
    [<a href="{{basename}}/">Home</a>]
    % if defined('board_name'):
      % if f':{board_name}:' in current_user.mod:
        [<a href="{{basename}}/{{board_name}}/mod">Mod</a>]
      % end
    % end
  </span>
</div>
