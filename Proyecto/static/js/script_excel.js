document.getElementById('formImportarExcel').addEventListener('submit', function(event) {
    event.preventDefault();
    const form = event.target;
    const formData = new FormData(form);

    fetch('/importar_excel', {
        method: 'POST',
        body: formData
    })
    .then(response => {
        if (!response.ok) {
            return response.text().then(text => { throw new Error(text) });
        }
        return response.text();  // O .json() si tu backend responde JSON
    })
    .then(result => {
        alert('Importación exitosa.');
        // Si tu backend manda un mensaje, muestra aquí el resultado
        // location.reload(); // Si quieres refrescar los datos automáticamente
    })
    .catch(error => {
        alert('Error al importar: ' + error.message);
    });
});


function exportarExcel() {
    const cuentaId = document.querySelector('select[name="cuenta_id"]').value;
    fetch(`/exportar_excel?cuenta_id=${cuentaId}`)
        .then(response => {
            if (!response.ok) {
                return response.text().then(text => { throw new Error(text) });
            }
            return response.blob();
        })
        .then(blob => {
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = `reporte_cuenta_${cuentaId}.xlsx`;
            document.body.appendChild(a);
            a.click();
            document.body.removeChild(a);
            window.URL.revokeObjectURL(url);
        })
        .catch(error => {
            console.error('Error:', error);
            alert(error.message);
        });
}
