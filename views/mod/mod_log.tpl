% rebase('base', title="Moderation log")
% from models import ModLogs

<head>
  <link rel="stylesheet" href="{{basename}}/static/css/style.css">
</head>

<body class="is-moderator active-page">
  <header><h1>Moderation log</h1><div class="subtitle"><p><a href="?/">Return to dashboard</a></p></div></header>
  <table class="modlog">
    <tbody>
      <tr><th>IP address</th><th>Time</th><th>Board</th><th>Action</th></tr>
      % for log in ModLogs.select().order_by(ModLogs.time.desc()):
        <tr>
          <td class="minimal">{{log.ip}}</td>
          <td class="minimal"><span title="{{log.time.strftime("%m/%d/%y (%a) %H:%M:%S")}}">{{log.time.strftime("%m/%d/%y (%a) %H:%M:%S")}}</span></td>
          % if log.board:
          <td class="minimal"><a href="{{basename}}/{{log.board}}/">{{log.board}}</a></td>
          % else:
          <td class="minimal">-</td>
          % end
          <td>{{log.text}}</td>
        </tr>
      % end
    </tbody>
  </table>
</body>