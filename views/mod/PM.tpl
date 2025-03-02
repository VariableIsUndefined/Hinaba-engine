% rebase('base', title=f"Private message - #{message.id}")

<head>
  <link rel="stylesheet" href="{{basename}}/static/css/style.css">
</head>

<body class="is-moderator active-page">
  <header><h1>Private message – #{{ message.id }}</h1><div class="subtitle"><p><a href="{{ basename }}/admin">Return to dashboard</a></p></div></header>
  <form action="{{basename}}/admin/PM/{{message.id}}" method="post">
    <table>
      <tbody>
        <tr><th>From</th><td><a href="{{basename}}/admin/new_PM/{{message.sender}}">admin</a></td></tr>
        <tr><th>Date</th><td>{{ message.time.strftime("%m/%d/%y (%a) %H:%M:%S") }}</small></td></tr>
        <tr><th>Message</th><td>{{ message.message }}</td></tr>
      </tbody>
    </table>
    <ul style="list-style:none;text-align:center;padding:0">
      <li style="padding:5px 0"><input type="submit" name="delete" value="Delete forever"></li>
      <li style="padding:5px 0"><a href="{{ basename }}/admin/PM/{{ message.id }}/reply">Reply with quote</a></li>
    </ul>
  </form>
</body>