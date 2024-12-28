
function window_reply(board_name, thread_refnum, post_refnum){
  var maxlength = $(document).find("#texta1").attr("maxlength");
  var maxsize = $(document).find("#max-size").text()
  var chars = post_refnum.length + 3

  $("#quickReply").remove();

  $("body").append(
    '<div id="quickReply" class="extPanel reply" data-trackpos="QR-position"> <div id="qrHeader" class="drag postblock">Reply to thread #' + post_refnum +
    '<span class="dclose">X</span></div> <form name="qrPost" method="POST" action="/' + board_name +
    '/' + thread_refnum + '" enctype="multipart/form-data"> <div id="qrForm"> <table> <tbody> <tr> <td>Name</td> <td> ' +
    '<input type="text" name="author"> </td> </tr> <tr> <td>Comment</td> <td><textarea maxlength="' + maxlength +
    '" id="texta2" rows="6" name="content" required>>>' + post_refnum +
    '\n</textarea><br><small style="opacity:.5;">Max message length: <span id="count2">' +
    chars + '</span>/' + maxlength +
    '</small></td> </tr><tr><td>File</td><td><small>' + maxsize +
    '</small><br><input type="file" name="upload"> <input type="submit" value="Reply"></td> </tr> </tbody> </table> </div> </form> </div>'
  );

  var window_width = $("#quickReply").width();

  $("#quickReply").css({
    "position": "absolute",
    "left": ($(window).width() - window_width - 8) + "px",
    "top": ($(window).height() / 2 - $(window).height() / 4) + "px"
  });

  $("#quickReply").attr("for", thread_refnum)
}

function open_window()
{
  var basename = document.URL.split("/").slice(3, 4);
  var board_name = document.URL.split("/").slice(4, 5);
  if (board_name == "")
    board_name = basename
  else
    board_name = basename +"/"+ board_name

  var thread_refnum = $(this).parents(".thread")
  var post_refnum = $(this).text()

  if (Boolean($("#quickReply").length))
  {
    var win = $("#quickReply")
    if ( win.attr("for") == thread_refnum )
    {
      var a = win.find("textarea").val() + ">>" + post_refnum + "\n";
      win.find("textarea").val(a);
      win.find("#count2").text(win.find("textarea").val().length);
      win.find("textarea").focus();
    }
    else {
      $("#quickReply").remove()
      window_reply(board_name, thread_refnum, post_refnum)
    }
  }
  else {
    window_reply(board_name, thread_refnum, post_refnum)
  }

  // Make the DIV element draggable:
  dragElement(document.getElementById("quickReply"));

  function dragElement(elmnt) {
    var pos1 = 0, pos2 = 0, pos3 = 0, pos4 = 0;
    if (document.getElementById("qrHeader")) {
      // if present, the header is where you move the DIV from:
      document.getElementById("qrHeader").onmousedown = dragMouseDown;
    } else {
      // otherwise, move the DIV from anywhere inside the DIV:
      elmnt.onmousedown = dragMouseDown;
    }

    function dragMouseDown(e) {
      e = e || window.event;
      e.preventDefault();
      // get the mouse cursor position at startup:
      pos3 = e.clientX;
      pos4 = e.clientY;
      document.onmouseup = closeDragElement;
      // call a function whenever the cursor moves:
      document.onmousemove = elementDrag;
    }

    function elementDrag(e) {
      e = e || window.event;
      e.preventDefault();
      // calculate the new cursor position:
      pos1 = pos3 - e.clientX;
      pos2 = pos4 - e.clientY;
      pos3 = e.clientX;
      pos4 = e.clientY;
      // set the element's new position:

      if ( elmnt.offsetTop - pos2 <= 0 ) return
      if ( elmnt.offsetLeft - pos1 <= 0 ) return

      if ( elmnt.offsetTop - pos2 >= $(window).height() - $(elmnt).height()) return

      if ( elmnt.offsetLeft - pos1 >= $(window).width() - $(elmnt).width() - 8) return

      elmnt.style.top = (elmnt.offsetTop - pos2) + "px";
      elmnt.style.left = (elmnt.offsetLeft - pos1) + "px";
    }

    function closeDragElement() {
      // stop moving when mouse button is released:
      document.onmouseup = null;
      document.onmousemove = null;
    }
  }

}

$( document ).ready(function() {

  console.log("Quick reply loaded")
  $("body").on("click", ".dclose", function() {
    $("#quickReply").remove();
  });

  $("#board").on("click", ".dopen", open_window);

})
