let firstPageLink
let prevPageLink
let nextPageLink
let lastPageLink

function filterByCode() {
    let code = document.querySelector('#code').value;
    if (code.length === 0) {
        alert("The code field can not be empty!");
        submitOK = "false";
    } else {
        let url = "api/rest/v1/countries/code/" + code;
        createRequest(url, "data")
        document.getElementById("code").value = ""
    }
}

function filterByYear() {
    let year = document.querySelector('#year').value;
    if (year.length === 0) {
        alert("The year field can not be empty!");
        submitOK = "false";
    } else {
        let url = "api/rest/v1/countries/year/" + year;
        createRequest(url, "data")
        document.getElementById("year").value = ""
    }
}

function showAll() {
    let url = "/api/rest/v1/countries";
    createRequest(url, "data")
}

function createNavItems(linkHeader) {
    if (linkHeader) {
        let firstLink = linkHeader.first
        if (!firstLink) {
            disableButton("first")
        } else {
            enableButton("first")
            firstPageLink = firstLink
        }

        let prevLink = linkHeader.prev
        if (!prevLink) {
            disableButton("prev")
        } else {
            enableButton("prev")
            prevPageLink = prevLink
        }

        let nextLink = linkHeader.next
        if (!nextLink) {
            disableButton("next")
        } else {
            enableButton("next")
            nextPageLink = nextLink
        }

        let lastLink = linkHeader.last
        if (!lastLink) {
            disableButton("last")
        } else {
            enableButton("last")
            lastPageLink = lastLink
        }
    } else {
        disableButton("first")
        disableButton("prev")
        disableButton("next")
        disableButton("last")
    }
}

function disableButton(id) {
    document.getElementById(id).disabled = true
}

function enableButton(id) {
    document.getElementById(id).disabled = false
}

function firstPage() {
    createRequest(firstPageLink, "data")
}

function prevPage() {
    createRequest(prevPageLink, "data")
}

function nextPage() {
    createRequest(nextPageLink, "data")
}

function lastPage() {
    createRequest(lastPageLink, "data")
}

function createRequest(url, targetId) {
    let xhr = new XMLHttpRequest();
    xhr.open('GET', url);
    xhr.setRequestHeader("Content-Type", "application/json")
    xhr.onreadystatechange = function () {
        if (xhr.readyState === 4 && xhr.status === 200) {
            const myObj = JSON.parse(this.responseText);
            let text = createText(myObj)
            let linkHeader = JSON.parse(xhr.getResponseHeader("Link"));
            createNavItems(linkHeader)
            document.getElementById(targetId).innerHTML = text;
        } else if (xhr.readyState === 4 && xhr.status !== 200) {
            let errorObject = JSON.parse(this.responseText);
            createErrorField(errorObject);
        }
    }
    xhr.send();
}


function createErrorField(errorObject) {
    let time = errorObject.timestamp;
    let statusCode = errorObject.status;
    let status = errorObject.title;
    let message = errorObject.detail;
    let text = "<table class='table table-bordered text-center table-danger'>";
    text += "<tr class='table-danger'><td>" + time + "</td>";
    text += "<tr class='table-danger'><td>" + statusCode + "</td>";
    text += "<tr class='table-danger'><td>" + status + "</td>";
    text += "<tr class='table-danger'><td>" + message + "</td>";
    text += "</table>";
    disableButton("first")
    disableButton("prev")
    disableButton("next")
    disableButton("last")
    document.getElementById("data").innerHTML = text;
}

function createText(myObj) {
    let text = "<table class='table table-hover table-bordered text-center table-success'>";
    text += "<tr class='table-secondary'><th>" + "Country Name" + "</th><th>" + "Country Code" + "</th><th>" + "Year" + "</th><th>" + "Population" + "</th></tr>";
    for (let x in myObj) {
        text += "<tr><td>" + myObj[x].country_name + "</td>"
            + "<td>" + myObj[x].country_code + "</td>"
            + "<td>" + myObj[x].year + "</td>"
            + "<td>" + myObj[x].population + "</td></tr>";
    }
    text += "</table>"
    return text;
}

