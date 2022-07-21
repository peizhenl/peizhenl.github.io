/**
 * get the url of the uploading image
 * */
function getObjectURL(file) {
  var url = null;
  if (window.createObjectURL != undefined) {
    // basic
    url = window.createObjectURL(file);
  } else if (window.URL != undefined) {
    // mozilla(firefox)
    url = window.URL.createObjectURL(file);
  } else if (window.webkitURL != undefined) {
    // webkit or chrome
    url = window.webkitURL.createObjectURL(file);
  }
  return url;
}

$(function () {
  $("#choose-file-btn").on("click", function () {
    $("#avatar").trigger("click");
  });
  $("#avatar").on("change", function (e) {
    let currentTarget = e.currentTarget;
    let files = currentTarget.files;
    if (files && files.length > 0) {
        $("#avatar-filename").html(files[0].name);
        $("#avatar-tip").html("");
        let _html = "";
        _html += "<div class='simg-item' style='width:80%;margin: 0 auto;'>";
        _html +=
          "<img src='" +
          getObjectURL(files[0]) +
          "' class='card-img-top rounded' />";
        _html += "</div>";
        if ("" !== _html) {
            $("#avatar-box").html(_html);
        }
    }
  });
});
