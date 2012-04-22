var ui = {};
ui.CONF_DATE = new Date(2012, 5-1, 19);
ui.schedule = {
    $schedule: null,

    init: function() {
        var $schedule = $("#schedule"),
            markerPlacementDate = new Date();

        /*
        markerPlacementDate = new Date(
            ui.CONF_DATE.getFullYear(),
            ui.CONF_DATE.getMonth(),
            ui.CONF_DATE.getDate(), 12, 15);
        */

        if ($schedule.length == 0) {
            return false;
        }

        this.$schedule = $schedule;
        this.initTooltips();

        if (ui.CONF_DATE.getFullYear() == markerPlacementDate.getFullYear() &&
            ui.CONF_DATE.getMonth() == markerPlacementDate.getMonth() &&
            ui.CONF_DATE.getDate() == markerPlacementDate.getDate()) {
            this.initTimeMarker(markerPlacementDate);
        }
    },

    initTooltips: function() {
        var $events = this.$schedule.find('.event');
        $events.each(function() {
            var eventLength = this.className.match(/div\-([0-9]{1,2})/),
                tooltipText = '';

            if (eventLength != null) {
                eventLength = Number(eventLength[1]);
                if (eventLength == 60) {
                    tooltipText = 'Длится 1 час';
                } else if (eventLength < 60) {
                    tooltipText = 'Длится '+ eventLength +' минут';
                }

                this.setAttribute('rel', 'tooltip');
                this.setAttribute('data-original-title', tooltipText);
                $(this).tooltip({
                    animation: false,
                    placement: 'left'
                });
            }
        });
    },

    initTimeMarker: function(placementDate) {
        var $schedule = this.$schedule,
            $timeElement, $timeLabels,
            labelHeight,
            placementDate = (placementDate instanceof Date) ? placementDate : new Date(),
            placementHours,
            placementMinutes,
            parseHourRegexp,
            startHour,
            endHour,
            inHourPixelVal, timeTopMargin;

        // init vars block
        placementHours = placementDate.getHours();
        placementMinutes = placementDate.getMinutes();
        $timeElement = $schedule.find(".current-time");
        $timeLabels = $schedule.find(".caption");
        parseHourRegexp = /time_([0-9]{1,2})\-[0-9]{1,2}/;
        labelHeight = $timeLabels[0].offsetHeight;
        startHour = $timeLabels[0].className.match(parseHourRegexp);
        endHour = $timeLabels[$timeLabels.length-1].className.match(parseHourRegexp);
        inHourPixelVal = Math.round((placementMinutes / 60) * labelHeight);

        if (startHour != null && endHour != null) {
            startHour = Number(startHour[1]);
            endHour = Number(endHour[1]);
            timeTopMargin = ((placementHours - startHour) * labelHeight) + (inHourPixelVal);
            timeTopMargin -= 1;

            $timeElement.css({
                'display': 'block',
                'top': timeTopMargin
            });
        }
    }
};
ui.getTweets = function(q) {
    var list = $("#confTweets"),
        tweets = [],
        url = 'http://search.twitter.com/search.json?q=%23' + q + '&rpp=20&callback=?';

    if (list.length == 0) {
        return false;
    }

    $.getJSON( url, function( data ) {
        $.each( data.results, function( i, item )
        {
            var tweet = {},
                now = new Date(),
                user = item.from_user,
                image = item.profile_image_url,
                text = item.text,
                date = null,
                created_at = Date.parse(item.created_at);

            text = text.replace(
                /(^|\s)(?:#([\d\w_]+)|@([\d\w_]{1,15}))|(https?:\/\/[^\s"]+[\d\w_\-\/])|([^\s:@"]+@[^\s:@"]*)/gi,
                function( all, space, hashtag, username, link, email ) {
                    var res = '<a href="mailto:' + email + '">' + email + "</a>";
                    hashtag && (res = space + '<a href="http://search.twitter.com/search?q=%23' + hashtag + '">#' + hashtag + "</a>");
                    username && (res = space + '<a href="http://twitter.com/' + username + '">@' + username + "</a>");
                    link && (res = '<a href="' + encodeURI(decodeURI(link.replace(/<[^>]*>/g, ""))) + '">' + link + "</a>");
                    return res;
                }
            );

            tweet.user = user;
            tweet.image = image;
            tweet.text = text;

            if (created_at != NaN) {
                tweet.date = now.setTime(created_at);
            }

            //list.push(tweet);
            list.append(
                '<li class="span4"><a href="http://twitter.com/' +
                    user + '" title="' +
                    user + '"><img src="' +
                    image + '"></a><p>' +
                    text + '</p></li>'
            );
        });
    });
    return tweets;
};


$(function(){
    $('.btn-share').click(function(){
        $(this).parent().siblings('.yashare-auto-init').slideToggle();

        return false;
    });

    ui.schedule.init();
});