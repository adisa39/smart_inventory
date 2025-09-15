document.getElementById("uploadForm").addEventListener("submit", async (e) => {
  e.preventDefault();
  const fileInput = document.getElementById("cameraInput");
  if (!fileInput.files.length) return;

  const formData = new FormData();
  formData.append("file", fileInput.files[0]);

  const res = await fetch("/detect", {
    method: "POST",
    body: formData,
  });

  const data = await res.json();
  const resultsDiv = document.getElementById("results");

  if (data.error) {
    resultsDiv.innerHTML = `<p style="color:red">❌ ${data.error}</p>`;
  } else {
    resultsDiv.innerHTML = `
      <h3>Detections</h3>
      <pre>${JSON.stringify(data.detections, null, 2)}</pre>
      <h3>Summary</h3>
      <pre>${JSON.stringify(data.summary, null, 2)}</pre>
    `;
  }
});
