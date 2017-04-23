
function displayVideos(){
    var dir = "recorded_videos/";
    var fileExtension = ".mp4";
    $.ajax({
        url: dir,
        success: function (data) {
            $(data).find("a:contains(" + fileExtension + ")").each(function () {
                var filename = this.href.replace(window.location, "").replace("http://", "");
                var something = filename.toString().split['-'][0];
                console.log(filename);
                console.log(something);
            });
        }
    });


    innerHTML = 'hi';
    $(".displayVideoDirs").html(innerHTML);
}
