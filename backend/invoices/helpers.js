const qr = require("qr-image");

function generateHeader(doc) {
  try {
    doc.image("logo.png", 50, 45, { width: 100 });
  } catch (error) {
    console.error("No se pudo cargar el logo.");
    doc.fontSize(20).text("CineCrisp", 50, 57);
  }

  doc
    .fontSize(10)
    .fillColor("#444444")
    .text("CineCrisp S.R.L.", 200, 50, { align: "right" })
    .text("Calle Ficticia 123, Zona Central", 200, 65, { align: "right" })
    .text("La Paz, Bolivia", 200, 80, { align: "right" })
    .text("NIT: 123456789", 200, 95, { align: "right" });

  doc.moveDown(3);
}

function generateCustomerInformation(doc, invoice) {
  doc.fillColor("#444444").fontSize(18).text("Factura", 50, 160);
  doc.strokeColor("#aaaaaa").lineWidth(1).moveTo(50, 185).lineTo(550, 185).stroke();

  const y = 200;

  doc
    .fontSize(10)
    .text("Nro. de Factura:", 50, y)
    .font("Helvetica-Bold")
    .text(invoice.payment_id, 150, y)
    .font("Helvetica")
    .text("Fecha de Emisión:", 50, y + 15)
    .text(invoice.purchase_date, 150, y + 15)
    .text("Total Pagado:", 50, y + 30)
    .font("Helvetica-Bold")
    .text(`Bs. ${parseFloat(invoice.ticket_price).toFixed(2)}`, 150, y + 30)
    .font("Helvetica-Bold")
    .text("Facturar a:", 350, y)
    .font("Helvetica")
    .text(invoice.customer_email, 350, y + 15);

  doc.strokeColor("#aaaaaa").lineWidth(1).moveTo(50, doc.y + 20).lineTo(550, doc.y + 20).stroke();
}

function generateInvoiceTable(doc, invoice) {
  const yStart = 330;
  const quantity = invoice.seat_names.split(",").length;
  const unitPrice = invoice.ticket_price / quantity;

  doc.font("Helvetica-Bold");
  generateTableRow(doc, yStart, "Descripción", "Precio Unit.", "Cantidad", "Subtotal");
  generateHr(doc, yStart + 20);
  doc.font("Helvetica");

  const description = `${invoice.movie_name}\nCine: ${invoice.theatre_name} - Sala: ${invoice.hall_name}\nFecha: ${invoice.showtime_date} - ${invoice.movie_start_time}\nAsientos: ${invoice.seat_names}`;
  const yRow = yStart + 30;

  generateTableRow(doc, yRow, description, `Bs. ${unitPrice.toFixed(2)}`, quantity, `Bs. ${invoice.ticket_price.toFixed(2)}`);

  generateHr(doc, yRow + 50);
  generateTableRow(doc, yRow + 60, "", "", "Subtotal", `Bs. ${invoice.ticket_price.toFixed(2)}`);
  generateTableRow(doc, yRow + 80, "", "", "Impuestos (IVA 0%)*", "Bs. 0.00");
  doc.font("Helvetica-Bold");
  generateTableRow(doc, yRow + 105, "", "", "TOTAL", `Bs. ${invoice.ticket_price.toFixed(2)}`);
  doc.font("Helvetica");
}

function generateFooter(doc, invoice) {
  const qrText = `https://cinecrisp.com/verificar-factura?id=${invoice.payment_id}`;
  const qrImage = qr.imageSync(qrText, { type: "png" });

  doc.image(qrImage, 70, doc.page.height - 200, { fit: [100, 100] });

  doc
    .fontSize(8)
    .text("Verifique su factura escaneando este código", 50, doc.page.height - 90, { align: "center" })
    .fontSize(9)
    .fillColor("#333333")
    .text("¡Gracias por su compra! Disfrute de la función.", 50, doc.page.height - 180, { align: "center" })
    .fontSize(8)
    .fillColor("#777777")
    .text("*Actividad económica exenta de IVA según normativa vigente.", 50, doc.page.height - 60, { align: "center" });
}

function generateTableRow(doc, y, c1, c2, c3, c4) {
  doc
    .fontSize(10)
    .text(c1, 50, y, { width: 260 })
    .text(c2, 310, y, { width: 90, align: "right" })
    .text(c3, 400, y, { width: 90, align: "right" })
    .text(c4, 500, y, { align: "right" });
}

function generateHr(doc, y) {
  doc
    .strokeColor("#aaaaaa")
    .lineWidth(1)
    .moveTo(50, y)
    .lineTo(550, y)
    .stroke();
}

module.exports = {
  generateHeader,
  generateCustomerInformation,
  generateInvoiceTable,
  generateFooter,
};