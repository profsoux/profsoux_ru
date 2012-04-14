var ui = {};
ui.schedule = {
    init: function() {
        var $schedule = $("#schedule"),
            $currentTimeEl, $timeLabels,
            labelHeight,
            now,
            currentHours,
            currentMinutes,
            parseHourRegexp,
            startHour,
            endHour,
            inHourPixelVal, timeTopMargin;

        if ($schedule.length == 0) {
            return;
        }

        $currentTimeEl = $schedule.find(".current-time");
        $timeLabels = $schedule.find(".caption");
        now = new Date();
        currentHours = now.getHours();
        currentMinutes = now.getMinutes();
        parseHourRegexp = /time_([0-9]{1,2})\-[0-9]{1,2}/;
        labelHeight = $timeLabels[0].offsetHeight;
        startHour = $timeLabels[0].className.match(parseHourRegexp);
        endHour = $timeLabels[$timeLabels.length-1].className.match(parseHourRegexp);
        inHourPixelVal = Math.round((currentMinutes / 60) * labelHeight);

        if (startHour != null && endHour != null) {
            startHour = Number(startHour[1]);
            endHour = Number(endHour[1]);
            timeTopMargin = ((currentHours - startHour) * labelHeight) + (inHourPixelVal);

            $currentTimeEl.css('top', timeTopMargin);
        }
    }
};


$().ready(function(){
    ui.schedule.init();
});