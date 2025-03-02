% rebase('base', title="PM Inbox")
% from models import PrivateMessage, Anon
% unread_messages = PrivateMessage.select().where(PrivateMessage.to == current_user.id, PrivateMessage.unread == True)
<head>
  <link rel="stylesheet" href="{{basename}}/static/css/style.css">
</head>

<body class="is-moderator active-page">
  <header><h1>PM inbox
  % if unread_messages.exists():
    ({{ unread_messages.count() }} unread)
  % else:
    (0 unread)
  % end
  </h1><div class="subtitle"><p><a href="{{basename}}/admin">Return to dashboard</a></p></div></header>

  <table class="modlog">
    <tbody>
      <tr><th>ID</th><th>From</th><th>Date</th><th>Message snippet</th></tr>
      % for message in PrivateMessage.select().where(PrivateMessage.to == current_user.id).order_by(PrivateMessage.unread.desc(), PrivateMessage.time.desc()):
      % sender = Anon.select().where(Anon.id == message.sender).get()
      <tr>
        <td class="minimal"><a href="{{ basename }}/admin/PM/{{ message.id }}">{{ message.id }}</a></td>
        <td class="minimal"><a href="{{ basename }}/admin/new_PM/{{ message.sender }}">{{ sender.ip }}</a></td>
        <td class="minimal">{{ message.time.strftime("%m/%d/%y (%a) %H:%M:%S") }}</td>
        <td><a href="{{ basename }}/admin/PM/{{ message.id }}"><em>{{ message.message }}</em></a></td>
      </tr>
      % end
    </tbody>
  </table>
</body>