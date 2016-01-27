
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
		// http://stackoverflow.com/questions/3614212/
		var img = $('<div/>').append($(this).clone()).html();
		var figcaption = '<figcaption><div><em>' + title + '</em></div></figcaption>';
		var figure = '<figure>' + img + figcaption + '</figure>';

		if ($parent.parent().hasClass('page')) {
			// article content
			$parent.replaceWith(figure);
		} else {
			// footnote content
			$(this).remove();
			$parent.prepend(figure);
		}
	});

	// Footnotes
	//-------------------------------------------------------
	$('a[rev=footnote]').remove();

	$($('a[rel=footnote]').get().reverse()).each(function(){
		var num = $(this).html();
		var rel = $(this).attr('href').substring(1).replace(':', '\\:');
		var is_multipar = $('.footnote li#' + rel + ' > p').length > 1;
		var body = $('.footnote li#' + rel).contents();

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
		var refbody_class = is_multipar ? 'refbody refbody_wide' : 'refbody';
		$footnote
			.wrap($('<span/>', {class: 'ref'}))
			.after('<span class="ellipsis">&#8627;</span>')
			.after($('<span/>', {class: refbody_class, html: body}));

		// Adjust punctuation place (before a reference body,
		// but after a reference icon)
		var node_after = $footnote.parent()[0].nextSibling;
		 /* 3 is Node.TEXT_NODE, IE7 does not define that */
		if (node_after == null || node_after.nodeType != 3)
			return;
		var text_orig = node_after.textContent;
		if (text_orig.length == 0)
			return;
		var text_split_2 = text_orig.replace(/^[,;:.)]*/, '');
		var text_split_1 = text_orig.substring(0, text_orig.length - text_split_2.length);
		node_after.textContent = text_split_2;
		$footnote.children('.refnum').after($('<span/>', { class: 'punctum', html: text_split_1 }));
	});

	$('.footnote').remove();
	$('.original+.page a').attr('target', '_blank');

	// Horizontal lines
	//-------------------------------------------------------
	$('div[class=page]').find('hr').each(function(){
		$(this).wrap('<div class="border-bottom"></div>');
	});

	// YouTube links
	//-------------------------------------------------------
	var playerShown = false;
	var videoLink = null;

	function getYouTubeIdAndTime(url){
		var yt = {
			'id': null,
			'time': null,
		}
		var urlRE = /^.*((youtu.be\/)|(v\/)|(\/u\/\w\/)|(embed\/)|(watch\?))\??(?:v=)?([^#\&\?]*)(.*)$/;
		var timeRE = /^.*[#\?\&]t=(\d+).*$/;
		var matchUrl = url.match(urlRE);
		if (matchUrl && matchUrl[7].length == 11){
			yt['id'] = matchUrl[7];
			var matchTime = matchUrl[8].match(timeRE);
			yt['time'] = matchTime ? matchTime[1] : 0;
		}
		return yt;
	}

	var ytIdAttr = "youtube-id";
	var ytTimeAttr = "youtube-time";
	$('.page a').each(function(){
		var url = $(this).attr('href');
		var yt = getYouTubeIdAndTime(url);
		if (yt['id']) {
			$(this).addClass('youtube');
			$(this).attr(ytIdAttr, yt['id']);
			$(this).attr(ytTimeAttr, yt['time']);
			//$(this).append('&nbsp;&#8227;');
		}
	});

	function getYouTubePlayer(ID, time, width, height) {
		var YouTubeURL = "//www.youtube.com/embed/" + ID + "?rel=0&showsearch=0&autohide=" + 0;
		YouTubeURL += "&autoplay=" + 1 + "&controls=" + 1 + "&fs=" + 1 + "&loop=" + 0;
		YouTubeURL += "&showinfo=" + 0 + "&color=" + "white" + "&theme=" + "light";
		YouTubeURL += "&start=" + time;

		var YouTubePlayer = '<iframe title="YouTube video player" style="margin:0; padding:0;" width="' + width + '" ';
		YouTubePlayer += 'height="' + height + '" src="' + YouTubeURL + '" frameborder="0" allowfullscreen></iframe>';

		YouTubePlayer = "<span id='youtube-title'>...</span>" + YouTubePlayer;
		YouTubePlayer += "<span id='youtube-close'>Закрыть ролик</span>";
		YouTubePlayer = "<div class='youtube-player'>" + YouTubePlayer + "</div>";
		return YouTubePlayer;
	}

	jQuery.fn.shake = function(times, distance, duration) {
		this.each(function() {
			$(this).css("position","relative");
			for (var x = 1; x <= times; x++) {
				$(this).animate({left: -distance}, (((duration / times) / 4)))
					   .animate({left: distance}, ((duration / times) / 2))
					   .animate({left: 0}, (((duration / times) / 4)));
				distance *= 0.7;
			}
	  });
	return this;
	};

	var closePlayer = function(event){
		if (event.target != $('.youtube-player iframe').get(0)) {
			$('.youtube-player').remove();
			playerShown = false;
		}
		videoLink.shake(3, 10, 500);
		event.stopPropagation();
		return false;
	};

	setVideoSize = function() {
		var video = $('.youtube-player iframe');
		var player = $('.youtube-player');
		var ratio = video.attr("height") / video.attr("width");
		var addedHeight = $('#youtube-title').height() + $('#youtube-close').height() + 60;

		var playerWidth = player.width() - 30;
		var playerHeight = player.height() - 30;

		var newWidth = playerWidth > 600 ? 600 : playerWidth;
		var newHeight = newWidth * ratio;

		if (newHeight + addedHeight > playerHeight) {
			newHeight = playerHeight - addedHeight;
			newWidth = newHeight / ratio;
		}

		video
			.attr("width", newWidth)
			.attr("height", newHeight)

		player.css("padding-top", (player.height() - newHeight - addedHeight) / 2);
	}

	setYouTubeTitle = function(id) {
		var title = videoLink.attr('title');
		if (title) {
			$('#youtube-title').html(title);
		} else {
			var url = "//gdata.youtube.com/feeds/api/videos/" + id + "?v=2&alt=json";
			$.ajax({ url: url, dataType: 'jsonp', cache: true,
				success: function(data){
					$('#youtube-title').html(data.entry.title.$t);
					//setVideoSize();
				}
			});
		}
	}

	$('a.youtube').click(function(event){

		if (event.which != 1) return true;

		if (!playerShown) {
			var videoID = $(this).attr(ytIdAttr);
			var time = $(this).attr(ytTimeAttr);
			var player = getYouTubePlayer(videoID, time, 400, 300);
			$(this).after(player);
			$('.youtube-player').click(closePlayer);
			$('.youtube-player a').click(function(e){
				e.preventDefault();
				return false;
			});
			videoLink = $(this);
			setVideoSize();
			setYouTubeTitle(videoID);

			playerShown = true;
		} else {
			$('.youtube-player').remove();
			playerShown = false;
		}

		event.preventDefault();
		event.stopPropagation();
		return false;
	});

	$(window).on('resize', function(){
		if (playerShown) {
			setVideoSize();
		}
	})

	//=======================================================

	// Menu
	function toggleNav(event) {
		if (event.which != 1) return true;
		var $nav = $("nav");
		$nav.toggleClass("expanded");
		event.preventDefault();
		event.stopPropagation();
		return false;
	}

	$(".menu-button, .menu-item.selected a").click(toggleNav);

	$('html, .content').click(function(event) {
		if ($(window).width() >= 1000) {
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
		if ($(window).width() >= 1000) {
			$(".ref").removeClass("active");
		}
		$(this).parent().parent().toggleClass("active", !nowActive);
	});

	// Figures
	$(".illustration").click(function(e) {
		$(this).parent().toggleClass("active");
	});

});
