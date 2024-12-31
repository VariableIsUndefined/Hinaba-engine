const markdownParser = (text) => {
  const toHTML = text
  .replace(/\*\*(.*)\*\*/gim, '<b>$1</b>') // bold text
  .replace(/\*(.*)\*/gim, '<i>$1</i>') // italic text
  .replace(/\_\_(.*)\_\_/gim, '<u>$1</u>') // underlined text
  .replace(/\%\%(.*)\%\%/gim, '<s>$1</s>') // spoiler text
  .replace(/\`(.*)\`/gim, '<code>$1</code>') // spoiler text

  return toHTML.trim()
}

function markdown(){

  var text_thread = $( ".postMessage" ).toArray();

  for ( i = 0; i < text_thread.length; i++) {

    thread_text = $(text_thread[i]).html().replace(/\s+/g, ' ');

    formated_text = markdownParser(thread_text).autoLink();

    $(text_thread[i]).html(formated_text);

  }

}

function card_text(){

  var text_thread = $( ".teaser" ).toArray();

  for ( i = 0; i < text_thread.length; i++) {

    thread_text = $(text_thread[i]).html().replace(/\s+/g, ' ');

    formated_text = markdownParser(thread_text);

    $(text_thread[i]).html(formated_text);

  }
}

$( document ).ready(function() {

  markdown();

  card_text();

});
