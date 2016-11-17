$(document).ready(function(){

	// Modify MD-generated HTML
	//=======================================================

	// Footnotes
	//-------------------------------------------------------

	// Adjust position of all multiparagraph footnotes to fit a viewport.
	// Will clear all dynamic styling when small display layout is on.
	function move_wide_refbodies() {
		$('.refbody_wide').each(function(){
			$(this).removeAttr('style');

			if ($(window).width() >= 1000) {
				var elem_left = $(this).parent().offset().left +
					parseInt($(this).css('left'));
				var elem_width = parseInt($(this).css('min-width')) + 30;
				var gap = $(window).width() - (elem_left + elem_width);
				if (gap < 0) {
					$(this).offset({
						left: elem_left + gap
					});
				}
			}
		});
	}

	move_wide_refbodies();

	// It skips too frequent events to be more responsible.
	var resizeTimer;
	$(window).on('resize', function(){
		clearTimeout(resizeTimer);
		resizeTimer = setTimeout(move_wide_refbodies, 100);
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
			var url = "https://www.googleapis.com/youtube/v3/videos" +
				"?part=snippet&fields=items/snippet/title&prettyPrint=false" +
				"&id=" + id + "&key=AIzaSyDHgqe2iHORox_6rxmlT19JjDlBuWYlygU";
			$.ajax({ url: url, dataType: 'jsonp', cache: true,
				success: function(data){
					$('#youtube-title').html(data.items[0].snippet.title);
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
