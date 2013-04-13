var ui = new Object();

/**
 * Constants
 */
ui.CONF_DATE = new Date(2013, 5-1, 18);

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

ui.create = function(data, options) {
    var mode,
        parent = (options && 'parent' in options) ? options.parent : null,
        retval,
        result;

    if (typeof data === 'string' || typeof data === 'number') {
        mode = 'text';
    } else if (data instanceof Array) {
        mode = 'elem_set';
    } else {
        mode = 'elem';
    }

    switch (mode) {
        case 'text':
            result = document.createTextNode(data);
            retval = result;
            break;

        case 'elem':
            result = createElements( [data], options );
            retval = (result.fragment.childNodes.length === 1) ? result.fragment.childNodes[0] : result.fragment.childNodes;
            break;

        case 'elem_set':
            result = createElements( data, options );
            retval = result;
            break;
    }

    if (parent) {
        parent.appendChild(result);
    }

    return retval;

    function createElements(data, options, parent) {
        var fragment,
            set = [],
            cache, contentCache,
            item, i, j;

        fragment = document.createDocumentFragment();

        for (i = 0; i < data.length; i++) {
            item = data[i];

            if (typeof item === 'string') {
                // TEXT NODE
                fragment.appendChild(document.createTextNode(item));
            } else {
                // SINGLE NODE
                if (!item.c || typeof item.c === 'string') {
                    // single element
                    cache = createElement(item, options, fragment);
                    if (item.get) {
                        set.push(cache);
                    }
                } else {
                    // NODES TREE
                    contentCache = item.c;

                    if (item.get) {
                        cache = createElement(item, options);
                        set.push(cache);
                    } else {
                        cache = createElement(item, options);
                    }

                    var l = createElements(contentCache, options, cache);

                    if (l.set.length > 0) {
                        for (j = 0; j < l.set.length; j++) {
                            set.push(l.set[j]);
                        }
                    }
                    fragment.appendChild(cache);
                }
            }
        }

        if (parent) {
            parent.appendChild(fragment);
        }

        return {
            set: set,
            fragment: fragment
        };
    }

    function createElement(data, options, parent) {
        var options = (typeof options !== 'undefined') ? options : {},
            prefix = '',
            className = '',
            isTextNode = (typeof data === 'string'),
            tagName = data.tag || 'div',
            element;

        if (typeof data.prefix !== 'undefined') {
            prefix = data.prefix;
        } else if (typeof options.prefix !== 'undefined') {
            prefix = options.prefix;
        }

        className = (typeof data.e !== 'undefined') ? data.e : '';
        className = prefix + className;

        if (isTextNode) {
            element = document.createTextNode(data);
        } else {
            element = document.createElement(tagName);

            if (className !== '') {
                element.className = className;
            }

            delete (data.e);
            delete (data.tag);

            if (data.c && typeof data.c === 'string') {
                element.appendChild(document.createTextNode(data.c));
                delete data.c;
            }

            if (data.style){
                for (var p in data.style){
                    element.style[p] = data.style[p];
                }
                delete data.style;
            }

            for (var p in data){
                element[p] = data[p];
            }
        }

        if (parent) {
            parent.appendChild(element);
        }

        return element;
    }
};

