$(document).ready(function () {
	$("#submitbook").click(function(){
		$.postJSON('/book/add', {'title' : $("#addbooktitle").val()}, function(data){
			var book_block = '<div class="book">'
				+	'<div class="booktitle">'+ data.title +'</div>'
				+	'<div class="bookcollect">'
				+	'<a href="#" class="expandaddcollect">Add a Collection</a>'
				+	'<div class="addcollectbox">'
				+		'<input type="text" class="addcollecttitle">'
				+		'<a href="#" class="submitcollect">Add</a>'
				+		'<input type="text" class="book_index none" value="'+ data.id +'">'
				+	'</div>'
				+'</div>'	
				+'</div>';

			window.location = '/';
		});

		return false;
	});

	$(".submitcollect").click(function(){
		var title = $(this).prev().val();
		var book_id = parseInt($(this).next().val());

		$.postJSON('/collection/add', {
			'title' : title,
			'book_id' : book_id
		},function(data){
			var collection_block = '<a href="/edit/collection/'+ data.id +'" class="collect">'+ data.title +'</a>';
			$("#bookcollect_" + data.book_id).append(collection_block);

			$("#addcollectbox_" + data.book_id).fadeToggle();
			$("#addcollecttitle_" + data.book_id).val('');
		});

		return false;
	});

	$(".modifybook").click(function(){
		var book_id = $(this).attr('value');
		$("#modifybooktitle_" + book_id).val($("#booktitletext_" + book_id).text());
		$(this).next().fadeToggle();

		return false;
	});

	$(".submitmodifiedtitle").click(function(){
		var bid = parseInt($(this).attr('value'));
		var url = '/modify/book/';
		$.postJSON(url, {'id' : bid, 'title' : $("#modifybooktitle_" + bid).val()}, function(data){
			$("#booktitletext_" + data.id).text(data.title);
		});

		$("#modifybooktitle_" + bid).val('');

		$("#modifybookbox_" + bid).fadeToggle();

		return false;
	});

	$(".expandaddcollect").click(function(){
		$(this).parent().parent().next().fadeToggle();

		return false;
	});

	$("#expandaddbook").click(function(){
		$("#addbookbox").fadeToggle();

		return false;
	});
})

function getCookie(name){
	var c = document.cookie.match("\\b" + name + "=([^;]*)\\b"); return c ? c[1] : undefined;
}

$.postJSON = function(url, data, callback) { 
	data._xsrf = getCookie("_xsrf"); 
	jQuery.ajax({
		url: url,
		data: jQuery.param(data), dataType: "json",
		type: "POST",
		success: callback
	}); 
}
