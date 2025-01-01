% rebase('base', title="Administration")
% from models import Board

<head>
  <link rel="stylesheet" href="{{basename}}/static/css/staff_yotsubanew.css">
</head>

% include('menu')

<div class="boardBanner"><div class="boardTitle">Mods</div></div>

<form class="banForm" action="{{basename}}/new_mod" method="POST">
	<input name="ip" type="text" placeholder="ip">
  <select name="board">
    % for board in Board.select():
    <option value="{{board.name}}">{{board.name}}</option>
    % end
  </select>
  Can Capcode: <input type="checkbox" name="can_capcode" size="35">
  Capcode: <input type="text" name="capcode">
	<input type="submit" value="Add">
</form>


<table class="Reports" id="mods">
  <thead>
    <tr>
      <th>IP</th>
      <td>Mod</td>
      <td>Role</td>
      <td>Can Capcode</td>
      <td>Capcode</td>
      <td></td>
    </tr>
  </thead>  
  <tbody>
    % for mod in mods:
      <tr>
      	<td>{{mod.ip}}</td>
      	<td>{{mod.mod.replace("::", ", ").strip(':')}}</td>
        <td>
          <form action="{{basename}}/mod" method="POST">
            <select name="board">
              % for board in Board.select():
              <option value="{{board.name}}">{{board.name}}</option>
              % end
            </select>
	          <input type="text" name="ip" value="{{mod.ip}}" hidden>
            <input type="submit" name="rm" value="Remove">
            <input type="submit" name="add" value="Add">
            </td>
            <td>
              <input type="checkbox" name="can_capcode" checked="{{"checked" if mod.can_capcode else ""}}" size="35">
            </td>
            <td>
              <input type="text" name="capcode" value="{{mod.capcode}}">
            </td>
            <td>
              <input type="submit" name="rmall" value="Remove all">
          </form>
        </td>
      </tr>
    % end
  </tbody>
</table>

<div class="boardBanner"><div class="boardTitle">Categories</div></div>

<form class="banForm" action="{{basename}}/add_category" method="POST" enctype="multipart/form-data">
	<input name="name" type="text" placeholder="category name" required>
	<input type="submit" value="Add">
</form>

<table class="Reports">
  <thead>
    <tr>
      <td>Id</td>
      <td>Category</td>
      <td></td>
    </tr>
  </thead>
  <tbody>
    % for category in categories:
      <tr>
        <td>{{category.id}}</td>
        <td>{{category.name}}</td>
        <td>
          <form action="{{basename}}/del_category/{{category.name}}" method="POST">	
            <input type="submit" value="Delete"></input>
          </form>
        </td>
      </tr>
    % end
  </tbody>
</table>

<div class="boardBanner"><div class="boardTitle">Boards</div></div>

<form class="banForm" action="{{basename}}/add_board" method="POST" enctype="multipart/form-data">
	<input name="name" type="text" placeholder="board name" required>
	<input name="title" type="text" placeholder="board title" required>
	NSFW: <input name="nsfw" type="checkbox" placeholder="board title">
  <select name="category">
    <option selected disabled>Category:</option>
    % for category in categories:
      <option value="{{category.name}}">{{category.name}}</option>   
    % end
  </select>
	<input type="submit" value="Add">
</form>
<table class="Reports">
  <thead>
    <tr>
      <td>Board</td>
      <td>Title</td>
      <td>Category</td>
      <td id="view-field"></td>
    </tr>
  </thead>
  <tbody>
    % for board in boards:
      <tr>
        <td>{{board.name}}</td>
        <td>{{board.title}}</td>
        <td>{{board.category}}</td>
        <td>
          <form action="{{basename}}/del_board/{{board.name}}" method="POST">	
            <input type="submit" value="Delete"></input>
          </form>
        </td>
      </tr>
    % end
  </tbody>
</table>

<form action="{{basename}}/logout" method="POST" style="text-align: center;margin-top:10px;">
  <input type="submit" value="Log out">
</form>
