from js import document

primary = document.getElementById("primary")
primary.innerHTML = ""
secondary = document.getElementById("secondary")
secondary.innerHTML = ""

def formatAns(text,value):
  return '<button onclick="nextQuestion(this.value,this.innerText)" value="' + str(value) + '">' + text + "</button>"

def addQuestion():
  answerList = ["hi","hello","that hurts I think"]
  secondary.innerHTML = "".join(list(map(formatAns,answerList,range(len(answerList)))))

def addAnswer(num,answer):
  primary.scrollTop = primary.scrollHeight
  primary.insertAdjacentHTML('beforeend', "<br>")
  primary.insertAdjacentHTML('beforeend', num)
  primary.insertAdjacentHTML('beforeend', answer)