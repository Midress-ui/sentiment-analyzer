document.getElementById("form").addEventListener("submit", function(event) {
  event.preventDefault();
  
  let text = document.getElementById("text").value;
  
  // Enviar o texto para o servidor via AJAX
  fetch("/", {
      method: "POST",
      headers: {
          "Content-Type": "application/json",
      },
      body: JSON.stringify({ text: text }),
  })
  .then(response => response.json())
  .then(data => {
      // Atualizar a interface com o resultado
      let resultDiv = document.getElementById("result");
      resultDiv.textContent = `Resultado: ${data.sentiment}`;
      resultDiv.className = `result ${data.sentiment}`;
  });
});
