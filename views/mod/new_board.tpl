% rebase('base', title="New board")
% from models import Board

<head>
  <link rel="stylesheet" href="{{basename}}/static/css/style.css">
</head>

<body class="is-moderator active-page">
    <header><h1>New board</h1><div class="subtitle"><p><a href="/admin">Return to dashboard</a></p></div></header>
    <form action="{{basename}}/admin/new-board" method="post">
      <table>
        <tbody>
          <tr><th>URI</th><td>/<input size="10" maxlength="255" type="text" name="uri" autocomplete="off">/</td></tr>
          <tr><th>Title</th><td><input size="25" type="text" name="title" value="" autocomplete="off"></td></tr>
          <tr><th>NSFW</th><td><input size="25" name="nsfw" type="checkbox" autocomplete="off"></td></tr>
        </tbody>
      </table>
      <ul style="padding:0;text-align:center;list-style:none"><li><input type="submit" value="Create board"></li></ul>
    </form>
</body>