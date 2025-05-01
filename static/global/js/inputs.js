const TIPOS_UNIDADE_PRODUTO_QUANTIDADE_MEDIDA_INTEIRA = [
  "unidade",
  "caixa",
  "pacote",
];

function ajustarStepInputQuantidade(unidadeMedidaInput, quantidadeInput) {
  if (!unidadeMedidaInput) return;

  unidadeMedidaInput.addEventListener("change", () => {
    const unidadeMedidaValue =
      unidadeMedidaInput.options[unidadeMedidaInput.selectedIndex].text;

    ajustarStepQuantidadePorValor(unidadeMedidaValue, quantidadeInput);
  });
}

function ajustarStepQuantidadePorValor(unidadeMedidaValue, quantidadeInput) {
  if (!quantidadeInput) return;

  const isQuantidadeInteira =
    checkUnidadeProdutoIsQuantidadeMedidaInteira(unidadeMedidaValue);

  if (isQuantidadeInteira) {
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

function getQuantidadeAtualProdutoHelperText(element, produto, label = '') {
  if (!element || !produto) return;

  const { unidade_medida, quantidade_estoque } = produto;

  const isQuantidadeInteira =
    checkUnidadeProdutoIsQuantidadeMedidaInteira(unidade_medida);

  const quantidadeNumerica = parseFloat(quantidade_estoque);
  let quantidadeFormatada;

  if (isNaN(quantidadeNumerica)) {
    element.innerHTML = `<span style="color: red;">Quantidade inválida</span>`;
    return;
  }

  if (isQuantidadeInteira) {
    quantidadeFormatada = String(Math.floor(quantidadeNumerica));
  } else {
    quantidadeFormatada = quantidadeNumerica.toFixed(2).replace(".", ",");
  }

  element.innerHTML = `${label}: <strong>${quantidadeFormatada}</strong> (${unidade_medida})`;
}

function getPrecoProdutoHelperText(element, value, label = '') {
  if (!element || !value) return;

  return (element.innerHTML = `${label}: <strong>${currencyMask(
    value
  )}</strong>`);
}

function checkUnidadeProdutoIsQuantidadeMedidaInteira(unidadeMedida) {
  const unidade = unidadeMedida.toLowerCase();
  return TIPOS_UNIDADE_PRODUTO_QUANTIDADE_MEDIDA_INTEIRA.some((categoria) =>
    unidade.includes(categoria)
  );
}
