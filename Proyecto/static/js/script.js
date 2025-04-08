document.addEventListener("DOMContentLoaded", function() {
    fetch('/api/datos')
        .then(response => response.json())
        .then(data => {
            const categorias = data.categoria;
            const presupuestos = data.presupuestos;
            const transacciones = data.transacciones;

            const transaccionesPorCategoria = {};
            categorias.forEach(categoria => {
                transaccionesPorCategoria[categoria.ID_categoria] = [];
            });

            transacciones.forEach(transaccion => {
                const categoriaId = transaccion.ID_Categoria;
                transaccionesPorCategoria[categoriaId].push(transaccion.Monto);
            });

            const etiquetasCategorias = categorias.map(c => c.nombre);

            const datasets = categorias.map(categoria => {
                const data = transaccionesPorCategoria[categoria.ID_categoria] || [];

                return {
                    label: `Transacciones para ${categoria.nombre}`,
                    data: data,
                    backgroundColor: `rgba(${Math.floor(Math.random() * 255)}, ${Math.floor(Math.random() * 255)}, ${Math.floor(Math.random() * 255)}, 0.2)`,
                    borderColor: `rgba(${Math.floor(Math.random() * 255)}, ${Math.floor(Math.random() * 255)}, ${Math.floor(Math.random() * 255)}, 1)`,
                    borderWidth: 1
                };
            });

            const ctxBar = document.getElementById('myChart').getContext('2d');
            new Chart(ctxBar, {
                type: 'bar',
                data: {
                    labels: etiquetasCategorias,
                    datasets: datasets
                },
                options: {
                    scales: {
                        y: {
                            beginAtZero: true
                        }
                    }
                }
            });
        })
        .catch(error => console.error('Error al obtener los datos:', error));
});