
/* -------------------- FUNCIONES UTILITARIAS -------------------- */

function toggleForm(formId) {
  const allForms = document.querySelectorAll('.card[id$="-form"]');
  allForms.forEach(f => f.style.display = 'none');
  const selectedForm = document.getElementById(formId);
  if (selectedForm) selectedForm.style.display = 'block';
}

function mostrarPresupuesto() {
  const tipo = document.getElementById("tipo_categoria").value;
  const presupuestoGroup = document.getElementById("presupuesto-group");
  presupuestoGroup.style.display = tipo === "GASTO" ? "block" : "none";
  if (tipo !== "GASTO") document.getElementById("presupuesto").value = "";
}

function habilitarEdicion(button) {
  const row = button.closest('tr');
  row.querySelector('.nombre-text').style.display = 'none';
  row.querySelector('.nombre-input').style.display = 'inline';
  button.style.display = 'none';
  row.querySelector('.btn-save').style.display = 'inline-block';
  row.querySelector('.btn-cancel').style.display = 'inline-block';
}

function cancelarEdicion(button) {
  const row = button.closest('tr');
  row.querySelector('.nombre-text').style.display = 'inline';
  row.querySelector('.nombre-input').style.display = 'none';
  row.querySelector('.btn-edit').style.display = 'inline-block';
  row.querySelector('.btn-save').style.display = 'none';
  row.querySelector('.btn-cancel').style.display = 'none';
}

async function actualizarTablaCategorias(cuentaId, tipo = "") {
  try {
    const response = await fetch(`/api/categorias?cuenta_id=${cuentaId}&tipo=${tipo}`, {
      method: 'GET',
      credentials: 'include'
    });

    if (response.status === 401) {
      throw new Error("Sesión expirada. Por favor, inicia sesión nuevamente.");
    }

    const contentType = response.headers.get("content-type");
    if (!contentType || !contentType.includes("application/json")) {
      const text = await response.text();
      console.error("❌ Error: El servidor devolvió HTML (posible redirección):", text.slice(0, 200));
      throw new Error("Sesión expirada o error inesperado");
    }

    const categorias = await response.json();
    const tbody = document.getElementById('tabla-categorias');
    tbody.innerHTML = "";

    if (!categorias.length) {
      tbody.innerHTML = '<tr><td colspan="3" style="text-align: center;">No hay categorías para mostrar</td></tr>';
      return;
    }

    categorias.forEach(categoria => {
      const row = document.createElement('tr');
      row.innerHTML = `
        <td>
          <form method="post" action="/categorias/actualizar/${categoria.id}" style="display: inline;">
            <span class="nombre-text">${categoria.nombre}</span>
            <input type="text" name="nombre" class="nombre-input" value="${categoria.nombre}" style="display: none;" required>
            <button type="button" class="btn-edit" onclick="habilitarEdicion(this)"><i class="fas fa-edit"></i></button>
            <button type="button" class="btn-cancel" onclick="cancelarEdicion(this)" style="display: none;"><i class="fas fa-times"></i></button>
            <button type="submit" class="btn-save" style="display: none;"><i class="fas fa-check"></i></button>
          </form>
        </td>
        <td>${categoria.tipo}</td>
        <td>
          <form method="post" action="/categorias/eliminar/${categoria.id}" style="display: inline;">
            <button type="submit" class="btn-delete" onclick="return confirm('¿Estás seguro de eliminar esta categoría?')">
              <i class="fas fa-trash"></i>
            </button>
          </form>
        </td>
      `;
      tbody.appendChild(row);
    });

  } catch (error) {
    console.error("Error al cargar categorías:", error);
    alert(error.message);
  }
}

document.addEventListener('DOMContentLoaded', () => {
  const filtroCuenta = document.getElementById('filtro-cuenta');
  const filtroTipo = document.getElementById('filtro-tipo');

  const handleFilterChange = () => {
    const cuentaId = filtroCuenta.value;
    const tipo = filtroTipo.value;
    actualizarTablaCategorias(cuentaId, tipo);
  };

  filtroCuenta.addEventListener('change', handleFilterChange);
  filtroTipo.addEventListener('change', handleFilterChange);

  const formCategoria = document.getElementById('form-nueva-categoria');
  if (formCategoria) {
    formCategoria.addEventListener('submit', async (e) => {
      e.preventDefault();
      const datos = {
        cuenta_id: formCategoria.cuenta_id.value,
        nombre: formCategoria.nombre.value,
        tipo: formCategoria.tipo.value,
        presupuesto: formCategoria.presupuesto.value
      };

      try {
        const res = await fetch('/api/categorias', {
          method: 'POST',
          credentials: 'include',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(datos)
        });

        if (!res.ok) throw new Error(await res.text());
        const nuevaCategoria = await res.json();

        alert('¡Categoría guardada con éxito!');
        formCategoria.reset();
        document.getElementById('presupuesto-group').style.display = 'none';

        actualizarTablaCategorias(datos.cuenta_id, datos.tipo);
      } catch (err) {
        alert("Error al guardar categoría: " + err.message);
      }
    });
  }

  const formCuenta = document.getElementById('form-nueva-cuenta');
  if (formCuenta) {
    formCuenta.addEventListener('submit', async (e) => {
      e.preventDefault();

      const nombre = document.getElementById('nombre_cuenta').value;
      const saldo = document.getElementById('saldo_inicial').value;

      try {
        const response = await fetch('/api/cuentas', {
          method: 'POST',
          credentials: 'include',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ nombre, saldo_inicial: saldo })
        });

        if (!response.ok) throw new Error(await response.text());
        const result = await response.json();

        alert('Cuenta creada exitosamente');

        const nuevaOpcion = document.createElement('option');
        nuevaOpcion.value = result.cuenta.id;
        nuevaOpcion.textContent = result.cuenta.nombre;
        filtroCuenta.appendChild(nuevaOpcion);
        filtroCuenta.value = result.cuenta.id;

        const selectCategoriaCuenta = document.getElementById('cuenta_id');
        if (selectCategoriaCuenta) {
          const nuevaOpcion2 = document.createElement('option');
          nuevaOpcion2.value = result.cuenta.id;
          nuevaOpcion2.textContent = result.cuenta.nombre;
          selectCategoriaCuenta.appendChild(nuevaOpcion2);
          selectCategoriaCuenta.value = result.cuenta.id;
        }


        actualizarTablaCategorias(result.cuenta.id);
        formCuenta.reset();
        document.getElementById('new-account-form').style.display = 'none';
      } catch (err) {
        alert("Error al crear cuenta: " + err.message);
      }
    });
  }
});
