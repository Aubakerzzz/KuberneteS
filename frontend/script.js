async function getPrediction() {
  const ticker = document.getElementById("ticker").value;
  const response = await fetch(`http://127.0.0.1:5000/predict?ticker=${ticker}`);
  const data = await response.json();

  document.getElementById("result").textContent = JSON.stringify(data, null, 2);
}
