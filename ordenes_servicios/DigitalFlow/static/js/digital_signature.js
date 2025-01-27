//Archivo: js/digital_signature.js
//Archivo para la funcionalidad de las firmas digitales en las órdenes de servicio

window.onload = function () {
    const encargadoCanvas = document.getElementById('firma_encargado_canvas');
    const clienteCanvas = document.getElementById('firma_cliente_canvas');
    const encargadoCtx = encargadoCanvas.getContext('2d');
    const clienteCtx = clienteCanvas.getContext('2d');

    // Ajuste de tamaño del lienzo dinámicamente
    function resizeCanvas(canvas) {
        canvas.width = canvas.offsetWidth;
        canvas.height = canvas.offsetHeight;
    }

    // Función para inicializar los lienzos cuando el modal es mostrado
    function initializeCanvas(canvas, ctx) {
        resizeCanvas(canvas);
        ctx.strokeStyle = 'black';
        ctx.lineWidth = 2;
    }

    // Función para cargar las firmas desde localStorage
    function loadSignature(canvas, ctx, storageKey) {
        const signatureData = localStorage.getItem(storageKey);
        if (signatureData) {
            const img = new Image();
            img.src = signatureData;
            img.onload = function () {
                ctx.drawImage(img, 0, 0, canvas.width, canvas.height);
            };
        }
    }

    // Esperar a que el modal de firma del encargado se abra
    $('#firmaModalEncargado').on('shown.bs.modal', function () {
        initializeCanvas(encargadoCanvas, encargadoCtx);
        loadSignature(encargadoCanvas, encargadoCtx, 'firma_encargado');
    });

    // Esperar a que el modal de firma del cliente se abra
    $('#firmaModalCliente').on('shown.bs.modal', function () {
        initializeCanvas(clienteCanvas, clienteCtx);
        loadSignature(clienteCanvas, clienteCtx, 'firma_cliente');
    });

    let drawingEncargado = false;
    let drawingCliente = false;

    // Función para obtener las coordenadas del cursor o toque
    function getCursorPosition(canvas, event) {
        const rect = canvas.getBoundingClientRect();
        const touch = event.touches ? event.touches[0] : event; // Usar el primer toque si hay varios
        return {
            x: touch.clientX - rect.left,
            y: touch.clientY - rect.top
        };
    }

    // Función para iniciar el dibujo
    function startDrawing(ctx, canvas, e) {
        const pos = getCursorPosition(canvas, e);
        ctx.beginPath();
        ctx.moveTo(pos.x, pos.y);
        return true;
    }

    // Función para dibujar en el lienzo
    function draw(ctx, canvas, e, drawing) {
        if (drawing) {
            const pos = getCursorPosition(canvas, e);
            ctx.lineTo(pos.x, pos.y);
            ctx.stroke();
        }
    }

    

    // Eventos para el lienzo del encargado
    encargadoCanvas.addEventListener('mousedown', (e) => {
        drawingEncargado = startDrawing(encargadoCtx, encargadoCanvas, e);
    });

    encargadoCanvas.addEventListener('mousemove', (e) => {
        draw(encargadoCtx, encargadoCanvas, e, drawingEncargado);
    });

    encargadoCanvas.addEventListener('mouseup', () => {
        drawingEncargado = false;
    });

    // Nuevos eventos para pantallas táctiles en el lienzo del encargado
    encargadoCanvas.addEventListener('touchstart', (e) => {
        drawingEncargado = startDrawing(encargadoCtx, encargadoCanvas, e);
        e.preventDefault(); // Prevenir el scroll
    });

    encargadoCanvas.addEventListener('touchmove', (e) => {
        draw(encargadoCtx, encargadoCanvas, e, drawingEncargado);
        e.preventDefault(); // Prevenir el scroll
    });

    encargadoCanvas.addEventListener('touchend', () => {
        drawingEncargado = false;
    });

    // Eventos para el lienzo del cliente
    clienteCanvas.addEventListener('mousedown', (e) => {
        drawingCliente = startDrawing(clienteCtx, clienteCanvas, e);
    });

    clienteCanvas.addEventListener('mousemove', (e) => {
        draw(clienteCtx, clienteCanvas, e, drawingCliente);
    });

    clienteCanvas.addEventListener('mouseup', () => {
        drawingCliente = false;
    });

    // Nuevos eventos para pantallas táctiles en el lienzo del cliente
    clienteCanvas.addEventListener('touchstart', (e) => {
        drawingCliente = startDrawing(clienteCtx, clienteCanvas, e);
        e.preventDefault(); // Prevenir el scroll
    });

    clienteCanvas.addEventListener('touchmove', (e) => {
        draw(clienteCtx, clienteCanvas, e, drawingCliente);
        e.preventDefault(); // Prevenir el scroll
    });

    clienteCanvas.addEventListener('touchend', () => {
        drawingCliente = false;
    });

    // Limpiar lienzos
    document.getElementById('clearEncargadoSignature').addEventListener('click', () => {
        encargadoCtx.clearRect(0, 0, encargadoCanvas.width, encargadoCanvas.height);
        localStorage.removeItem('firma_encargado'); // Borrar firma almacenada
    });

    document.getElementById('clearClienteSignature').addEventListener('click', () => {
        clienteCtx.clearRect(0, 0, clienteCanvas.width, clienteCanvas.height);
        localStorage.removeItem('firma_cliente'); // Borrar firma almacenada
    });

};
