function displayVideos(){
    var dir = "recorded_videos/";
    var fileExtension = ".mp4";
    $.ajax({
        url: dir,
        success: function (data) {
            $(data).find("a:contains(" + fileExtension + ")").each(function () {
                var filename = this.href.replace(window.location, "").replace("http://", "");
                var filetimestamp = filename.split('_')[1].split('-');
                var yearMonthDay = filetimestamp[0];
                var hourMinSec = filetimestamp[1].split('.')[0];
                var ymdDate = parseYYYYMMDD(yearMonthDay);
                displayDateHTML(ymdDate);
                displayVideoFromDate(filename);
             });
        }
    });
}

function parseYYYYMMDD(str) {
    if(!/^(\d){8}$/.test(str)) return "invalid date";
    var y = str.substr(0,4),
        m = str.substr(4,2) - 1,
        d = str.substr(6,2);
    return new Date(y,m,d);
}

function displayDateHTML(date) {
    idString = 'day_' + date.getDate().toString();
    var elementExists = document.getElementById(idString);
    if (elementExists == null){
        htmlString = '<div id="';
        htmlString += idString
        htmlString += '" class= "videosShown"><h2>';
        htmlString += 'Videos from ';
        htmlString += moment(date).format('MMMM Do YYYY');
        htmlString += '</h2>';
        htmlString += '</div>';
        $(".displayVideoHeaders").append(htmlString);
    }
}

function displayVideoFromDate(filename) {
    htmlString = '<video width="320" height="240" controls>';
    htmlString += '<source src="/recorded_videos/'
    htmlString += filename;
    htmlString += '" type="video/mp4">Browser does not support HTML5 video';
    htmlString += '</video><br><br>';
    $(".displayVideoDirs").append(htmlString);
}

