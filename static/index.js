function abrirModal (nomeModal, nomeBackdrop) {

    ativarBackdrop(nomeBackdrop);

    var janelaModal = document.querySelector(nomeModal);
    if (janelaModal) {
        janelaModal.style.display = `block`;
    }
}

function fecharModal (nomeModal, nomeBackdrop) {
    
    desativarBackdrop(nomeBackdrop);

    var janelaModal = document.querySelector(nomeModal);
    if (janelaModal) {
        janelaModal.style.display = `none`;
    }
}

function ativarBackdrop (idBackdrop) {
    var backdrop = document.querySelector(idBackdrop)
    if (backdrop) {
        backdrop.style.display = `block`;
    }
}

function desativarBackdrop (idBackdrop) {
    var backdrop = document.querySelector(idBackdrop)
    if (backdrop) {
        backdrop.style.display = `none`;
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
    const containerCartoes = document.getElementById('container-cards-produtos');
    const cardDiv = document.createElement('div');
    cardDiv.classList.add(`card`);
    cardDiv.innerHTML = `
        <div>
        <span>Nome: </span> <span class="nome">${nome}</span>
        </div>
        <div>
            <span>Marca: </span> <span class="marca">${marca}</span>
        </div>
        <div>
            <span>Valor da Compra: </span> <span class="valor">${valorCompra}</span>
        </div>
        <div>
            <span>Quantidade: </span> <span class="quantidade">${quantidade}</span>
        </div>
        <div>
            <span>Data de Validade: </span> <span class="data-validade">${dataValidade}</span>
        </div>
    `;
    containerCartoes.appendChild(cardDiv);

    // Limpa o formulário e fecha a segunda modal
    document.getElementById('infoForm').reset();
    fecharModal(`.modal`, `#backdrop2`);
}

function coletarProdutosDoModal () {
    const dataCompra = document.querySelector(`#data`);
    const id = 12345; // gerar id para cada compra

    let produtos = [];
    const conteudoDoModal = document.querySelectorAll(`.card`);
    conteudoDoModal.forEach(card => {
        let produto = {
            nome: card.querySelector(`.nome`).innerHTML,
            nome: card.querySelector(`.marca`).innerHTML,
            nome: card.querySelector(`.valor`).innerHTML,
            nome: card.querySelector(`.quantidade`).innerHTML,
            nome: card.querySelector(`.data-validade`).innerHTML
        };
        produtos.push(produto);
    })
    return produtos;
}
