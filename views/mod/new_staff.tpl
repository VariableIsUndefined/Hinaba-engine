% rebase('base', title="New staff")
% from models import Board

<head>
  <link rel="stylesheet" href="{{basename}}/static/css/style.css">
</head>

<body class="is-moderator active-page">
  <header><h1>New user</h1><div class="subtitle"><p><a href="{{basename}}/admin">Return to dashboard</a></p></div></header>
  <form action="{{basename}}/admin/staff/new" method="post">
    <table>
      <tbody>
        <tr><th>IP</th><td><input size="20" maxlength="18" type="text" name="ip" value="" autocomplete="off"></td></tr>
        <tr><th>Can Capcode</th><td><input size="25" name="can_capcode" type="checkbox" autocomplete="off"></td></tr>
        <tr><th>Capcode</th><td><input size="20" maxlength="30" type="text" name="capcode" placeholder="## Moderator" autocomplete="off"></td></tr>
        <tr>
          <th>Boards</th>
          <td>
            <select name="board">
              % for board in Board.select():
                <option value="{{board.name}}">{{board.name}}</option>
              % end
            </select>
          </td>
        </tr>
      </tbody>
    </table>
    <ul style="padding:0;text-align:center;list-style:none"><li><input type="submit" value="Create user"></li></ul>
  </form>
</body>