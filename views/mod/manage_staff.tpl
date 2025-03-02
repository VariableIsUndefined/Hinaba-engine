% rebase('base', title="Manage staff")
% from models import Anon
% total_users = Anon.select().where(Anon.mod != "").count()

<head>
  <link rel="stylesheet" href="{{basename}}/static/css/style.css">
</head>

<body class="is-moderator active-page">
    <header><h1>Manage staff ({{total_users}})</h1><div class="subtitle"><p><a href="{{basename}}/admin">Return to dashboard</a></p></div></header>
    <table class="modlog" style="width:auto">
      <tbody>
        <tr><th>ID</th><th>IP</th><th>Type</th><th>Boards</th><th>Can Capcode</th><th>Capcode</th><th>...</th></tr>
        % for anon in Anon.select().where(Anon.mod != ""):
          <tr>
            <td><small>{{anon.id}}</small></td>
            <td><small>{{anon.ip}}</small></td>
            <td>Mod</td>
            <td>{{anon.mod.replace("::", ", ").strip(':')}}</td>
            <td>{{anon.can_capcode}}</td>
            <td>{{anon.capcode}}</td>
            <td>
              <a class="unimportant" style="margin-left:5px;float:right"  href="{{basename}}/admin/staff/{{anon.id}}">[edit]</a>
              <a class="unimportant" style="margin-left:5px;float:right" href="{{basename}}/admin/new_PM/{{anon.id}}">[PM]</a>
            </td>
          </tr>
        % end
      </tbody>
    </table>
    <p style="text-align:center"><a href="{{basename}}/admin/staff/new">Create a new staff</a></p>
</body>