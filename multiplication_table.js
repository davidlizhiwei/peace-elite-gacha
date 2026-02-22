const fs = require('fs');
const { Document, Packer, Paragraph, Table, TableRow, TableCell, TextRun, AlignmentType, BorderStyle, ShadingType, WidthType, VerticalAlign } = require('docx');

// Elegant color palette - Chinese traditional colors
const COLORS = {
  primary: "8B0000",      // Deep red - 绛红
  secondary: "D4AF37",    // Gold - 金色
  accent: "1a1a2e",       // Deep navy
  bgWarm: "FFF8F0",       // Warm cream - 米白
  bgLight: "FFFBF0",      // Light cream
  textDark: "2C2C2C",     // Soft black
  textMedium: "5a5a5a",   // Gray
  coral: "FF6B6B",        // Coral for highlights
  teal: "4ECDC4",         // Teal for accents
  lavender: "95A5A6"      // Soft gray-blue
};

// Table border - subtle and elegant
const outerBorder = { style: BorderStyle.SINGLE, size: 8, color: COLORS.primary };
const innerBorder = { style: BorderStyle.SINGLE, size: 1, color: "E8D5C4" };
const cellBordersOuter = {
  top: outerBorder,
  bottom: outerBorder,
  left: outerBorder,
  right: outerBorder
};
const cellBordersInner = {
  top: innerBorder,
  bottom: innerBorder,
  left: innerBorder,
  right: innerBorder
};

// Generate multiplication table rows
const rows = [];

// Header row with gradient-like effect
const headerRowCells = [];

// Top-left corner cell with × symbol
headerRowCells.push(
  new TableCell({
    borders: cellBordersOuter,
    width: { size: 900, type: WidthType.DXA },
    shading: { fill: COLORS.primary, type: ShadingType.CLEAR },
    verticalAlign: VerticalAlign.CENTER,
    children: [new Paragraph({
      alignment: AlignmentType.CENTER,
      children: [new TextRun({
        text: "×",
        bold: true,
        size: 32,
        color: "FFFFFF",
        font: "Georgia"
      })]
    })]
  })
);

// Number headers 1-9
for (let j = 1; j <= 9; j++) {
  headerRowCells.push(
    new TableCell({
      borders: cellBordersInner,
      width: { size: 900, type: WidthType.DXA },
      shading: { fill: COLORS.primary, type: ShadingType.CLEAR },
      verticalAlign: VerticalAlign.CENTER,
      children: [new Paragraph({
        alignment: AlignmentType.CENTER,
        children: [new TextRun({
          text: j.toString(),
          bold: true,
          size: 32,
          color: "FFFFFF",
          font: "Georgia"
        })]
      })]
    })
  );
}
rows.push(new TableRow({ children: headerRowCells }));

// Data rows with alternating subtle pattern
const rowShades = [
  { fill: COLORS.bgWarm, type: ShadingType.CLEAR },
  { fill: COLORS.bgLight, type: ShadingType.CLEAR },
  { fill: "FFF5E6", type: ShadingType.CLEAR },
  { fill: "FAF0E6", type: ShadingType.CLEAR },
  { fill: "FDF5E6", type: ShadingType.CLEAR },
  { fill: "F5F0E6", type: ShadingType.CLEAR },
  { fill: "FFF0F5", type: ShadingType.CLEAR },
  { fill: "F0F5F5", type: ShadingType.CLEAR },
  { fill: "F5F0FF", type: ShadingType.CLEAR }
];

