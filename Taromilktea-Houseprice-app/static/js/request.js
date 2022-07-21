// BASE_URL = "http://localhost:5000";

let request = function(params) {
  // console.log("method is: ", params.method);
  // console.log("data is: ", params.data);
  const promise = new Promise(function(resolve, reject) {
    $.ajax({
      type: params.method,
      url: params.url,
      data: params.data,
      contentType: params.contentType || "",
      dataType: params.dataType || "json",
      success(res) {
        resolve(res);
      },
      error(res) {
        reject("Response error!");
      }
    });
  });
  return promise;
};
