function abrirModal (nomeModal) {
    var janelaModal = document.querySelector(nomeModal);
    if (janelaModal) {
        janelaModal.style.display = `block`;
    }
}

function fecharModal (nomeModal) {
    var janelaModal = document.querySelector(nomeModal);
    if (janelaModal) {
        janelaModal.style.display = `none`;
    }
}

function submitForm(event) {
    event.preventDefault();

    // Obtém os valores dos inputs
    const nome = document.getElementById('nome_produto').value;
    const marca = document.getElementById('marca').value;
    const valorCompra = document.getElementById('valor_compra').value;
    const quantidade = document.getElementById('quantidade').value;
    const dataValidade = document.getElementById('data-validade').value;

    // Cria um novo cartão com as informações
    const containerCartoes = document.getElementById('container-cartoes');
    const cardDiv = document.createElement('div');
    cardDiv.innerHTML = `
        <div class="card">
            <span>Nome: ${nome}</span>
            <span>Marca: ${marca}</span>
            <span>Valor da Compra: ${valorCompra}</span>
            <span>Quantidade: ${quantidade}</span>
            <span>Data de Validade: ${dataValidade}</span>
        </div>
    `;
    containerCartoes.appendChild(cardDiv);

    // Limpa o formulário e fecha a segunda modal
    document.getElementById('infoForm').reset();
    fecharModal(`.modal`);
}