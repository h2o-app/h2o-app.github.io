from js import document
import json

primary = document.getElementById("primary")
secondary = document.getElementById("secondary")

primary.innerHTML = "Awaiting JSON..."

try:
    with open("/data.json", "r") as file:
        data = json.loads(file.read())
except Exception as e:
    data = {
        "START": {
            "q": "CRITICAL INTERNAL ERROR -  PLEASE REPORT TO US.",
            "a": [
                [
                    "OK",
                    "Thank you for understanding. we will try and fix the issue ASAP.",
                    "END",
                ]
            ],
        }
    }
    print(f"An error occurred: {e}")


primary.innerHTML = ""
secondary.innerHTML = ""
questionID: str = "START"


def formatAns(text, value) -> str:
    return (
        '<button onclick="nextQuestion(this.value,this.innerText)" value="'
        + str(value)
        + '">'
        + text[0]
        + "</button>"
    )


def appendPrimary(text: str, pos: int):
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
    global questionID
    if questionID == "END":
        appendPrimary("SYSTEM - DATA END", 0)
        secondary.innerHTML = ""
    else:
        appendPrimary(data[questionID]["q"], 0)
        answerList = data[questionID]["a"]
        secondary.innerHTML = "".join(
            list(map(formatAns, answerList, range(len(answerList))))
        )


def addAnswer(num: int, answer: str):
    global questionID
    appendPrimary(answer, 1)
    appendPrimary(data[questionID]["a"][num][1], 0)
    questionID = data[questionID]["a"][num][2]
