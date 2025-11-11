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
  document.getElementById("answers").innerHTML = "Loading Pyodide..."
  pyodide = await loadPyodide();
  document.getElementById("answers").innerHTML = "Fetching Data..."
  let AnalyzeR = await fetchData("/AnalyzeR.py")
  let qadata = await fetchData("/qadata.json")
  let start = await fetchData("init.py")
  shownext = await fetchData("shownext.py")
  document.getElementById("answers").innerHTML = "Loading Content..."
  pyodide.FS.writeFile("/home/pyodide/AnalyzeR.py", AnalyzeR)
  pyodide.FS.writeFile("/qadata.json", qadata)
  pyodide.runPython("import AnalyzeR")
  pyodide.runPython(start)
  pyodide.runPython(shownext)
}
async function nextQuestion(value){
  pyodide.runPython("selection = "+value)
  pyodide.runPython(shownext)
}
init();