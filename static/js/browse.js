$(document).ready(function () {
	$("#submitbook").click(function(){
		$.getJSON('/book/add', {'title' : $("#addbooktitle").val()}, function(data){
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

		$.getJSON('/collection/add', {
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
		$(this).next().fadeToggle();
	});

	$(".submitmodifiedtitle").click(function(){
		var bid = parseInt($(this).attr('value'));
		var url = '/modify/book/';
		$.getJSON(url, {'id' : bid, 'title' : $("#modifybooktitle_" + bid).val()}, function(data){
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