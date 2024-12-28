function show_preview(){

    var href = $(this).attr("href");
    var id = $(this).text().replace(/[>>\D]/g, '');

    var is_thread = href.split("/").slice(-1)[0].includes("#")

    var elmnt = this;

    $("#quote-preview").remove();

    $("body").append('<div id="quote-preview" class="post reply preview reveal-spoilers"><span style="text-align:center;">[...]</span></div>');

    var $preview = $("#quote-preview");

    $(elmnt).on("mousemove", function(e) {
        $preview.css({
            top: e.pageY + 10 + "px",
            left: e.pageX + 10 + "px"
        });
    });

    jQuery.ajax({
      url: href,
      method: 'GET',
      success: function(data){
        if (is_thread){
          preview = $(data).find("#" + id).find(".post");
          preview.find(".hide-reply").detach();
          preview.find(".gsearch").detach();
          var thread = preview.html().replace(/\[\]/g, "");
          preview = markdown_parser(thread).autoLink();
        }
        else
        {
          preview = $(data).find("#" + id);
          preview.find(".reply").detach();
  
          var postInfo = preview.find(".postInfo");
          postInfo.css("margin", 0);
          preview.find(".postMessage").before(postInfo);

          preview.find("button").detach();
          preview.find(".hide-thread").detach();
          preview.find(".gsearch").detach();

          var thread = preview.html().replace(/\[\]/g, "");
          preview = thread;
        }
        $preview.html(preview).fadeIn(200);
      }
    });
}

$( document ).ready(function(){

  $("#container").on("mouseenter", ".reference", show_preview);

  $("#container").on("mouseleave", ".reference", function() {
    $("#quote-preview").remove();
  });

});
