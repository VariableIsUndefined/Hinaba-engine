% rebase('base', title="New PM")

<head>
  <link rel="stylesheet" href="{{basename}}/static/css/style.css">
</head>

<body class="is-moderator active-page">
  <header><h1>New PM for {{ reciever.ip }}</h1><div class="subtitle"><p><a href="{{basename}}/admin">Return to dashboard</a></p></div></header>
  <form action="{{ basename }}/admin/new_PM/{{ reciever.id }}" method="post">
    <table>
      <tbody>
        <tr><th>To</th><td><a href="{{ basename }}/admin/staff/{{ reciever.id }}">{{ reciever.ip }}</a></td></tr>
        <tr><th>Message</th><td><textarea name="message" rows="10" cols="40">{{ reply }}</textarea></td></tr>
      </tbody>
    </table>
    <p style="text-align:center"><input type="submit" value="Send message"></p>
  </form>

</body>