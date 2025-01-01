const markdownParser = (text) => {
  const rules = [
    { regex: /\*\*(.*)\*\*/gim, replacement: '<b>$1</b>' }, // bold text
    { regex: /\*(.*)\*/gim, replacement: '<i>$1</i>' }, // italic text
    { regex: /\_\_(.*)\_\_/gim, replacement: '<u>$1</u>' }, // underlined text
    { regex: /\%\%(.*)\%\%/gim, replacement: '<s>$1</s>' }, // spoiler text
    { regex: /\`(.*)\`/gim, replacement: '<code>$1</code>' }, // code text
  ];

  const toHTML = rules.reduce((acc, rule) => acc.replace(rule.regex, rule.replacement), text)

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