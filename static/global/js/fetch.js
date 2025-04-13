function fetchProdutosPorEmpresa() {
  const empresaSelect = document.getElementById("id_empresa");
  const produtoSelect = document.getElementById("id_produto");

  empresaSelect.addEventListener("change", function () {
    const empresaId = this.value;

    produtoSelect.innerHTML = '<option value="">Carregando...</option>';

    if (!empresaId) {
      produtoSelect.innerHTML =
        '<option value="">Selecione a empresa primeiro</option>';
      return;
    }

    fetch(`/produto/api/produtos-por-empresa/?empresa_id=${empresaId}`)
      .then((response) => response.json())
      .then((data) => {
        produtoSelect.innerHTML =
          '<option value="">Selecione o produto</option>';
        data.forEach((produto) => {
          const option = document.createElement("option");
          option.value = produto.id;
          option.textContent = produto.nome;
          produtoSelect.appendChild(option);
        });
      })
      .catch((error) => {
        console.error("Erro ao buscar produtos:", error);
        produtoSelect.innerHTML =
          '<option value="">Erro ao carregar produtos</option>';
      });
  });
}

function fetchClientesPorEmpresa() {
  const empresaSelect = document.getElementById("id_empresa");
  const clienteSelect = document.getElementById("id_cliente");

  empresaSelect.addEventListener("change", function () {
    const empresaId = this.value;

    clienteSelect.innerHTML = '<option value="">Carregando...</option>';

    if (!empresaId) {
      clienteSelect.innerHTML =
        '<option value="">Selecione a empresa primeiro</option>';
      return;
    }

    fetch(`/cliente/api/clientes-por-empresa/?empresa_id=${empresaId}`)
      .then((response) => response.json())
      .then((data) => {
        clienteSelect.innerHTML =
          '<option value="">Selecione o cliente</option>';
        data.forEach((cliente) => {
          const option = document.createElement("option");
          option.value = cliente.id;
          option.textContent = cliente.nome;
          clienteSelect.appendChild(option);
        });
      })
      .catch((error) => {
        console.error("Erro ao buscar clientes:", error);
        clienteSelect.innerHTML =
          '<option value="">Erro ao carregar clientes</option>';
      });
  });
}
