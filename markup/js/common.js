var ui = {};
ui.confDate = new Date(2012, 5-1, 19);
ui.schedule = {
    init: function() {
        var $schedule = $("#schedule"),
            $currentTimeEl, $timeLabels,
            labelHeight,
            //now = new Date(2012, 4-1, 14, 12, 45),
            now = new Date(),
            confDate = ui.confDate,
            currentHours,
            currentMinutes,
            parseHourRegexp,
            startHour,
            endHour,
            inHourPixelVal, timeTopMargin;

        if ( $schedule.length == 0) {
            return;
        }
        if (confDate.getFullYear() != now.getFullYear() ||
            confDate.getMonth() != now.getMonth() ||
            confDate.getDate() != now.getDate) {
            // comment this return for debug
            return false;
        }

        currentHours = now.getHours();
        currentMinutes = now.getMinutes();

        $currentTimeEl = $schedule.find(".current-time");
        $timeLabels = $schedule.find(".caption");
        parseHourRegexp = /time_([0-9]{1,2})\-[0-9]{1,2}/;
        labelHeight = $timeLabels[0].offsetHeight;
        startHour = $timeLabels[0].className.match(parseHourRegexp);
        endHour = $timeLabels[$timeLabels.length-1].className.match(parseHourRegexp);
        inHourPixelVal = Math.round((currentMinutes / 60) * labelHeight);

        if (startHour != null && endHour != null) {
            startHour = Number(startHour[1]);
            endHour = Number(endHour[1]);
            timeTopMargin = ((currentHours - startHour) * labelHeight) + (inHourPixelVal);

            $currentTimeEl.css({
                'display': 'block',
                'top': timeTopMargin
            });
        }
    }
};

$(function(){
    $('.btn-share').click(function(){
        $(this).parent().siblings('.yashare-auto-init').show();

        return false;
    });

    ui.schedule.init();
});