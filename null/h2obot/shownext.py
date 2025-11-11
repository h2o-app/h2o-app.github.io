if selection !=-1:
  selected.append(selection)
questionNum += 1

if questionNum >= len(qadata):
  updateQuestion("You're done! Your selections:"+ str(selected))
else:
  question = qadata[questionNum][0]
  answers = qadata[questionNum][1:]
  updateQuestion(question, answers)