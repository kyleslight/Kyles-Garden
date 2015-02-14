$(document).ready(function(){
	// console.log("good");
	var gra_text = $("#test").text();
	var result = Viz(gra_text, "svg");

	$("#display").html(result);
});