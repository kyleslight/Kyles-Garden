var eveCode = -1

$(document).ready(function(){
	$(window).keyup(function(e){
        if (e.keyCode==38) {
            return;
        };
        eveCode=e.keyCode;
    });
})

function showHint(searchKeyWord){



    if (eveCode==40||eveCode==38) {
        return;
    };
    if (searchKeyWord.replace(/\s/g,"").length==0&&searchKeyWord!="") {
        return;
    };
    $(".resultlist").empty();

    suggestionurl = '/suggestion/' + searchKeyWord;
    $.getJSON(suggestionurl, function(data){
    	$(".resultlist").empty();
    	var i;
    	for(i = 0;i < data.length;i++){
    		var data_temp = data[i];
    		var blog ='<li class="result">'
					+ '<p class="title"><a href="'+data_temp['link']+'">'+data_temp['title']+'</a></p>'
					+ '<p class="content">'+data_temp['content']+'</p>'
					+ '</li><hr>';

			$('.resultlist').append(blog);
    	}
    	$('.resultlist').append('<p>and this is '+searchKeyWord+'</p>')
   		// console.log(data.length);
    }); 
    
    // var returnWordsNum=Math.floor(Math.random()*8)+2;
    // for(var i=0;i<returnWordsNum;i++){
    //     var searchSuggestionWord=searchKeyWord+generateMixed(2);
    //     var app='<a class="searchSuggestionsList" href="/book'+searchSuggestionWord+'" >'+searchSuggestionWord+'</a>';
    //     $(".resultlist").prepend(app);
    // };

}

var chars = ['0','1','2','3','4','5','6','7','8','9','A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z'];
function generateMixed(n) {
     var res = "";
     for(var i = 0; i < n ; i ++) {
         var id = Math.ceil(Math.random()*35);
         res += chars[id];
     }
     return res;
}