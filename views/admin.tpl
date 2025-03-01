% rebase('base', title="Dashboard")
% from models import Board

<head>
  <link rel="stylesheet" href="{{basename}}/static/css/style.css">
</head>

<body class="is-moderator active-page">
  <header><h1>Dashboard</h1><div class="subtitle"></div></header>

  <fieldset>
    <legend>Boards</legend>
    <ul>
      % for board in boards:
        <li>
           <a href="{{basename}}/{{board.name}}">/{{board.name}}/</a> - {{board.title}} <a href="admin/edit/{{board.name}}"><small>[edit]</small></a>
        </li>
      % end
      <li style="margin-top:15px"><a href="admin/new-board"><strong>Create new board</strong></a></li>
    </ul>
  </fieldset>

  <fieldset>
    <legend>Administration</legend>
    <li><a href="{{basename}}/admin/staff">Manage staff</a></li>
  </fieldset>

  <fieldset><legend>User account</legend><ul><li><form action="{{basename}}/logout" method="POST"><input type="submit" value="Log out">
</form></li></ul></fieldset>
</body>