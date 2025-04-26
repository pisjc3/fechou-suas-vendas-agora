function ajustarStepInputQuantidade(unidadeMedidaInput, quantidadeInput) {
  const unidadeMedidaValor =
    unidadeMedidaInput.options[unidadeMedidaInput.selectedIndex].text;

  ajustarStepQuantidadePorValor(unidadeMedidaValor, quantidadeInput);
}

function ajustarStepQuantidadePorValor(unidadeMedidaValor, quantidadeInput) {
  const categoriasInteiras = ["unidade", "caixa", "pacote"];

  if (!quantidadeInput) return;

  const unidade = unidadeMedidaValor.toLowerCase();

  if (categoriasInteiras.some((categoria) => unidade.includes(categoria))) {
    quantidadeInput.step = "1";
  } else {
    quantidadeInput.step = "0.01";
  }

  quantidadeInput.value = ""; 
}

function onInputProdutoChange(callbackFunction) {
  const produtoSelect = document.getElementById("id_produto");

  if (!produtoSelect) return;

  produtoSelect.addEventListener("change", async function () {
    const produtoId = this.value;

    if (!produtoId) return;

    if (callbackFunction) {
      try {
        await callbackFunction(produtoId);
      } catch (error) {
        console.error("Erro na função callback:", error);
      }
    }
  });
}
