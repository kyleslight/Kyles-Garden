$(document).ready(function(){
	$("#writing h1").eq(0).after($("#store_author").html());

	get_article_index();

	$("#modifycollection").click(function(){
		$("#modifycollectionbox").fadeToggle();
	});

	$("#submitmodifiedtitle").click(function(){
		cid = parseInt($(this).attr('value'));
		$.getJSON('/modify/collection/', {'id' : cid, 'title' : $("#modifycollectiontitle").val()}, function(data){
			$("#collectiontitletext").text(data.title);

			$("#modifycollectiontitle").val('');
			$("#modifycollectionbox").fadeToggle();
		});

		return false;
	});
});


function get_article_index(){
	var article_index = [];
	$("#writing h2").each(function(){
		article_index.push({'title' : $(this).html(), 'point' : $(this).attr('id')});
	});

	var article_index_block = '<div id="article_index">';
	for (var i = 0; i < article_index.length; i++) {
		article_index_block += '<a href=#'+ article_index[i].point +' class="article_h2">'+ article_index[i].title +'</a>'
	};
	article_index_block += '</div>';

	$(".spearticlelisttitle").eq(0).after(article_index_block);
}