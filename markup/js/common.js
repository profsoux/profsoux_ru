var ui = {};
ui.schedule = {
    init: function() {
        var $schedule = $("#schedule"),
            $currentTimeEl, $timeLabels,
            labelHeight,
            now,
            nowHours,
            nowMinutes,
            parseHourRegexp,
            startHour,
            endHour,
            inHourPixelVal, timeTopMargin;

        if ($schedule.length == 0) {
            return;
        }

        $currentTimeEl = $schedule.find(".current-time");
        $timeLabels = $schedule.find(".caption");
        now = new Date(2012, 4-1, 14, 18, 1 );
        nowHours = now.getHours();
        nowMinutes = now.getMinutes();
        parseHourRegexp = /time_([0-9]{1,2})\-[0-9]{1,2}/;
        labelHeight = $($timeLabels[0]).height();
        startHour = $timeLabels[0].className.match(parseHourRegexp);
        endHour = $timeLabels[$timeLabels.length-1].className.match(parseHourRegexp);
        inHourPixelVal = Math.round((nowMinutes / 60) * labelHeight);

        if (startHour != null && endHour != null) {
            startHour = Number(startHour[1]);
            endHour = Number(endHour[1]);
            timeTopMargin = ((endHour-1 - startHour) * labelHeight) + (inHourPixelVal);

            console.log([
                nowMinutes,
                60,
                labelHeight,
                endHour,
                startHour
            ]);

            $currentTimeEl.css({
                top: timeTopMargin
            });

        }

    }
};


$().ready(function(){
    ui.schedule.init();
});