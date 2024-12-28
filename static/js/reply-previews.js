function show_preview(){

    var href = $(this).attr("href");
    var id = $(this).text().replace(/[>>\D]/g, '');

    var is_thread = href.split("/").slice(-1)[0].includes("#")

    elmnt = this;

    $(this).after('<div class="postPreview"><span style="text-align:center;">[...]</span></div>');

    jQuery.ajax({
      url: href,
      method: 'GET',
      success: function(data){
        if (is_thread){
          preview = $(data).find("#" + id).find(".postMessage");
          preview.find(".hide-reply, .gsearch").detach();
          var thread = preview.html().replace(/\[\]/g, "");
          preview = markdown_parser(thread).autoLink();
        }
        else
        {
          preview = $(data).find("#" + id);
          preview.find(".Reply-list, .postInfo .fileThumb").detach();
  
          var postInfo = preview.find(".postInfo");
          postInfo.css("margin", 0);
          preview.find(".postMessage").before(postInfo);
          preview.find("button, .hide-thread, .gsearch").detach();
  
          var thread = preview.html().replace(/\[\]/g, "");
          preview = thread;
        }
        $(elmnt).siblings(".postPreview").html(preview);
      }
    });
}

$( document ).ready(function(){

  // Подключаем событие наведения мыши на ссылки с классом .reference
  $("#container").on("mouseenter", ".reference", show_preview);

  // Удаляем превью при выходе мыши
  $("#container").on("mouseleave", ".reference", function() {
    $(this).siblings(".postPreview").detach();
  });

});
