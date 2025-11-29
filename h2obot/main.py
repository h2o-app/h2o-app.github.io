from js import document
import json

primary = document.getElementById("primary")
secondary = document.getElementById("secondary")

primary.innerHTML = "Awaiting JSON..."

try:
    with open("/data.json", "r") as file:
        content = file.read()
except Exception as e:
    print(f"An error occurred: {e}")


primary.innerHTML = ""
secondary.innerHTML = ""
questionID = "START"
data = json.loads(content)


def formatAns(text, value):
    return (
        '<button onclick="nextQuestion(this.value,this.innerText)" value="'
        + str(value)
        + '">'
        + text[0]
        + "</button>"
    )


def appendPrimary(text, pos):
    global primary
    if pos == 0:
        primary.insertAdjacentHTML(
            "beforeend", "<div class='leftMessage'>" + text + "</div>"
        )
    elif pos == 1:
        primary.insertAdjacentHTML(
            "beforeend", "<div class='rightMessage'>" + text + "</div>"
        )
    else:
        primary.insertAdjacentHTML("beforeend", text)
    primary.scrollTop = primary.scrollHeight


def addQuestion():
    if questionID == "END":
        appendPrimary("SYSTEM - DATA END", 0)
        secondary.innerHTML = ""
    else:
        appendPrimary(data[questionID]["q"], 0)
        answerList = data[questionID]["a"]
        secondary.innerHTML = "".join(
            list(map(formatAns, answerList, range(len(answerList))))
        )


def addAnswer(num, answer):
    global questionID
    appendPrimary(answer, 1)
    appendPrimary(data[questionID]["a"][num][1], 0)
    questionID = data[questionID]["a"][num][2]
