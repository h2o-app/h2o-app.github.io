from js import document
import json

primary = document.getElementById("primary")
devInfo = document.getElementById("devInfo")
secondary = document.getElementById("secondary")


with open("/data.json", "r") as file:
    data: dict[str, dict[str, str | list[dict[str, str]]]] = json.loads(file.read())


secondary.innerHTML = ""
questionID: str = "START"


# Convert question option to html button
def formatAns(text: list[str], value: int | str) -> str:
    return (
        '<button class="button" onclick="nextQuestion(this.value,this.innerText)" value="'
        + str(value)
        + '">'
        + text["o"]
        + "</button>"
    )


# Add message to message box
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


# Update Bot after question
def addQuestion():
    global questionID
    if questionID == "END":
        appendPrimary("SYSTEM - DATA END", 0)
        secondary.innerHTML = ""
    else:
        appendPrimary(data[questionID]["q"], 0)
        answerList: list[dict[str, str]] = data[questionID]["a"]
        secondary.innerHTML = "".join(
            list(map(formatAns, answerList, range(len(answerList))))
        )


# Add answer of question to message list
def addAnswer(num: int, answer: str):
    global questionID
    appendPrimary(answer, 1)
    appendPrimary(data[questionID]["a"][num]["r"], 0)
    questionID = data[questionID]["a"][num]["n"]


devInfo.innerHTML += """
OK!<br><b>Starting H2OBot...</b><br><br>
<button class="link cn"onclick="document.getElementById('devInfo').innerHTML = ''">
<b>Hide Initiation Log</b></button><hr><br>
"""
