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

let produtos = [];  // lista para armazenar os produtos cadastrados

// função para adicionar um produto na lista de compras
function adicionarProduto() {
    const nome = document.getElementById('nome').value;
    const marca = document.getElementById('marca').value;
    const valor = parseFloat(document.getElementById('valor').value);
    const quantidade = parseInt(document.getElementById('quantidade').value);
    const data_validade = document.getElementById('data_validade').value;

    // criar um objeto do produto
    const produto = {
        nome: nome,
        marca: marca,
        valor: valor,
        quantidade: quantidade,
        data_validade: data_validade
    };

    // adiciona o produto na lista
    produtos.push(produto);

    // atualiza a lista de produtos no modal
    atualizarListaProdutos();

    // fechar o modal de produto depois adicionar
    fecharModal('.modal', `#backdrop2`);
}

// funcao para exibir os produtos cadastrados no modal
function atualizarListaProdutos() {
    const listaProdutosDiv = document.getElementById('container-cards-produtos');
    listaProdutosDiv.innerHTML = '';

    // loop para criar os cards de produtos
    produtos.forEach(produto => {
        const card = document.createElement('div');
        card.classList.add('card');
        card.innerHTML = `
            <p>Nome: ${produto.nome}</p>
            <p>Marca: ${produto.marca}</p>
            <p>Valor: ${produto.valor}</p>
            <p>Quantidade: ${produto.quantidade}</p>
            <p>Data de Validade: ${produto.data_validade}</p>
        `;
        listaProdutosDiv.appendChild(card);
    });
}

// funcao para confirmar a compra e enviar os dados para o flask
function confirmarCompra() {
    const dataCompra = document.querySelector(`#data`).value;
    const codigoCompra = Math.floor(Math.random() * 10000);

    const compra = {
        data: dataCompra,
        cod: codigoCompra,
        produtos: produtos
    };

    // enviar os dados para o servidor usando fetch
    fetch('/confirmar-compra', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(compra)
    })
    .then(response => {
        return response

    })
    .then(data => {
        alert('Compra confirmada com sucesso!');
        console.log(data)
        // limpar a lista de produtos depois da confirmacao
        produtos = [];
        atualizarListaProdutos();
    })
    .catch(error => {
        console.error('Erro ao confirmar compra:', error);
    });
    fecharModal('.modal-compras', '#backdrop1');
}