ui.program = {
    timelineSegmentHeight: null,

    data: null,

    init: function(opts) {
        var that = this,
            data = opts.data,
            table;

        that.data = data;
        that.timelineSegmentHeight = that._getTimelineSegmentHeight();

        table = that.tpl.table(opts);

        return table;
    },

    getItemsInFlow: function(id) {
        var items = this.data.items,
            f = [];

        for (var i = 0, l = items.length; i < l; i++) {
            if (items[i].flowId === id) {
                f.push(items[i]);
            }
        }

        return f;
    },

    _getTimelineSegmentHeight: function() {
        var testNode, testTimelineSegment,
            segmentHeight = 0;

        testNode = ui.create({tag: 'div',
            style: {width: 0, height: 0, visibility: 'hidden', overflow: 'hidden'}
        });
        testTimelineSegment = ui.create({e:'program-timeline', c: [{e:'segment'}]});
        testNode.appendChild(testTimelineSegment);
        document.body.appendChild(testNode);
        segmentHeight = testTimelineSegment.offsetHeight;
        document.body.removeChild(testNode)

        return segmentHeight;
    },

    tpl: {
        table: function(opts) {
            var tpl = this,
                data = opts.data,
                table,
                timeline, timelineCell,
                flowCell, flowTitle, itemsInFlow,
                flowItem,
                i, j,
                programRow;

            table = ui.program.tpl.tableLayout(opts);

            programRow = table.set[0];
            timelineCell = table.set[1];

            timeline = tpl.timeline(opts.from, opts.to, opts.segments);
            timelineCell.appendChild(timeline);

            for (i = 0, il = data.flows.length; i < il; i++) {
                itemsInFlow = ui.program.getItemsInFlow(data.flows[i].id);
                flowTitle = data.flows[i].title;
                flowCell = tpl.flowCell(flowTitle, i === 0);

                for (j = 0; j < itemsInFlow.length; j++) {
                    flowItem = tpl.item(itemsInFlow[j]);
                    flowCell.appendChild(flowItem);
                }

                programRow.appendChild(flowCell);
            }

            return table.fragment;
        },
        tableLayout: function() {
            var table = ui.create([{
                tag: 'table',
                e: 'program program-flows-count_4',
                c: [{
                    tag: 'tr',
                    e: 'program-row',
                    c: [
                       {tag: 'td', e: 'program-timeline', get: 1}
                    ],
                    get: 1
                }]
            }]);

            return table;
        },
        flowCell: function(title, isFirst) {
            return ui.create({
                e: 'program-flow' + ((isFirst) ? ' first' : ''),
                tag: 'td',
                c: [
                    {e: 'program-flow-title', c: [
                        {e: 'title', c: title}
                    ]}
                ]}
            );
        },
        item: function(item) {
            return ui.create({
                e: 'program-item duration_'+ item.duration,
                c: [
                    {e: 'time', c: item.startTime},
                    {e: 'title', c: item.title},
                    {e: 'person', c: item.person}
                ]
            });
        },
        timelineSegment: function(label, isLast) {
            return ui.create({e: 'segment' + (isLast ? ' last' : ''), c: [
                {e: 'segment-line', style: {width: '1000px'}},
                {e: 'segment-label', c: label}
            ]});
        },
        timelineSubsegment: function(label) {
            return ui.create({e: 'subsegment', c: [{
                e: 'subsegment-label', c: label
            }]});
        },
        timeline: function(from, to, subsegments) {
            var from = Number(from.split(':')[0]),
                to = Number(to.split(':')[0]),
                segmentHeight = ui.program.timelineSegmentHeight,
                subsegments = (typeof subsegments !== 'undefined') ? subsegments : 2,
                subsegmentDuration = (subsegments > 0) ? Math.round(60 / subsegments) : 0,
                subsegmentPxStep = Math.round(segmentHeight / subsegments),
                segment, subsegment, label, sublabel,
                fragment = document.createDocumentFragment(),
                i, j;

            // Segments
            for (i = from; i <= to; i++) {
                label = i.toString() + ':00';
                segment = ui.program.tpl.timelineSegment(label, i === to);

                // Sub-segments
                if (i < to) {
                    for (j = 1; j < subsegments; j++) {
                        sublabel = i.toString() + ':' + (j * subsegmentDuration).toString();
                        subsegment = ui.program.tpl.timelineSubsegment(sublabel);
                        subsegment.style.top = (subsegmentPxStep * j).toString() + 'px';
                        segment.appendChild(subsegment);
                    }
                }

                fragment.appendChild(segment);
            }

            return fragment;
        }
    }
};

/**
 * Tweets stream
 */
