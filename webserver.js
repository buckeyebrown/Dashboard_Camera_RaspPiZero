
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
            });
        }
    });


    innerHTML = 'hi';
    $(".displayVideoDirs").html(innerHTML);
}
