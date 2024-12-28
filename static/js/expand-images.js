function expand_images(){
  thread_width = $(this).parents( ".thread" ).width();
  image_full = $(this).parent().parent().find(".fileText").children().attr("href");

  image_small = image_full.split(".")[0] + "s.jpg";

  if ($(this).attr("src") == image_small){
    $(this).attr("src", image_full);
    $(this).addClass("full-image");
    $(this).css("max-width", thread_width / 2);
  } 
  else {
    $(this).attr("src", image_small);
    $(this).removeClass("full-image");
    $(this).css("max-width", "");

  }
  
}

function expand_image_reply(){
  thread_width = $(this).parents( ".thread" ).width();

  image_full = $(this).parent().parent().find(".fileText").children("a").attr("href");

  image_small = image_full.split(".")[0] + "s.jpg";

  if ($(this).attr("src") == image_small){

    $(this).attr("src", image_full);
    $(this).addClass("full-image");
    $(this).css("max-width", thread_width);
    $(this).css("margin-right", 0);

  } 
  else {

    $(this).attr("src", image_small);
    $(this).removeClass("full-image");
    $(this).css("max-width", "");
    $(this).css("margin-right", 5);

  }
}

$( document ).ready(function() {

  $("#board").off("click").on("click", ".Thread-image", expand_images)
  $("#board").on("click", ".Reply-image", expand_image_reply)

});
