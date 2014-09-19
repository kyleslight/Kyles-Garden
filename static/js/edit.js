$(document).ready(function(){
  	enable_tab();
	Preview.Init();
	Preview.Update();

	$(".articlesubmit").on('click', function(){
		var theform = document.getElementById("editdata");
		var previewcon = document.getElementById("previewtextcontainer");
		previewcon.innerHTML = get_preview_content();
		console.log(previewcon.innerHTML);
		theform.submit();
	})
})

function enable_tab(){
	$(document).delegate('#writing', 'keydown', function(e) {
  		var keyCode = e.keyCode || e.which;

	  	if (keyCode == 9) {
	    	e.preventDefault();
	    	var start = $(this).get(0).selectionStart;
	    	var end = $(this).get(0).selectionEnd;

	    // set textarea value to: text before caret + tab + text after caret
	    	$(this).val($(this).val().substring(0, start)
	                + "\t"
	                + $(this).val().substring(end));

	    // put caret at right position again
	    	$(this).get(0).selectionStart =
	    	$(this).get(0).selectionEnd = start + 1;
	  	}
	});

}

function highlight_code(){
	$('#previewbuffer code, #preview code').each(function(i, block) {
    	hljs.highlightBlock(block);
  	});
}

function get_preview_content(){
	var content = Preview.buffer.innerHTML;
	return content;
}