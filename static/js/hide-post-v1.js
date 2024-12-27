function toggle_post_hide() {
    console.log("click hide btn")
}

$( document ).ready(function() {

    $("#container").on("click", ".hide-thread", toggle_post_hide)
  
});