for (let i = 1; i <= 9; i++) {
  const rowCells = [];

  // Row header (1-9)
  rowCells.push(
    new TableCell({
      borders: i === 9 ? {
        top: innerBorder,
        bottom: outerBorder,
        left: outerBorder,
        right: innerBorder
      } : {
        top: innerBorder,
        bottom: innerBorder,
        left: outerBorder,
        right: innerBorder
      },
      width: { size: 900, type: WidthType.DXA },
      shading: { fill: COLORS.secondary, type: ShadingType.CLEAR },
      verticalAlign: VerticalAlign.CENTER,
      children: [new Paragraph({
        alignment: AlignmentType.CENTER,
        children: [new TextRun({
          text: i.toString(),
          bold: true,
          size: 32,
          color: "FFFFFF",
          font: "Georgia"
        })]
      })]
    })
  );

  // Data cells
  for (let j = 1; j <= 9; j++) {
    const product = i * j;
    const isDiagonal = i === j;
    const isPerfectSquare = isDiagonal;

    let cellShading;
    let textColor = COLORS.textDark;
    let isBold = false;

    if (isDiagonal) {
      // Diagonal (perfect squares) - highlight with gold
      cellShading = { fill: "FFF8DC", type: ShadingType.CLEAR };
      textColor = COLORS.primary;
      isBold = true;
    } else {
      cellShading = rowShades[i - 1];
    }

    rowCells.push(
      new TableCell({
        borders: i === 9 && j === 9 ? {
          top: innerBorder,
          bottom: outerBorder,
          left: innerBorder,
          right: outerBorder
        } : i === 9 ? {
          top: innerBorder,
          bottom: outerBorder,
          left: innerBorder,
          right: innerBorder
        } : j === 9 ? {
          top: innerBorder,
          bottom: innerBorder,
          left: innerBorder,
          right: outerBorder
        } : cellBordersInner,
        width: { size: 900, type: WidthType.DXA },
        shading: cellShading,
        verticalAlign: VerticalAlign.CENTER,
        children: [new Paragraph({
          alignment: AlignmentType.CENTER,
          children: [new TextRun({
            text: product.toString(),
            bold: isBold,
            size: 28,
            color: textColor,
            font: "Georgia"
          })]
        })]
      })
    );
  }
  rows.push(new TableRow({ children: rowCells }));
}

// Create the document with elegant styling
const doc = new Document({
  styles: {
    default: {
      document: {
        run: { font: "Georgia", size: 24, color: COLORS.textDark },
        paragraph: { spacing: { before: 0, after: 0 } }
      }
    },
    paragraphStyles: [
      {
        id: "titleStyle",
        name: "Title Style",
        basedOn: "Normal",
        run: {
          font: "Georgia",
          size: 52,
          bold: true,
          color: COLORS.primary,
          smallCaps: true
        },
        paragraph: {
          spacing: { before: 100, after: 50 },
          alignment: AlignmentType.CENTER
        }
      },
      {
        id: "subtitleStyle",
        name: "Subtitle Style",
        basedOn: "Normal",
        run: {
          font: "Georgia",
          size: 26,
          italics: true,
          color: COLORS.textMedium,
          highlight: "transparent"
        },
        paragraph: {
          spacing: { before: 0, after: 300 },
          alignment: AlignmentType.CENTER
        }
      }
    ]
  },
  sections: [{
    properties: {
      page: {
        margin: { top: 1000, right: 800, bottom: 1000, left: 800 },
        size: { orientation: "landscape" }
      }
    },
    children: [
      // Decorative top line
      new Paragraph({
        alignment: AlignmentType.CENTER,
        spacing: { before: 0, after: 50 },
        children: [new TextRun({
          text: "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━",
          size: 20,
          color: COLORS.secondary,
          font: "Arial"
        })]
      }),
      // Main title
      new Paragraph({
        style: "titleStyle",
        children: [new TextRun("乘法口诀表")]
      }),
      // Subtitle
      new Paragraph({
        style: "subtitleStyle",
        children: [new TextRun("The Multiplication Table · 一一得一到九九八十一")]
      }),
      // Decorative bottom line
      new Paragraph({
        alignment: AlignmentType.CENTER,
        spacing: { before: 0, after: 400 },
        children: [new TextRun({
          text: "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━",
          size: 20,
          color: COLORS.secondary,
          font: "Arial"
        })]
      }),
      // The multiplication table
      new Table({
        columnWidths: [900, 900, 900, 900, 900, 900, 900, 900, 900, 900],
        margins: { top: 0, bottom: 0, left: 0, right: 0 },
        rows: rows
      }),
      // Footer decoration
      new Paragraph({
        alignment: AlignmentType.CENTER,
        spacing: { before: 500, after: 100 },
        children: [new TextRun({
          text: "◆  ◆  ◆",
          size: 24,
          color: COLORS.secondary,
          font: "Georgia"
        })]
      }),
      new Paragraph({
        alignment: AlignmentType.CENTER,
        spacing: { before: 0, after: 200 },
        children: [new TextRun({
          text: "Mathematical Foundation · 数学基础",
          size: 18,
          italics: true,
          color: COLORS.textMedium,
          font: "Georgia"
        })]
      })
    ]
  }]
});

// Generate and save the document
Packer.toBuffer(doc).then(buffer => {
  fs.writeFileSync("/Users/davidli/lobsterai/project/乘法口诀表.docx", buffer);
  console.log("✨ 殿堂级乘法口诀表.docx 创建成功！");
}).catch(err => {
  console.error("Error:", err);
});
