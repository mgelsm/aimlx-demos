BasicIoLayout.config({
    sampleLink: "argumentation/static/samples.json",
    submitFunction: submit
});

function submit(input) {
    console.log("Argumentation input:", input);
    url = "/argumentation";
    var data = {"input": input};
    $.ajax({
        type: "POST",
        url: url,
        contentType: 'application/json',
        data: JSON.stringify(data, null, '\t'),
        success: function () {
            BasicIoLayout.showResults()
        }
    });
}