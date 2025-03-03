% rebase('base', title="Dashboard")
% from models import Board, PrivateMessage
% from functions import has_permissions

% unread_messages = PrivateMessage.select().where(PrivateMessage.to == current_user.id, PrivateMessage.unread == True)
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
    <legend>Messages</legend>
    <ul>
      <li><a href="{{basename}}admin/edit_news">News</a></li>
      <li><a href="{{ basename }}/admin/inbox">PM inbox
       % if unread_messages.exists():
         <strong>({{ unread_messages.count() }} unread) </strong>
       % else:
           <strong>(0 unread) </strong>
       % end
       </a></li>
    </ul>
  </fieldset>

  <fieldset>
    <legend>Administration</legend>
    % if has_permissions(staff_type, "managestaff"):
    <li><a href="{{basename}}/admin/staff">Manage staff</a></li>
    % end
    % if has_permissions(staff_type, "modlog"):
    <li><a href="{{basename}}/admin/log">Moderation log</a></li>
    % end
  </fieldset>

  <fieldset><legend>User account</legend><ul><li><form action="{{basename}}/logout" method="POST"><input type="submit" value="Log out">
</form></li></ul></fieldset>
</body>