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
                console.log(filename);
                console.log(yearMonthDay);
                console.log(hourMinSec);
                var ymdDate = parseYYYYMMDD(yearMonthDay);
                console.log(ymdDate);
                displayDateHTML(ymdDate);
             });
        }
    });


    innerHTML = 'hi';
    $(".displayVideoDirs").html(innerHTML);
}

function parseYYYYMMDD(str) {
    if(!/^(\d){8}$/.test(str)) return "invalid date";
    var y = str.substr(0,4),
        m = str.substr(4,2) - 1,
        d = str.substr(6,2);
    return new Date(y,m,d);
}

function displayDateHTML(date) {
    htmlString = '<h3>';
    htmlString += 'Videos from ';
    htmlString += date.toString();
    htmlString += '</h3>';
    $(".displayVideoDirs").append(htmlString);
}
