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

      atualizarGrafico(tipo, dados);
    } catch (error) {
      console.error("Erro ao filtrar gráfico:", tipo, error);
    }
  }
}

function atualizarGrafico(tipo, dados) {
  if (charts[tipo]) {
    charts[tipo].data.labels = dados.labels;
    charts[tipo].data.datasets[0].data = dados.values;
    charts[tipo].update();
  } else {
    console.error("Gráfico não encontrado para o tipo:", tipo);
  }
}

function criarGraficoLine(canvasId, labels, datasets) {
  const ctx = document.getElementById(canvasId).getContext("2d");
  return new Chart(ctx, {
    type: "line",
    data: {
      labels: labels,
      datasets: datasets,
    },
    options: {
      tension: 0.1,
      fill: false,
    },
  });
}

function criarGraficoBar(canvasId, labels, datasets) {
  const ctx = document.getElementById(canvasId).getContext("2d");
  return new Chart(ctx, {
    type: "bar",
    data: {
      labels: labels, 
      datasets: datasets,
    },
    options: {
      responsive: true,
      scales: {
        x: {
          ticks: {
            minRotation: 45,
            maxRotation: 45,
            callback: function (value, index, values) {
              const maxLength = 10; 
              let labelValue = value; 

              if (Array.isArray(labels) && labels[index]) {
                labelValue = labels[index];
              }

              if (labelValue.length > maxLength) {
                return labelValue.substring(0, maxLength) + "...";
              }
              return labelValue;
            },
          },
        },
      },
    },
  });
}

function selecionarAnalisarGrafico(){
  const graficoSelect = document.getElementById('graficoSelect');

  graficoSelect.addEventListener('change', function () {
    const selected = graficoSelect.value;
    const sections = document.querySelectorAll('.grafico');

    if (selected === 'todos') {
      sections.forEach(section => {
        section.style.display = 'block';
      });
    } else {
      sections.forEach(section => {
        if (section.id === `grafico_${selected}`) {
          section.style.display = 'block';
        } else {
          section.style.display = 'none';
        }
      });
    }
  });
}