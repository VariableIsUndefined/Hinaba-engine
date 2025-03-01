% rebase('base', title="News")
% from models import News

<head>
  <link rel="stylesheet" href="{{basename}}/static/css/style.css">
</head>

<body class="is-moderator active-page">
    <header><h1>News</h1><div class="subtitle"><p><a href="?/">Return to dashboard</a></p></div></header>
    <fieldset>
      <legend>New post</legend>
      <form style="margin:0" action="{{basename}}/admin/edit_news" method="post">
        <table>
          <tbody>
            <tr><th><label for="name">Name</label></th><td><input type="text" size="55" name="name" id="name" value=""></td></tr>
            <tr><th><label for="subject">Subject</label></th><td><input type="text" size="55" name="subject" id="subject"></td></tr>
            <tr><th><label for="body">Body</label></th><td><textarea name="body" id="body" style="width:100%;height:100px"></textarea></td></tr>
          </tbody>
        </table>
      <p style="text-align:center"><input type="submit" value="Post news entry"></p>
      </form>
    </fieldset>

     % for neww in News.select().order_by(News.id.desc()):
       <div class="ban">
         <h2 id="{{neww.id}}"><small class="unimportant"><a href="#{{neww.id}}">#</a></small> {{neww.subject}} <small class="unimportant">— by {{neww.name}} at {{neww.time.strftime("%m/%d/%y (%a) %H:%M:%S")}} </small></h2>
         <p>{{neww.body}}</p>
       </div>
     % end
</body>