
function displayVideos(){
    var dir = "recorded_videos/";
    var fileExtension = ".mp4";
    $.ajax({
        url: dir,
        success: function (data) {
            $(data).find("a:contains(" + fileExtension + ")").each(function () {
                var foldername = this.href.replace(window.location, "").replace("http://", "");
                console.log(filename);
            });
        }
    });


    innerHTML = 'hi';
    $(".displayVideoDirs").html(innerHTML);
}
