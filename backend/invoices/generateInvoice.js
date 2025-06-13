const express = require("express");
const router = express.Router();
const PDFDocument = require("pdfkit");

const {
  generateHeader,
  generateCustomerInformation,
  generateInvoiceTable,
  generateFooter,
} = require("./helpers");

router.post("/", (req, res) => {
  const invoice = req.body;

  if (!invoice.ticket_price || !invoice.seat_names) {
    return res.status(400).send("Faltan datos para generar la factura.");
  }

  invoice.ticket_price = parseFloat(invoice.ticket_price);

  const doc = new PDFDocument({ size: "A4", margin: 50 });
  let buffers = [];

  doc.on("data", buffers.push.bind(buffers));
  doc.on("end", () => {
    const pdfData = Buffer.concat(buffers);
    res.setHeader("Content-Type", "application/pdf");
    res.setHeader("Content-Disposition", `attachment; filename=factura_${invoice.payment_id}.pdf`);
    res.send(pdfData);
  });

  generateHeader(doc);
  generateCustomerInformation(doc, invoice);
  generateInvoiceTable(doc, invoice);
  generateFooter(doc, invoice);

  doc.end();
});

module.exports = router;