ui.twee = {
    __months: {
        0: 'января',
        1: 'февраля',
        2: 'марта',
        3: 'апреля',
        4: 'мая',
        5: 'июня',
        6: 'июля',
        7: 'августа',
        8: 'сентября',
        9: 'ноября',
        10: 'октября',
        11: 'декабря'
    },

    // tweets list
    $list: null,

    // service time interval
    __t: null,

    // receiving data in progress flag
    isReceivingData: false,

    // data updated flag
    isDataUpdated: false,

    // data update interval
    updateDataInterval: 10000,

    // tweets list update interval
    updateListInterval: 3500,

    // animation duration
    updateAnimationDuration: 700,

    // tweets storage
    // when initialized tweets == []
    tweets: null,

    // visible tweets quantity
    tweetsToShow: 3,

    // current right tweet position
    currentPosition: 0,

    // test node
    testNode: null,

    // mode
    mode: 'normal',

    queryParams: {
        rpp: 20,
        result_type: 'recent',
        since_id: 0
    },

    maxTweetsNodesInStack: 10,

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

        if (typeof options === 'object') {
            for (option in options) {
                that[option] = options[option];
            }
        }
        that.$list.addClass('mode-'+ that.mode);
        $(document.body).addClass('twitter-widget-mode-'+ that.mode);

        // create test node
        testNode = document.createElement('ul');
        testNode.className = 'conf-tweets unstyled mode-'+ that.mode +' twee-test-node';
        document.body.appendChild(testNode);
        that.testNode = testNode;


        // sets normal state
        that.state = 'normal';


        // initial tweets render
        that.getTweets(options.searchQuery);
        that.__t = setInterval(function()
        {
            // observe for updates
            var from = that.tweetsToShow - 1,
                to = 0;

            if (that.isDataUpdated === true) {
                if (that.mode === 'projection') {
                    that.currentPosition = -1;
                    that.spinUp();
                } else if (that.mode === 'normal') {
                    that.renderTweets(from, to);
                    that.currentPosition = from;
                }
                that.isDataUpdated = false;
                clearInterval(that.__t);
            }
        }, 50);


        // set spin up interval
        setInterval(function() {
            that.spinUp();
        }, that.updateListInterval);


        // set data update
        setInterval(function() {
            that.getTweets(options.searchQuery);
        }, that.updateDataInterval);
    },

    getTweets: function(q) {
        if (this.state === 'paused') {
            return false;
        }

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
                    tweet.id_str = item.id_str;
                    tweet.user = item.from_user;
                    tweet.avatar = item.profile_image_url;
                    tweet.text = item.text;
                    tweet.created_at_timestamp = Date.parse(item.created_at);
                    tweet.created_at = new Date(tweet.created_at_timestamp);
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
            if (that.tweets === null) {
                that.tweets = [];
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
            tweetTextFormatted, tweetBody,
            tweetYear = tweet.created_at.getFullYear(),
            tweetMonthName = that.__months[ tweet.created_at.getMonth() ],
            tweetDay = tweet.created_at.getDate(),
            tweetHours = tweet.created_at.getHours(),
            tweetMinutes = tweet.created_at.getMinutes(),
            tweetLink = 'http://twitter.com/#!/'+ tweet.user +'/status/'+ tweet.id_str;

        if (tweetMinutes < 10) {
            tweetMinutes = '0'+ tweetMinutes;
        }

        tweetTextFormatted = tweet.text.replace(
            tweetTextReplacePattern,
            function(all, space, hashtag, username, link, email) {
                var res = '<a href="mailto:' + email + '">' + email + "</a>";
                hashtag && (res = space + '<a href="http://search.twitter.com/search?q=%23' + hashtag + '" class="hashtag">#' + hashtag + "</a>");
                username && (res = space + '<a href="http://twitter.com/' + username + '" class="username">@' + username + "</a>");
                link && (res = '<a href="' + encodeURI(decodeURI(link.replace(/<[^>]*>/g, ""))) + '" class="link">' + link + "</a>");
                return res;
            }
        );
        tweetBody = '<a href="http://twitter.com/' +
            tweet.user + '" title="@' +
            tweet.user + '"><img src="' +
            tweet.avatar + '"></a><p>' +
            '<a href="http://twitter.com/'+ tweet.user +'" class="tweet-author">'+ tweet.user +'</a>';

        if (that.mode === 'projection') {
            tweetBody += ' <span class="date">в ' + tweetHours +':'+ tweetMinutes +'</span><br>';
        } else if (that.mode === 'normal') {
            tweetBody += ': ';
        }
        tweetBody += tweetTextFormatted;

        // date

        if (that.mode === 'normal') {
            tweetBody += '<span class="date"><a href="'+ tweetLink+'" class="text">';
            tweetBody += [tweetHours, ':', tweetMinutes, ', ', tweetDay, ' ', tweetMonthName, ' ', tweetYear].join('');
            tweetBody += '</a></span>';
        }
        tweetBody += '</p>';

        if (that.mode == 'normal') {
            tweetBody = '<div class="tweet span4">'+ tweetBody +'</div>';
        } else if (that.mode == 'projection') {
            tweetBody = '<div class="tweet">'+ tweetBody +'</div>';
        }
        return tweetBody;
    },

    renderTweets: function(from, to) {
        if (this.tweets.length == 0) {
            return false;
        }

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
            tweetWidth, tweetHeight;

        tweetRendered = that.renderTweet(tweet);

        // get tweet width
        liTest = document.createElement('li');
        liTest.innerHTML = tweetRendered;
        testNode.appendChild(liTest);
        tweetWidth = liTest.offsetWidth;
        tweetHeight = liTest.offsetHeight;
        testNode.removeChild(liTest);

        // prepend tweet
        li = document.createElement('li');
        li.innerHTML = tweetRendered;

        if (that.mode === 'normal') {
            li.style.width = '0';
        } else if (that.mode === 'projection') {
            li.style.height = '0';
        }

        $tweetNode = $(li).find('.tweet');
        $tweetNode.css('display', 'none');
        if (that.width) {
            //$tweetNode.css('width', that.width);
        }
        $list.prepend(li);

        if (that.mode === 'normal') {
            $(li).animate({width: tweetWidth+'px'}, that.updateAnimationDuration, function() {
                $tweetNode.fadeIn();
                li.style.width = 'auto';
            });
        } else if (that.mode === 'projection') {
            $(li).animate({height: tweetHeight+'px'}, that.updateAnimationDuration, function() {
                $tweetNode.fadeIn();
                li.style.height = 'auto';
            });
        }
    },

    spinUp: function() {
        if (this.state === 'paused' || this.tweets.length === 0) {
            return false;
        }

        var that = this,
            $list = that.$list,
            tweets = that.tweets,
            targetTweet,
            tweetsNodes,
            nextTweet, newPosition;

        newPosition = that.currentPosition + 1;
        if (newPosition < that.tweets.length) {
            targetTweet = tweets[newPosition];
            that.addTweet(targetTweet);
            that.currentPosition = newPosition;

            // garbage cleaner
            tweetsNodes = $list.find('li');
            if (tweetsNodes.length >= that.maxTweetsNodesInStack) {
                $(tweetsNodes[tweetsNodes.length-1]).remove();
            }
        }
    },

    pause: function() {
        this.state = 'paused';
    },

    resume: function() {
        this.state = 'normal';
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

    var $paygate = $('#paygate');

    $paygate.find('link').remove();
});
