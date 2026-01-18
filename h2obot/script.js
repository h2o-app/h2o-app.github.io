primary = document.getElementById("primary")
secondary = document.getElementById("secondary")
devInfo = document.getElementById("devInfo")

async function fetchData(url) {
    try {
        const response = await fetch(url);
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        const fetchdata = await response.text();
        return fetchdata;
    } catch (error) {
        console.error('Error fetching data:', error);
        return;
    }
}

// Add delay to code in ms
delay = ms => new Promise(res => setTimeout(res, ms));

function appendPrimary(text, pos) {
    if (pos == 0) {
        primary.insertAdjacentHTML(
            "beforeend", "<div class='leftMessage'>" + text + "</div>"
        )
    } else if (pos == 1) {
        primary.insertAdjacentHTML(
            "beforeend", "<div class='rightMessage'>" + text + "</div>"
        )
    } else {
        primary.insertAdjacentHTML("beforeend", text)
    }
    primary.scrollTop = primary.scrollHeight
}

function addQuestion() {
    if (questionID == "END") {
        appendPrimary("<br>This is the end of your H2OBot History.<br><br>", -1)
    } else {
        appendPrimary(data[questionID]["q"], 0)
    }
}

function addOptions() {
    function formatAns(text) {
        i++
        return (
            '<button class="button" onclick="nextQuestion(this.value,this.innerText)" value="'
            + String(i)
            + '">'
            + String(text["o"])
            + "</button>"
        )
    }
    if (questionID != "END") {
        i = -1
        secondary.innerHTML = data[questionID]["a"].map(x => formatAns(x)).join("")
    }
}

function addResponse(answer) {
    appendPrimary(answer, 1)
    secondary.innerHTML = ""
}

function addAnswer(num) {
    ans = data[questionID]["a"][num]
    appendPrimary(ans["r"], 0)
    questionID = ans["n"]
}

// Initiate on page load
async function init() {
    document.title = "H2OBot " + document.getElementById("version").innerText;
    offlineMode = false;
    enableDownload = false;
    questionID = "START";
    devInfo.innerHTML += " OK!<br>";
    await delay(100);
    if (offlineMode) {
        rawdata = "REPLACE"
        data = JSON.parse(rawdata)
        devInfo.innerHTML += "<b>Viewing in Offline Mode. No Internet Connection Required.</b>"
    } else {
        devInfo.innerHTML += "Fetching JSON Data... "
        data = JSON.parse(await fetchData("data.json"))
        devInfo.innerHTML += " OK!<br>"
        await delay(100)
        devInfo.innerHTML += "<b>Network Requests Complete. No More Internet Connection Required.</b>"
    }
    await delay(100)
    devInfo.innerHTML += (`
        <br><b>Starting H2OBot...</b>
        <br><br>
        <button class="link cn"onclick="document.getElementById('devInfo').innerHTML = ''">
        <b>Hide Initiation Log</b></button>
    `)

    if (!offlineMode && enableDownload) {
        devInfo.innerHTML += (`
        <br><button class="link cn"onclick="downloadPage()">
        <b>Download Offline Version</b></button>
    `)

    }
    devInfo.innerHTML += "<hr><br>"
    // Start the actual bot
    await delay(200)
    primary.innerHTML += "This is the start of your H2OBot History.<br>"
    await delay(200)
    addQuestion()
    await delay(200)
    addOptions()
}

// Run by button press, to add answer to question and then 
async function nextQuestion(num, value) {
    addResponse(value)
    await delay(200)
    addAnswer(num)
    await delay(200)
    addQuestion()
    await delay(200)
    addOptions()
}

async function downloadPage() {
    html = await fetchData("index.html")
    css = await fetchData("../style.css")
    js = await fetchData("script.js")
    json = await fetchData("data.json")

    // Insert CSS into HTML
    cssReplaced = html.replace('<link href="../style.css" rel="stylesheet" type="text/css" />', "<style>" + css + "</style>")

    // change JS for offline mode
    offlineMode = js.replace('offlineMode = false', "offlineMode = true")

    // Insert JSON into JS
    jsonReplaced = offlineMode.replace('rawdata = "REPLACE"', "rawdata = `" + json + "`")

    // Combine HTML and JS changes
    html_json = cssReplaced.replace('<script src="script.js"></scr' + 'ipt>', "<script>" + jsonReplaced + '</scr' + 'ipt>')

    blob = new Blob([html_json], { type: 'text/plain' })
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'H2OBot.html'
    document.body.appendChild(a)
    a.click()
}

document.addEventListener("DOMContentLoaded", function () {
    init();
});