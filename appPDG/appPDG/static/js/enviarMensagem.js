function enviarMensagem() {
    const mensagemInput = document.querySelector("input[placeholder='Digite sua mensagem...']");
    const mensagemTexto = mensagemInput.value;
    
    fetch("{% url 'enviar_mensagem' %}", {
        method: "POST",
        headers: {
            "Content-Type": "application/x-www-form-urlencoded",
            "X-CSRFToken": "{{ csrf_token }}"
        },
        body: `mensagem=${encodeURIComponent(mensagemTexto)}`
    })
    .then(response => response.json())
    .then(data => {
        if (data.resposta) {
            // Cria o elemento para a resposta do assistente
            const respostaDiv = document.createElement("div");
            respostaDiv.textContent = `IA: ${data.resposta}`;
            
            // Adiciona a resposta ao final do contêiner de mensagens
            const mensagensContainer = document.querySelector(".mensagens-container");
            mensagensContainer.appendChild(respostaDiv);

            // Limpa o campo de entrada
            mensagemInput.value = '';
            
            // Rola automaticamente para a última mensagem adicionada
            mensagensContainer.scrollTop = mensagensContainer.scrollHeight;
        } else {
            alert("Erro ao enviar mensagem.");
        }
    })
    .catch(error => console.error("Erro:", error));
}