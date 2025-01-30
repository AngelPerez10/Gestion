// Función para generar el PDF
const generatePDF = async () => {
    const pdfCanvas = document.createElement("canvas");
    pdfCanvas.width = canvas.width;
    pdfCanvas.height = canvas.height;
    const pdfCtx = pdfCanvas.getContext("2d");
    pdfCtx.drawImage(canvas, 0, 0);

    const imgData = pdfCanvas.toDataURL("image/jpg");

    const A4_WIDTH_MM = 210;
    const A4_HEIGHT_MM = 297;

    const scale = Math.min(
        A4_WIDTH_MM / (canvas.width / 72 * 25.4),
        A4_HEIGHT_MM / (canvas.height / 72 * 25.4)
    );

    const pdfWidth = (canvas.width / 72) * 25.4 * scale;
    const pdfHeight = (canvas.height / 72) * 25.4 * scale;

    const pdf = new window.jspdf.jsPDF("portrait", "mm", [A4_WIDTH_MM, A4_HEIGHT_MM]);
    pdf.addImage(imgData, "jpg", 0, 0, pdfWidth, pdfHeight);

    // Espera a que las fotos se carguen correctamente
    const fotoInicio = new Image();
    fotoInicio.src = orden.foto_inicio;
    await new Promise((resolve) => {
        fotoInicio.onload = () => {
            const imgInicioDataURL = getImageDataURL(fotoInicio);
            pdf.addImage(imgInicioDataURL, "png", 30, pdfHeight + 2, 60, 70);
            pdf.setFontSize(12);
            pdf.text("Foto de Inicio:", 30, pdfHeight + 1);
            resolve();
        };
    });

    const fotoFin = new Image();
    fotoFin.src = orden.foto_fin;
    await new Promise((resolve) => {
        fotoFin.onload = () => {
            const imgFinDataURL = getImageDataURL(fotoFin);
            pdf.addImage(imgFinDataURL, "png", 120, pdfHeight + 2, 60, 70);
            pdf.text("Foto de Termino:", 120, pdfHeight + 1);
            resolve();
        };
    });

    return pdf.output("blob");
};


// Función para convertir la imagen a DataURL
function getImageDataURL(image) {
    const canvas = document.createElement("canvas");
    const ctx = canvas.getContext("2d");
    canvas.width = image.width;
    canvas.height = image.height;
    ctx.drawImage(image, 0, 0);
    return canvas.toDataURL();
}

// Inicialización
document.addEventListener("DOMContentLoaded", () => {
    drawCanvasContent(); // Dibujar el contenido del canvas al cargar la página

    // Evento para enviar el PDF
    document.getElementById("sendPdf").addEventListener("click", sendPDF);
});