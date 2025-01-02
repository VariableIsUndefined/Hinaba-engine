% from models import Board

% rebase('base', title="FAQ - PyChan")

<head>
  <link rel="stylesheet" href="{{basename}}/static/css/yui.css">
  <link rel="stylesheet" href="{{basename}}/static/css/global.css">
  <link rel="stylesheet" href="{{basename}}/static/css/faq.css">
  <style type="text/css">
    .danbo-slot {
    width:728px;
    height:90px;
    margin:10px auto;
    overflow:hidden
    }
    @media only screen and (max-width:480px) {
    .danbo-slot {
      width:300px;
      height:250px
    }
    }
  </style>
</head>

<body>
  <div id="doc">
    <div id="hd">
      <div id="logo-fp">
        <a href="{{basename}}" title="Home"><img alt="pychan" src="https://upload.wikimedia.org/wikipedia/commons/thumb/f/f8/Python_logo_and_wordmark.svg/2560px-Python_logo_and_wordmark.svg.png" width="300" height="120"></a>
      </div>
    </div>
    <div class="box-outer top-box">
      <div class="box-inner">
        <div class="boxbar">
          <h2>Frequently Asked Questions</h2>
        </div>
        <div class="boxcontent">
          <p>{{faq}}</p>
        </div>
      </div>
    </div>
    <div class="yui-g">
      <div class="yui-u first">
        <div class="box-outer left-box">
          <div class="box-inner">
            <div class="boxbar"><h2>Questions</h2></div>
            <div class="boxcontent">
              <ul>
                <ul>
                  <li>
                    <strong><a href="#basics">Basics</a></strong>
                    <ul>
                      <li> </li>
                    </ul>
                  </li>
                </ul>
              </ul>
            </div>
          </div>
        </div>
      </div>
      <div class="yui-u">
        <div class="box-outer right-box">
          <div class="box-inner">
            <div class="boxbar"><h2><a name="basics">Basics</a></h2></div>
            <div class="boxcontent">
              <dl>
              </dl>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>

  <div id="ft">
    <ul>
      <li class="fill"></li>
      <li class="first"><a href="/">Home</a></li>
      <li><a href="/faq">FAQ</a></li>
      <li><a href="/rules">Rules</a></li>
    </ul>
    <br class="clear-bug">
    <div id="copyright">
    % include('foot')
    </div>
  </div>
  <div id="modal-bg"></div>
</body>