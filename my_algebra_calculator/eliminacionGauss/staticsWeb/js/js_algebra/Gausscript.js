document.addEventListener('DOMContentLoaded', function () {
    const createMatrixBtn = document.getElementById('createMatrixBtn');
    const matrixContainer = document.getElementById('matrixContainer');
    const resolveBtn = document.getElementById('resolveBtn');
    const resolverForm = document.getElementById('resolverForm');

    // Event listener for creating the matrix
    createMatrixBtn.addEventListener('click', function () {
        const filas = parseInt(document.getElementById('id_filas').value);
        let columnas = parseInt(document.getElementById('id_columnas').value); // Add an extra column

        // Clear previous matrix container
        matrixContainer.innerHTML = '';

        // Validate inputs
        if (!validarEntradas(filas, columnas)) return; 

        // Create and display the matrix
        crearMatriz(filas, columnas);

        // Show the "Resolve" button
        resolveBtn.style.display = 'block';
    });

    // Function to fetch existing table IDs and assign a new one
    async function fetchNewTableId() {
        try {
            const response = await fetch('/get-existing-ids/'); // Use the correct endpoint here
            if (!response.ok) throw new Error('Network response was not ok');

            const data = await response.json();
            console.log('Existing IDs:', data.ids);

            // Determine the next available ID (incrementing from max)
            let newId = data.ids.length > 0 ? Math.max(...data.ids) + 1 : 1;

            return newId;
        } catch (error) {
            console.error('Error fetching table IDs:', error);
            alert('Error al obtener el ID de la tabla.');
            throw error; // Rethrow error to handle it in submit event
        }
    }

    // Event listener for form submission
    resolverForm.addEventListener('submit', async function (event) {
        event.preventDefault(); // Prevent traditional form submission

        try {
            // Get the number of rows and columns
            const filas = parseInt(document.getElementById('id_filas').value);
            const columnas = parseInt(document.getElementById('id_columnas').value) + 1; // Include the extra column

            // Convert matrix inputs to JSON format
            const matriz = obtenerMatriz();

            // Prepare data to send
            const datosAEnviar = {
                EG_matriz: JSON.stringify(matriz) // Convert matrix to JSON string
            };

            // Check if the matrix is valid
            if (datosAEnviar.EG_matriz === '[]') {
                alert('La matriz está vacía o no es válida.');
                return; // Exit the function if the matrix is invalid
            }

            console.log('Datos a enviar:', datosAEnviar); // Log data being sent

            const formData = new URLSearchParams(datosAEnviar); // Format data for sending

            const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value; // Get CSRF token

            // Send data to the server using Fetch API
            const response = await fetch(resolverForm.action, { 
                method: 'POST',
                body: formData,
                headers: {
                    'X-Requested-With': 'XMLHttpRequest',
                    'X-CSRFToken': csrftoken 
                }
            });

            const data = await response.json(); // Parse JSON response

            // Handle server response
            if (data.status === 'success') {
                alert('Datos guardados exitosamente');
                document.getElementById('resultText').textContent = data.resultados; // Show results
            } else {
                let errorMessage = data.message;
                if (data.errors) {
                    errorMessage += '\nErrores específicos:\n' + data.errors.join('\n');
                }
                alert(errorMessage); // Show detailed error message
            }
        } catch (error) {
            console.error('Error:', error);
            alert('Ocurrió un error al enviar los datos.');
        }
    });

    // Function to validate input entries
    function validarEntradas(filas, columnas) {
        if (isNaN(filas) || filas <= 0) {
            alert('Por favor, ingresa un número válido de ecuaciones (mayor que 0).');
            return false;
        }
        if (isNaN(columnas) || columnas <= 0) {
            alert('Por favor, ingresa un número válido de incógnitas (mayor que 0).');
            return false;
        }
        if (filas !== columnas) {
            alert('La matriz debe ser cuadrada, es decir, el número de filas debe ser igual al de columnas.');
            return false;
        }
        return true;
    }

    // Function to create the matrix table
    function crearMatriz(filas, columnas) {
        const table = document.createElement('table');
        table.className = 'table table-bordered'; 

        for (let i = 0; i < filas; i++) {
            const row = document.createElement('tr'); 

            for (let j = 0; j < (columnas + 1); j++) {
                const cell = document.createElement('td'); 
                const input = document.createElement('input'); 

                input.type = 'number';
                input.className = 'form-control'; 
                input.placeholder = `(${i + 1}, ${j + 1})`; 
                input.name = `valor_${i + 1}_${j + 1}`; 

                cell.appendChild(input); 
                row.appendChild(cell); 
            }

            table.appendChild(row); 
        }

        matrixContainer.appendChild(table); 
    }

    // Function to obtain the matrix as a two-dimensional array
    function obtenerMatriz() {
        const filas = parseInt(document.getElementById('id_filas').value);
        const columnas = parseInt(document.getElementById('id_columnas').value) + 1; // Include the extra column
        const matriz = [];
    
        for (let i = 0; i < filas; i++) {
            const fila = [];
            for (let j = 0; j < columnas; j++) {
                const input = document.querySelector(`input[name='valor_${i + 1}_${j + 1}']`);
                const valor = parseFloat(input.value);
                if (isNaN(valor)) {
                    alert(`El valor en la posición (${i + 1}, ${j + 1}) no es un número válido.`);
                    return [];  // Return an empty array to indicate error
                }
                fila.push(valor); 
            }
            matriz.push(fila);
        }
    
        return matriz;
    }
});