from js import document
import json


try:
  with open('/qadata.json', 'r') as file:
      content = file.read()
except Exception as e:
  print(f"An error occurred: {e}")

qadata = json.loads(content)
questionNum = -1
selection = -1
selected = []

def formatAns(text,value):
  return '<button onclick="nextQuestion(this.value)" value="' + str(value) + '">' + text + "</button>"

def updateQuestion(question, answers=[]):
  document.getElementById("question").innerHTML = question
  ans = "<br>".join(list(map(formatAns,answers,range(len(answers)))))
  document.getElementById("answers").innerHTML = ans