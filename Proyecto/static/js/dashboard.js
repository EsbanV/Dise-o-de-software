// Función para redirigir según la cuenta seleccionada
function seleccionarCuenta(rutaBase) {
  const select = document.getElementById('cuenta_select');
  if (select && select.value) {
    window.location.href = rutaBase + '?cuenta_id=' + select.value;
  }
}

// Inicialización del gráfico de categorías (pie chart)
function initChartCategorias(labels, values) {
  const ctx = document.getElementById('chart-categorias').getContext('2d');
  new Chart(ctx, {
    type: 'pie',
    data: {
      labels: labels,
      datasets: [{
        data: values,
        backgroundColor: [
          'rgba(255, 99, 132, 0.8)',
          'rgba(54, 162, 235, 0.8)',
          'rgba(255, 206, 86, 0.8)',
          'rgba(75, 192, 192, 0.8)',
          'rgba(153, 102, 255, 0.8)'
        ]
      }]
    },
    options: {
      responsive: true,
      plugins: {
        legend: { position: 'bottom' }
      }
    }
  });
}

// Inicialización del gráfico de movimiento (bar chart)
function initChartDissection(labels, values) {
  const ctx = document.getElementById('chart-dissection').getContext('2d');
  new Chart(ctx, {
    type: 'bar',
    data: {
      labels: labels,
      datasets: [{
        label: 'Movimiento',
        data: values,
        backgroundColor: 'rgba(75, 192, 192, 0.8)'
      }]
    },
    options: {
      responsive: true,
      scales: {
        y: { beginAtZero: true }
      }
    }
  });
}

// Inicialización del gráfico de ingresos vs gastos (line chart)
function initChartIngresosGastos(labels, ingresos, gastos) {
  const ctx = document.getElementById('chart-ingresos-gastos').getContext('2d');
  new Chart(ctx, {
    type: 'line',
    data: {
      labels: labels,
      datasets: [{
        label: 'Ingresos',
        data: ingresos,
        borderColor: 'rgba(54, 162, 235, 1)',
        backgroundColor: 'rgba(54, 162, 235, 0.2)',
        fill: true
      },
      {
        label: 'Gastos',
        data: gastos,
        borderColor: 'rgba(255, 99, 132, 1)',
        backgroundColor: 'rgba(255, 99, 132, 0.2)',
        fill: true
      }]
    },
    options: {
      responsive: true,
      scales: {
        y: { beginAtZero: true }
      }
    }
  });
}

// Datos de ejemplo (estos se deben reemplazar por los datos reales del back-end)
const categoriasLabels = {{ chart_categorias_labels | tojson }};
const categoriasValues = {{ chart_categorias_values | tojson }};
initChartCategorias(categoriasLabels, categoriasValues);

const dissectionLabels = {{ chart_dissection_labels | tojson }};
const dissectionValues = {{ chart_dissection_values | tojson }};
initChartDissection(dissectionLabels, dissectionValues);

const ingresosGastosLabels = {{ chart_ingresos_gastos_labels | tojson }};
const ingresosData = {{ chart_ingresos | tojson }};
const gastosData = {{ chart_gastos | tojson }};
initChartIngresosGastos(ingresosGastosLabels, ingresosData, gastosData);
