async function filtrarTodosGraficos() {
  const dataInicio = document.getElementById("dataInicio").value;
  const dataFim = document.getElementById("dataFim").value;

  const tipos = ["cliente", "movimentacao", "produto", "vendas_por_cliente"];

  for (const tipo of tipos) {
    try {
      const response = await fetch(
        `?tipo=${tipo}&data_inicio=${dataInicio}&data_fim=${dataFim}`,
        {
          headers: { "X-Requested-With": "XMLHttpRequest" },
        }
      );

      if (!response.ok) {
        throw new Error(`Erro ao buscar dados para ${tipo}`);
      }

      const dados = await response.json();

      if (dados.error) {
        alert("Erro: " + dados.error);
        continue;
      }
      if (tipo === "cliente") {
        criarGraficoClientes(dados);
      }
      if (tipo === "movimentacao") {
        criarGraficoMovimentacoes(dados);
      }
      if (tipo === "produto") {
        criarGraficoProdutos(dados);
      }
      if (tipo === "vendas_por_cliente") {
        criarGraficoVendasPorCliente(dados);
      }
    } catch (error) {
      console.error("Erro ao filtrar gráfico:", tipo, error);
    }
  }
}

function criarGraficoLine(ctx, labels, datasets, titleX, titleY) {
  return new Chart(ctx, {
    type: "line",
    data: {
      labels: labels,
      datasets: datasets,
    },
    options: {
      responsive: true,
      tension: 0.1,
      fill: false,
      scales: {
        y: {
          beginAtZero: true,
          title: {
            display: true,
            text: titleX,
          },
        },
        x: {
          title: {
            display: true,
            text: titleY,
          },
          ticks: {
            minRotation: 45,
            maxRotation: 45,
            callback: function (value, index, values) {
              return textTransformEllipsis(
                value,
                index,
                this.chart.data.labels
              );
            },
          },
        },
      },
      plugins: {
        legend: {
          display: true,
          position: "top",
        },
        tooltip: {
          mode: "index",
          intersect: false,
        },
      },
    },
  });
}

function criarGraficoBar(ctx, labels, datasets, titleX, titleY) {
  return new Chart(ctx, {
    type: "bar",
    data: {
      labels: labels,
      datasets: datasets,
    },
    options: {
      responsive: true,
      scales: {
        y: {
          beginAtZero: true,
          ticks: {
            stepSize: 1,
            precision: 0,
          },
          title: {
            display: true,
            text: titleX,
          },
        },
        x: {
          title: {
            display: true,
            text: titleY,
          },
          ticks: {
            minRotation: 45,
            maxRotation: 45,
            callback: function (value, index, values) {
              return textTransformEllipsis(
                value,
                index,
                this.chart.data.labels
              );
            },
          },
        },
      },
      plugins: {
        legend: {
          display: true,
          position: "top",
        },
        tooltip: {
          mode: "index",
          intersect: false,
        },
      },
    },
  });
}

function selecionarAnalisarGrafico() {
  const graficoSelect = document.getElementById("graficoSelect");

  graficoSelect.addEventListener("change", function () {
    const selected = graficoSelect.value;
    const sections = document.querySelectorAll(".grafico");

    if (selected === "todos") {
      sections.forEach((section) => {
        section.style.display = "block";
      });
    } else {
      sections.forEach((section) => {
        if (section.id === `grafico_${selected}`) {
          section.style.display = "block";
        } else {
          section.style.display = "none";
        }
      });
    }
  });
}

function criarGraficoClientes(clientesData) {
  const ctx = document.getElementById("clientesChart").getContext("2d");

  if (charts.clientes) {
    charts.clientes.destroy();
  }

  const labels = clientesData.labels;

  const datasets = [
    {
      label: "Clientes",
      data: clientesData.values,
      backgroundColor: "rgba(54, 162, 235, 0.6)",
      borderColor: "rgba(54, 162, 235, 1)",
      borderWidth: 1,
    },
  ];

  const titleX = "Quantidade de Clientes";
  const titleY = "Período";

  charts.clientes = criarGraficoBar(ctx, labels, datasets, titleX, titleY);
}

function criarGraficoMovimentacoes(movimentacoesData) {
  const ctx = document.getElementById("movimentacoesChart").getContext("2d");

  if (charts.movimentacoes) {
    charts.movimentacoes.destroy();
  }

  const labels = movimentacoesData.labels;

  const datasets = [
    {
      label: "Vendas",
      data: movimentacoesData.vendas,
      borderColor: "#198754",
      backgroundColor: "rgba(25, 135, 84, 0.2)",
      tension: 0.1,
      fill: false,
    },
    {
      label: "Entradas",
      data: movimentacoesData.compras,
      borderColor: "#ffc107",
      backgroundColor: "rgba(255, 193, 7, 0.2)",
      tension: 0.1,
      fill: false,
    },
  ];

  const titleX = "Quantidade de movimentações";
  const titleY = "Período";

  charts.movimentacoes = criarGraficoBar(ctx, labels, datasets, titleX, titleY);
}

function criarGraficoProdutos(produtosData) {
  const ctx = document.getElementById("produtosChart").getContext("2d");

  if (charts.produtos) {
    charts.produtos.destroy();
  }

  const labels = produtosData.labels;

  const datasets = [
    {
      label: "Vendas",
      data: produtosData.vendas,
      borderColor: "#198754",
      backgroundColor: "rgba(25, 135, 84, 0.2)",
      tension: 0.1,
      fill: false,
    },
    {
      label: "Entradas",
      data: produtosData.compras,
      borderColor: "#ffc107",
      backgroundColor: "rgba(255, 193, 7, 0.2)",
      tension: 0.1,
      fill: false,
    },
  ];

  const titleX = "Quantidade de movimentações";
  const titleY = "Produto";

  charts.produtos = criarGraficoLine(ctx, labels, datasets, titleX, titleY);
}

function criarGraficoVendasPorCliente(vendasPorClienteData) {
  const ctx = document.getElementById("vendasPorClienteChart").getContext("2d");

  if (charts.vendas_por_cliente) {
    charts.vendas_por_cliente.destroy();
  }

  const labels = vendasPorClienteData.labels;

  const datasets = [
    {
      label: "Vendas por cliente",
      data: vendasPorClienteData.values,
      backgroundColor: "rgba(255, 159, 64, 0.6)",
      borderColor: "rgba(255, 159, 64, 1)",
      borderWidth: 1,
    },
  ];

  const titleX = "Quantidade de vendas";
  const titleY = "Cliente";

  charts.vendas_por_cliente = criarGraficoBar(
    ctx,
    labels,
    datasets,
    titleX,
    titleY
  );
}

function textTransformEllipsis(value, index, labels) {
  const maxLength = 10;
  let labelValue = value;

  if (Array.isArray(labels) && labels[index]) {
    labelValue = labels[index];
  }

  if (labelValue.length > maxLength) {
    return labelValue.substring(0, maxLength) + "...";
  }
  return labelValue;
}

function isGraficoEmpty(obj) {
  for (const key in obj) {
    if (Array.isArray(obj[key]) && obj[key].length > 0) return false;
    if (obj[key] && !Array.isArray(obj[key])) return false;
  }
  return true;
}

function mensagemGraficoSemDados(elementId) {
  const el = document.getElementById(elementId);
  if (el) {
    el.innerHTML = 'Sem dados.';
    el.style.display = 'block';
  }
}