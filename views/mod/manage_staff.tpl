% rebase('base', title="Manage staff")
% from models import Staff
% total_users = Staff.select().count()

<head>
  <link rel="stylesheet" href="{{basename}}/static/css/style.css">
</head>

<body class="is-moderator active-page">
    <header><h1>Manage staff ({{total_users}})</h1><div class="subtitle"><p><a href="{{basename}}/admin">Return to dashboard</a></p></div></header>
    <table class="modlog" style="width:auto">
      <tbody>
        <tr><th>ID</th><th>Username</th><th>Type</th><th>Boards</th><th>Can Capcode</th><th>Capcode</th><th>...</th></tr>
        % for staff in Staff.select():
          <tr>
            <td><small>{{staff.id}}</small></td>
            <td><small>{{staff.username}}</small></td>
            <td>{{staff.type}}</td>
            <td>{{staff.anon.mod.replace("::", ", ").strip(':')}}</td>
            <td>{{staff.anon.can_capcode}}</td>
            <td>{{staff.anon.capcode}}</td>
            <td>
              <a class="unimportant" style="margin-left:5px;float:right" href="{{basename}}/admin/log:{{staff.username}}">[log]</a>
              <a class="unimportant" style="margin-left:5px;float:right"  href="{{basename}}/admin/staff/{{staff.id}}">[edit]</a>
              <a class="unimportant" style="margin-left:5px;float:right" href="{{basename}}/admin/new_PM/{{staff.id}}">[PM]</a>
            </td>
          </tr>
        % end
      </tbody>
    </table>
    <p style="text-align:center"><a href="{{basename}}/admin/staff/new">Create a new staff</a></p>
</body>