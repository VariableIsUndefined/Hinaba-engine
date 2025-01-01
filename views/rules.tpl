% rebase('base', title="Rules")

<head>
  <link rel="stylesheet" href="{{basename}}/static/css/yui.css">
  <link rel="stylesheet" href="{{basename}}/static/css/global.css">
  <link rel="stylesheet" href="{{basename}}/static/css/rules.css">
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
          <h2>Rules</h2>
        </div>
        <div class="boxcontent">
          <p>{{rules}}</p>
        </div>
      </div>
    </div>
    <div class="yui-g">
      <div class="yui-u first">
        <div class="box-outer left-box">
          <div class="box-inner">
            <div class="boxbar"><h2>Boards</h2></div>
            <div class="boxcontent">
              <li><strong><a href="#global">Global Rules</a></strong></li>
              <li>
                <strong><a href="#imgboard">Image Boards</a></strong>
                <ul>
                </ul>
              </li>
            </div>
          </div>
        </div>
      </div>
      <div class="yui-u">
        <div class="box-outer right-box">
          <div class="box-inner">
            <div class="boxbar"><h2><a name="global">Global Rules</a></h2></div>
            <div class="boxcontent">
              <ol>
                <li id="global1">You will not upload, post, discuss, request, or link to anything that violates local or United States law.</li>
                <li id="global2">You will immediately cease and not continue to access the site if you are under the age of 18.</li>
                <li id="global3">You will not post any of the following outside of /b/:
                  <ol class="list-alpha">
                    <li>Troll posts</li>
                    <li>Racism</li>
                    <li>Anthropomorphic ("furry") pornography</li>
                    <li>Grotesque ("guro") images</li>
                    <li>Loli/shota pornography</li>
                    <li>Dubs or GET posts, including 'Roll for X' images</li>
                  </ol>
                </li>
                <li id="global4">You will not post or request personal information ("dox") or calls to invasion ("raids"). Inciting or participating in cross-board (intra-PyChan) raids is also not permitted.</li>
                <li id="global5">All boards that default to the Yotsuba B (blue) theme are to be considered "work safe". Violators may be temporarily banned and their posts removed. Note: Spoilered pornography or other "not safe for work" content is NOT allowed.</li>
                <li id="global6">The quality of posts is extremely important to this community. Contributors are encouraged to provide high-quality images and informative comments. Please refrain from posting the following:
                  <ol class="list-alpha">
                    <li>Irrelevant catchphrases or copypasta<br><small>Example: "What the fuck did you just fucking say about me, you little bitch?..."</small></li>
                    <li>Indecipherable text<br><small>Example: "lol u tk him 2da bar|?"</small></li>
                    <li>Irrelevant ASCII macros</li>
                    <li>Ironic shitposting<br><small>Example: "upboads for le funy maymay trollololololoxdxdxdxd~~!"</small></li>
                    <li>Gibberish text<br><small>Example: "l;kjdsfioasoiupwajnasdfa"</small></li>
                  </ol>
                </li>
                <li id="global7">Submitting false or misclassified reports, or otherwise abusing the reporting system may result in a ban. Replying to a thread stating that you've reported or "saged" it, or another post, is also not allowed.</li>
                <li id="global8">Complaining about PyChan (its policies, moderation, etc) on the imageboards may result in post deletion and a ban.</li>
                <li id="global9">Evading your ban will result in a permanent one. Instead, wait and <a href="/faq#banappeal" target="_blank">appeal</a> it!</li>
                <li id="global10">No spamming or flooding of any kind. No intentionally evading spam or post filters.</li>
                <li id="global11">Advertising (all forms) is not welcome—this includes any type of referral linking, "offers", soliciting, begging, stream threads, etc.</li>
                <li id="global12">Impersonating a PyChan administrator, moderator, or janitor is strictly forbidden.</li>
                <li id="global13">Do not use avatars or attach signatures to your posts.</li>
                <li id="global14">The use of scrapers, bots, or other automated posting or downloading scripts is prohibited. Users may also not post from proxies, VPNs, or Tor exit nodes.</li>
                <li id="global15">All pony/brony threads, images, Flashes, and avatars belong on /<a href="#mlp" title="Pony">mlp</a>/.</li>
                <li id="global16">All request threads for adult content belong on /<a href="{{basename}}/r/" title="Request">r</a>/, and all request threads for work-safe content belong on /<a href="{{basename}}/wsr/" title="Worksafe Requests">wsr</a>/, unless otherwise noted.</li>
                <li id="global17">Do not upload images containing additional data such as embedded sounds, documents, archives, etc.</li>
              </ol>
              <p>Global rules apply to all boards unless otherwise noted.<br><br>
              Remember: The use of PyChan is a privilege, not a right. The PyChan moderation team reserves the right to revoke access and remove content for any reason without notice.</p>
            </div>
          </div>
        </div>
        <div class="box-outer right-box">
          <div class="box-inner">
            <div class="boxbar"><h2><a name="imgboard">Image Boards</a></h2></div>
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