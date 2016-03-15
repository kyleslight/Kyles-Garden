$(document).ready(function(){
  	enable_tab();
	Preview.Init();
	Preview.Update();

	$(".articlesubmit").on('click', function(){
		define_heading_id();
		// removeMathjaxBlocks();
		var theform = document.getElementById("editdata");
		var previewcon = document.getElementById("previewtextcontainer");
		previewcon.innerHTML = get_preview_content();
		$('#arttitle').val(get_title());
		var description = Preview.preview.children[2].innerHTML;
		if (Preview.preview.children[3]) {
			description = description + Preview.preview.children[3].innerHTML;
			if (Preview.preview.children[4]) {
				description = description + Preview.preview.children[4].innerHTML;
			};	
		};
		
		description = description + '...';
		
		$('#artdes').val(description);
		$('#ori_text').val($('#writing').val());
		theform.submit();
	});

	$(".articleshare").click(function(){
		var theform = document.getElementById("editdata");
		var previewcon = document.getElementById("previewtextcontainer");
		var maintext = get_preview_content();
		var share_id = calcMD5(maintext);

		$('#arttitle').val(get_title());
		$('#ori_text').val($('#writing').val());
		var post_data = {
			'arttitle' : $('#arttitle').val(),
			'maintext' : maintext,
			'ori_text' : $('#ori_text').val(),
			'share_id' : share_id
		};
		$.postJSON("/share/add/", post_data, function(data){
			window.location = "/share/" + share_id;
		});

		return false;
	});
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

function define_heading_id() {
	$('h2').each(function () {
		var $next = $(this).next();
		if($next.text().slice(0, 1) === '=') {
			$(this).attr('id', $next.text().slice(1));
			$(this).next().remove();
		}
	});
}

function removeMathjaxBlocks () {
	$('.MathJax_SVG_Display').each(function () {
		$(this).next().remove();
	});
}

function center_image(){
	$('.preview p img').parent().each(function(){
		if($(this).html().substr(0,4) == "<img"){
			$(this).addClass('center');
		}else{
			$(this).removeClass('center');
		}
	});
}

function get_preview_content(){
	var content = Preview.preview.innerHTML;
	return content;
}

function get_title(){
	var title = Preview.preview.getElementsByTagName('h1')[0].innerHTML;
	return title;
}

function swap_grap_block(){
	$(".grap").each(function(){
		var gra_ori_test = $(this).text();

		try{
			var result = Viz(gra_ori_test, "svg");
			var title_label = "";
			var grap_parent = $(this).parent();
			var next_para_text = grap_parent.next().text();
			if (next_para_text.substr(0,5) == "title") {
				title_label = '<br>' + next_para_text.slice(6);
				grap_parent.next().remove();
			};
			grap_parent.before('<div class="graphvizdisplay">' + result + title_label +'</div>');
			grap_parent.prev().addClass('center');
			grap_parent.remove();
		}catch(e){
			// console.log(e);
		}
	});
}