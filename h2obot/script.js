async function fetchData(url) {
  try {
    const response = await fetch(url);
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    const data = await response.text();
    return data;
  } catch (error) {
    console.error('Error fetching data:', error);
    return;
  }
}
var pyodide
var next
async function init(){
  document.getElementById("primary").innerHTML = "Loading Pyodide..."
  pyodide = await loadPyodide();
  document.getElementById("primary").innerHTML = "Fetching Data..."
  let AnalyzeR = await fetchData("/AnalyzeR.py")
  let qadata = await fetchData("data.json")
  let start = await fetchData("main.py")
  document.getElementById("primary").innerHTML = "Writing Files..."
  pyodide.FS.writeFile("/home/pyodide/AnalyzeR.py", AnalyzeR)
  pyodide.FS.writeFile("/data.json", qadata)
  document.getElementById("primary").innerHTML = "Awaiting Content..."
  pyodide.runPython("import AnalyzeR")
  pyodide.runPython(start)
  pyodide.runPython("addQuestion()")
}
async function nextQuestion(num,value){
  pyodide.runPython("addAnswer("+num+",'"+value+"')")
  pyodide.runPython("addQuestion()")
}
init();