
// https://youtu.be/ot5h1FFy7jk
var output1 = document.getElementById("output1");
var output2 = document.getElementById("output2");
var output3 = document.getElementById("output3");
var ajaxhttp = new XMLHttpRequest();
var url = "data.json"

ajaxhttp.open("GET", url, true);
ajaxhttp.setRequestHeader("content-type", "application/json");
ajaxhttp.onreadystatechange = function () {
    if(ajaxhttp.readyState == 4 && ajaxhttp.status == 200)
    {
        var jcontent = JSON.parse(ajaxhttp.responseText);

        output1.innerHTML = 'Customer: ' + jcontent.customer;
        output2.innerHTML = 'Firmware: ' + jcontent.firmware;
        output3.innerHTML = 'Integrationtest: ' + jcontent.integrationtest;
        
        // Visa objektet i Chrome
        console.log(jcontent);
    }
}

ajaxhttp.send(null)

