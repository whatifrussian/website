
$(document).ready(function(){ 

	// Modify MD-generated HTML
	//=======================================================

	// Question
	//-------------------------------------------------------
	var $question = $('blockquote').first();
	// $question
	// 	.contents().filter(function() {
	// 		return this.nodeType == 3;
	// 	}).wrap('<p></p>');
	// $question
	// 	.contents().filter('br').remove();
	$question
		.addClass('question')
		.html('<div>' + $question.html() + '</div>');
	// var $author = $('.question div p').last();
	// $author.addClass('q-author').html($author.html().trim());

	// Figures
	//-------------------------------------------------------
	$('p img').each(function(){
		$(this).addClass('illustration');
		var title = $(this).attr('title');
		
		var $parent = $(this).parent();
		// var $transcript = $parent.next();
		// $('<div/>', {
		// 	class: 'transcript',
		// 	text: '[transcript]' + $transcript.html() + '[/transcript]'
		// }).appendTo($parent).wrap('<figcaption></figcaption>').after($('<em/>', {text: title}));
		// $transcript.remove();
		$('<div/>', {
			html: '<em>' + title + '</em>'
		}).appendTo($parent).wrap('<figcaption></figcaption>');

		$parent.replaceWith('<figure>' + $parent.html() + '</figure>');
	});

	// Footnotes
	//-------------------------------------------------------
	$('a[rev=footnote]').remove();
	$('a[rel=footnote]').each(function(){
		var num = $(this).html();
		var rel = $(this).attr('href').substring(1).replace(':', '\\:');
		var body = $('.footnote li#' + rel + ' p').map(function(){
		    return $(this).html();
		}).get().join('<br><br>');

		var $footnote = $('<sup/>', {class: 'refnum', html: '<span>' + num + '</span>'});
		$footnote
			.prepend('<span class="bracket">[</span>')
			.append('<span class="bracket">]</span>')
			.append('<b></b>');
		$(this).parent().replaceWith($footnote);
		$footnote
			.wrap('<nobr></nobr>')
			.after('<span class="ellipsis">&#8626;</span>');
		$footnote = $footnote.parent();
		$footnote
			.wrap($('<span/>', {class: 'ref'}))
			.after('<span class="ellipsis">&#8627;</span>')
			.after($('<span/>', {class: 'refbody', html: body}));
	});
	$('.footnote').remove();
	$('.original+.page a').attr('target', '_blank');


	//=======================================================

	// Menu
	function toggleNav(event) {
	  	var $nav = $("nav");
	  	$nav.toggleClass("expanded");
	}

	$(".menu-button, .menu-item.selected a").click(toggleNav);

	$('html, .content').click(function(event) {
		if ($(window).width() >= 800) {
			$(".ref").removeClass("active");
		}
	});

	$('.logo, .header-title, .content').click(function(){
		$('nav').removeClass('expanded');
	});

	$('.refnum').click(function(event) {
		event.stopPropagation();
		return false;
	});

	// Ref-popups
	$(".refnum").click(function(e) {
		var nowActive = $(this).parent().parent().hasClass("active");
		if ($(window).width() >= 800) {
			$(".ref").removeClass("active");
		}
		$(this).parent().parent().toggleClass("active", !nowActive);
	});

	// Figures
	$(".illustration").click(function(e) {
		$(this).parent().toggleClass("active");
	});

});

