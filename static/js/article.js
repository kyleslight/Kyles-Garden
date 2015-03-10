$(document).ready(function(){
	$("#writing h1").eq(0).after($("#store_author").html());

	get_article_index();

	$("#modifycollection").click(function(){
		$("#modifycollectiontitle").val($("#collectiontitletext").text());
		$("#modifycollectionbox").fadeToggle();
	});

	$("#submitmodifiedtitle").click(function(){
		cid = parseInt($(this).attr('value'));
		$.postJSON('/modify/collection/', {'id' : cid, 'title' : $("#modifycollectiontitle").val()}, function(data){
			$("#collectiontitletext").text(data.title);

			$("#modifycollectiontitle").val('');
			$("#modifycollectionbox").fadeToggle();
		});

		return false;
	});


	$(window).scroll(function(){
		var top = $(window).scrollTop();
		if (top > 0.1*$(window).height()) {
			if (!$(".readareawrap").hasClass("leftsharereadwrap")) {
				$(".readareawrap").addClass("leftsharereadwrap");
				$(".articlelist").addClass("fixedarticlelist");
				$(".articlelist").stop();
				$(".articlelist").animate({opacity:0.3}, 1000);
			};
		}else{
			if ($(".readareawrap").hasClass("leftsharereadwrap")) {
				$(".readareawrap").removeClass("leftsharereadwrap");
				$(".articlelist").removeClass("fixedarticlelist");
				$(".articlelist").stop();
				$(".articlelist").animate({opacity:1}, 1000);
			}
		}
		
	});

	$(".articlelist").hover(function(){
		$(".articlelist").stop();
		$(".articlelist").animate({opacity:1}, 1000);
	});
	$(".articlelist").mouseleave(function(){
		$(".articlelist").stop();
		var top = $(window).scrollTop();
		if (top > 0.1*$(window).height()) {
			$(".articlelist").animate({opacity:0.3}, 1000);
		}
	});
	remove_block();
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

function remove_block(){
	$("[type='math/tex; mode=display']").prev().remove();
}