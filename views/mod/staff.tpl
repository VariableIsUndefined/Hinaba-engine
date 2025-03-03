% rebase('base', title="Edit staff")
% from models import Board
% from functions import has_permissions

<head>
  <link rel="stylesheet" href="{{basename}}/static/css/style.css">
</head>

<body class="is-moderator active-page">
  <header><h1>Edit staff - {{staff.username}}</h1><div class="subtitle"><p><a href="?/">Return to dashboard</a></p></div></header>
  <form action="{{basename}}/admin/staff/{{staff.id}}" method="post">
    <table>
      <tbody>
        <tr><th>IP</th><td><input readonly size="20" maxlength="30" type="text" name="ip" value="{{anon.ip}}" autocomplete="off"></td></tr>
        <tr><th>Username</th><td><input size="20" maxlength="30" type="text" name="username" value="{{staff.username}}" autocomplete="off"></td></tr>
        <tr><th>Password <small style="font-weight:normal">(new; optional)</small></th><td><input size="20" maxlength="30" type="password" name="password" value="" autocomplete="off"></td></tr>
        <tr><th>Can Capcode (Currently: {{anon.can_capcode}})</th><td><input size="25" name="can_capcode" type="checkbox" autocomplete="off"></td></tr>
        <tr><th>Capcode</th><td><input size="20" maxlength="30" type="text" name="capcode" value="{{anon.capcode}}" autocomplete="off"></td></tr>
        <tr><th>Boards</th><td>{{anon.mod.replace("::", ", ").strip(':')}}</td></tr>
        <tr>
          <th>Select board</th>
          <td>
            <select name="board">
              % for board in Board.select():
                <option value="{{board.name}}">{{board.name}}</option>
              % end
            </select>
            <input type="submit" name="add" value="Add to">
            <input type="submit" name="rm" value="Remove from">
          </td>
        </tr>
      </tbody>
    </table>
    <ul style="padding:0;text-align:center;list-style:none">
       <li><input type="submit" value="Save changes"></li>
       % if has_permissions(staff_type, "deletestaff"):
       <li><input name="delete" onclick="return confirm('Are you sure you want to permanently delete this user?');" type="submit" value="Delete user"></li>
       % end
    </ul>
  </form>
</body>