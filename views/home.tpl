% from models import Post, Board
% from utils import get_size_format, short_msg, is_video
% rebase('base', title=title)
<div id="doc">
  <h1 class="Title">{{title}}</h1>
  <link rel="stylesheet" href="{{basename}}/static/css/frontpage.css">

  <div id="bd">
    <div class="box-outer" id="announce">
      <div class="box-inner">
        <div class="boxbar">
          <h2 class="Boards-title">What is {{title}}?</h2>
        </div>
        <div class="boxcontent">
          {{welcome_message}}
        </div>
      </div>
    </div>

    <div class="box-outer top-box" id="boards">
      <div class="boxbar"> <h2>Boards</h2> </div>
      <div class="box-inner">
        <div id=class="boxcontent">
          % if Board.select().count() == 0:
            No boards have been created.
          % end
          % for board in Board.select():
            <a href="{{basename}}/{{board.name}}/" style="display:inline-block;">/{{board.name}}/ - {{board.title}}</a>
          % end
        </div>
      </div>
    </div>

    <div class="box-outer top-box" id="site-stats">
      <div class="box-inner">
        <div class="boxbar">
          <h2>Stats</h2>
        </div>
        <div class="boxcontent">
          <div class="stat-cell"><b>Number of messages:</b> {{number_of_messages}}</div>
          <div class="stat-cell"><b>Active content:</b> {{get_size_format(active_content_size)}}</div>
        </div>
      </div>
    </div>
    
    <div id="ft">
      % include('foot')
    </div>
    
  </div>
</div>
