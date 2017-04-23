
function displayVideos(){
    var dir = "recorded_videos/";
    var fileExtension = ".mp4";
    $.ajax({
        url: dir,
        success: function (data) {
            $(data).find("a:contains(" + fileExtension + ")").each(function () {
                var filename = this.href.replace(window.location, "").replace("http://", "");
                var something = filename.split('_')[1].split('-');
                console.log(filename);
                console.log(something[0]);
                console.log(something[1]);
            });
        }
    });


    innerHTML = 'hi';
    $(".displayVideoDirs").html(innerHTML);
}
