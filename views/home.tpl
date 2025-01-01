% from models import Post, Board, Category
% from utils import get_size_format, short_msg, is_video
% rebase('base', title=title)
<head>
  <link rel="stylesheet" href="{{basename}}/static/css/frontpage.css">
</head>

<div id="doc">
  <div id="hd">
    <div id="logo-fp">
      <a href="{{basename}}" title="Home"><img alt="4chan" src="https://upload.wikimedia.org/wikipedia/commons/thumb/f/f8/Python_logo_and_wordmark.svg/2560px-Python_logo_and_wordmark.svg.png" width="500" height="120"></a>
    </div>
  </div>
  <h1 class="Title">{{title}}</h1>
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
      <div class="box-inner">
        <div class="boxbar"> <h2>Boards</h2> </div>
        <div class="boxcontent">
          % if Board.select().count() == 0:
            No boards have been created.
          % end
          % for category in Category.select():
            <div class="column">
              <h3 style="text-decoration: underline; display: inline;">{{category.name}}</h3>
              <ul>
                % for board in Board.select().where(Board.category == category.name):
                <li>
                  <a href="{{basename}}/{{board.name}}/" class="boardlink">{{board.title}}</a>
                </li>
                % end
              </ul>
              <div style="clear:both;"></div>
            </div>
          % end
        </div>
      </div>
      <div style="clear:both;"></div>
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
