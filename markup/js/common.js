var ui = new Object();

/**
 * Constants
 */
ui.CONF_DATE = new Date(2012, 5-1, 19);

/**
 * Schedule
 */
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
        //this.initTooltips();

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

/**
 * Tweets stream
  */
ui.twee = {
    // tweets list
    $list: null,

    // service time interval
    __t: null,

    // receiving data in progress flag
    isReceivingData: false,

    // data updated flag
    isDataUpdated: false,

    // data update interval
    dataUpdateInterval: 10000,

    // tweets list update interval
    listUpdateInterval: 3000,

    // animation duration
    updateAnimationDuration: 700,

    // tweets storage
    tweets: [],

    // visible tweets quantity
    tweetsToShow: 3,

    // current right tweet position
    currentPosition: 0,

    // test node
    testNode: null,

    // orientation
    orientation: 'x',

    queryParams: {
        rpp: 20,
        result_type: 'recent',
        since_id: 0
    },

    // current state
    state: 'paused',

    // tweet text replacement pattern
    tweetTextReplacePattern: /(^|\s)(?:#([a-zA-Zа-яА-Я0-9_]+)|@([\d\w_]{1,15}))|(https?:\/\/[^\s"]+[\d\w_\-\/])|([^\s:@"]+@[^\s:@"]*)/gi,

    init: function(options) {
        var that = this,
            testNode;

        that.$list = $('#confTweets');
        if (that.$list.length == 0) {
            return false;
        }

        // create test node
        testNode = document.createElement('ul');
        testNode.className = 'twee-test-node';
        document.body.appendChild(testNode);
        that.testNode = testNode;

        // initial tweets render
        that.getTweets(options.searchQuery);
        // observe for updates
        that.__t = setInterval(function()
        {
            var from = that.tweetsToShow - 1,
                to = 0;

            if (that.isDataUpdated === true) {
                that.renderTweets(from, to);
                that.currentPosition = from;
                that.isDataUpdated = false;
                clearInterval(that.__t);
            }
        }, 50);

        if (that.state == 'paused') {
            that.state = 'normal';
        }
        // set roll interval
        setInterval(function()
        {
            that.spinUp();
        }, that.listUpdateInterval);

        // set data update
    },

    getTweets: function(q) {
        var that = this,
            tweets = [],
            url = 'http://search.twitter.com/search.json?q='+ escape(q) + '&callback=?';

        that.isReceivingData = true;
        $.getJSON(url, that.queryParams, function(data) {
            var reverseTweets = [],
                i, length;

            if (data.results.length > 0)
            {
                $.each(data.results, function(i, item)
                {
                    var tweet = {};
                    //if (item.text.indexOf("RT ") != 0) {
                    tweet.id = item.id;
                    tweet.user = item.from_user;
                    tweet.avatar = item.profile_image_url;
                    tweet.text = item.text;
                    tweet.created_at = Date.parse(item.created_at);
                    tweets.push(tweet);
                });
            }

            // get new tweets from this id
            if (data.max_id_str) {
                that.queryParams.since_id = data.max_id_str;

                // debug id
                //that.queryParams.since_id = 203374752235139070;
            }

            // initial call
            if (that.tweets.length == 0) {
                // reverse array
                i = tweets.length;
                while (i > 0) {
                    i--;
                    reverseTweets.push(tweets[i]);
                }
                that.tweets = reverseTweets;
            } else {
                if (tweets.length > 0) {
                    i = tweets.length;
                    while (i > 0) {
                        i--;
                        that.tweets.push(tweets[i]);
                    }
                }
            }
            that.isDataUpdated = true;
            that.isReceivingData = false;
        });
    },

    renderTweet: function(tweet) {
        var that = this,
            tweetTextReplacePattern = that.tweetTextReplacePattern,
            tweetTextFormatted, tweetBody;

        tweetTextFormatted = tweet.text.replace(
            tweetTextReplacePattern,
            function(all, space, hashtag, username, link, email) {
                var res = '<a href="mailto:' + email + '">' + email + "</a>";
                hashtag && (res = space + '<a href="http://search.twitter.com/search?q=%23' + hashtag + '">#' + hashtag + "</a>");
                username && (res = space + '<a href="http://twitter.com/' + username + '">@' + username + "</a>");
                link && (res = '<a href="' + encodeURI(decodeURI(link.replace(/<[^>]*>/g, ""))) + '">' + link + "</a>");
                return res;
            }
        );
        tweetBody = '<div class="tweet span4"><a href="http://twitter.com/' +
            tweet.user + '" title="@' +
            tweet.user + '"><img src="' +
            tweet.avatar + '"></a><p>' +
            '<a href="http://twitter.com/'+ tweet.user +'" class="twitter-user">'+ tweet.user +'</a>&nbsp;' +
            tweetTextFormatted +'</p></div>';

        return tweetBody;
    },

    renderTweets: function(from, to) {
        var that = this,
            $list = that.$list,
            tweets = that.tweets,
            from = (typeof from === 'number') ? from : 0,
            to = (typeof to === 'number') ? to : tweets.length,
            tweetsFormatted = [],
            i;

        // reverse iteration
        if (from > to)
        {
            i = from;
            while (i >= to) {
                tweetsFormatted.push('<li>' + that.renderTweet(tweets[i]) + '</li>');
                i--;
            }
        }
        // normal
        else {
            for (i = from; i < to; i++) {
                tweetsFormatted.push('<li>' + that.renderTweet(tweets[i]) + '</li>');
            }
        }
        $list.html(tweetsFormatted.join(''));
    },

    addTweet: function(tweet) {
        var that = this,
            $list = that.$list,
            tweets = that.tweets,
            testNode = that.testNode,
            tweetRendered, $tweetNode,
            li, liTest,
            tweetWidth;

        tweetRendered = that.renderTweet(tweet);

        // get tweet width
        liTest = document.createElement('li');
        liTest.innerHTML = tweetRendered;
        testNode.appendChild(liTest);
        tweetWidth = liTest.offsetWidth;
        testNode.removeChild(liTest);

        // prepend tweet
        li = document.createElement('li');
        li.innerHTML = tweetRendered;
        li.style.width = '0';

        $tweetNode = $(li).find('.tweet');
        $tweetNode.css('display', 'none');
        $list.prepend(li);

        $(li).animate({width: tweetWidth+'px'}, that.updateAnimationDuration, function() {
            $tweetNode.fadeIn();
            li.style.width = 'auto';
        });
    },

    pause: function() {
        this.state = 'paused';
    },

    resume: function() {
        this.state = 'normal';
    },

    spinUp: function() {
        if (this.state == 'paused') {
            return false;
        }

        var that = this,
            $list = that.$list,
            tweets = that.tweets,
            nextTweet, newPosition;

        newPosition = that.currentPosition + 1;
        if (newPosition < that.tweets.length) {
            that.addTweet(tweets[newPosition]);
            that.currentPosition = newPosition;
        }
    }
};

/**
 * Livestream
 */
ui.videoStream = {
    playerTemplate:
        '<iframe width="{width}" height="{height}" src="http://cdn.livestream.com/embed/{streamProfile}?layout=4&amp;height={height}&amp;width={width}&amp;autoplay={autoplay}" style="border:0;outline:0" frameborder="0" scrolling="no"></iframe>' +
        '<div style="font-size:11px; padding-top:10px; text-align:center;">Watch ' +
        '<a href="http://www.livestream.com/?utm_source=lsplayer&amp;utm_medium=embed&amp;utm_campaign=footerlinks" title="live streaming video">live streaming video</a> from ' +
        '<a href="http://www.livestream.com/{streamProfile}?utm_source=lsplayer&amp;utm_medium=embed&amp;utm_campaign=footerlinks" title="Watch ProfsoUX at livestream.com">ProfsoUX Conference</a> at livestream.com' +
        '</div>',

    $playerContainer: null,
    width: 640,
    height: 385,
    streamProfile: 'profsoux',
    autoplay: false,

    init: function(options) {
        var that = this,
            option;

        if (typeof options === 'object') {
            for (option in options) {
                if (option in that) {
                    that[option] = options[option];
                }
            }
        }

        that.$playerContainer = $('#confVideoStream');
        if (that.$playerContainer.length == 0) {
            return false;
        }

        that.showPreloader();
        that.renderPlayer();
    },

    showPreloader: function() {
        var that = this;
        that.$playerContainer.html('Loading...');
    },

    renderPlayer: function() {
        var that = this,
            playerTemplate = that.playerTemplate,
            width, height,
            playerStr = '';

        width = that.$playerContainer.get(0).offsetWidth;
        height = Math.round(width * 0.75); // 4/3

        playerStr = playerTemplate.replace(/\{width\}/g, width)
            .replace(/\{height\}/g, height)
            .replace(/\{streamProfile\}/g, that.streamProfile)
            .replace(/\{autoplay\}/g, that.autoplay);

        that.$playerContainer.html(playerStr);
    }
};


$(function(){
    // schedule
    ui.schedule.init();

    // tweets stream
    ui.twee.init({
        searchQuery: '#profsoux'
    });

    // video stream
    ui.videoStream.init({
        streamProfile: 'profsoux'
    });
});