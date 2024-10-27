async function buscarReceita() {
    const query = document.getElementById('query').value;
    const url = `http://127.0.0.1:8000/receitas/${query}`;
    const resultadoDiv = document.getElementById('resultado');
    const loadingDiv = document.getElementById('loading');
    const voltarBtn = document.getElementById('voltarBtn'); // Botão de voltar

    // Exibe o indicador de carregamento e limpa o conteúdo anterior
    loadingDiv.style.display = "block";
    resultadoDiv.innerHTML = "";
    voltarBtn.style.display = "none"; // Esconde o botão de voltar no início

    try {
        const response = await fetch(url);

        if (!response.ok) {
            throw new Error("Erro ao buscar receita");
        }

        const data = await response.json();

        // Oculta o indicador de carregamento após a resposta
        loadingDiv.style.display = "none";

        // Exibe o conteúdo da receita, se os dados forem válidos
        if (data.ingredientes && data.instrucoes) {
            resultadoDiv.innerHTML = `
                <h2>Ingredientes:</h2>
                <p>${data.ingredientes.replace(/\n/g, "<br>")}</p>
                <h2>Instruções:</h2>
                <p>${data.instrucoes.replace(/\n/g, "<br>")}</p>
            `;
        } else {
            resultadoDiv.innerHTML = "<p>Erro: Receita mal formatada ou incompleta.</p>";
        }

        voltarBtn.style.display = "block"; // Exibe o botão de voltar

    } catch (error) {
        loadingDiv.style.display = "none";
        resultadoDiv.innerHTML = `<p>Erro: ${error.message}</p>`;
    }
}