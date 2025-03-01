% rebase('base', title="Edit board")
% from models import Board

<head>
  <link rel="stylesheet" href="{{basename}}/static/css/style.css">
</head>

<body class="is-moderator active-page">
  <header><h1>Edit board: /{{board.name}}/</h1><div class="subtitle"><p><a href="/admin">Return to dashboard</a></p></div></header>
  <form action="{{basename}}/admin/edit/{{board.name}}" method="post">
    <table>
      <tbody>
        <tr><th>URI</th><td>/{{board.name}}/</td></tr>
        <tr><th>Title</th><td><input size="25" type="text" name="title" value="{{board.title}}" autocomplete="off"></td></tr>
        <tr><th>NSFW (Currently: {{board.nsfw}})</th><td><input size="25" name="nsfw" type="checkbox" autocomplete="off"></td></tr>
      </tbody>
    </table>

    <ul style="padding:0;text-align:center;list-style:none">
      <li><input type="submit" value="Save changes"></li>
      <li><input name="delete" onclick="return confirm('Are you sure you want to permanently delete this board?');" type="submit" value="Delete board"></li>
    </ul>
  </form>
</body>