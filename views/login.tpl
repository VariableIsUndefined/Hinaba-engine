% rebase('base', title="Login")

<head>
    <link rel="stylesheet" href="{{basename}}/static/css/style.css">
</head>

<body>
    <title>Login</title>
    <header>
     <h1>Login</h1>
     <div class="subtitle"></div>
    </header>

    % if error:
    <h2 style="text-align:center">{{ error }}</h2>
    % end

    <form class="Login" action="{{basename}}/login" method="POST">
      <table style="margin-top:25px;">
        <tbody>
          <tr><th>Password</th><td><input type="password" name="password" size="20" maxlength="30"><br><br></td></tr>
          <tr><td></td><td><input type="submit" name="login" value="Continue"></td></tr>
        </tbody>
      </table>
    </form>
</body>
