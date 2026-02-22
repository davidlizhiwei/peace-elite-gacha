const pptxgen = require('pptxgenjs');
const fs = require('fs');

// Elegant Chinese-inspired color palette
const COLORS = {
  primary: "8B0000",      // Deep red - 绛红
  secondary: "D4AF37",    // Gold - 金色
  bgWarm: "FFF8F0",       // Warm cream
  bgLight: "FFFBF0",      // Light cream
  textDark: "2C2C2C",     // Soft black
  textMedium: "5a5a5a",   // Gray
  accent: "C41E3A"        // Cardinal red
};

async function createMultiplicationPPT() {
  const pptx = new pptxgen();
  pptx.layout = 'LAYOUT_16x9';
  pptx.title = '乘法口诀表';
  pptx.author = 'Educational Materials';

  // Slide 1: Title Slide
  const slide1 = pptx.addSlide();

  // Background gradient effect using shape
  slide1.addShape(pptx.shapes.RECTANGLE, {
    x: 0, y: 0, w: '100%', h: '100%',
    fill: { type: 'gradient', color1: COLORS.bgWarm, color2: COLORS.bgLight, angle: 45 }
  });

  // Decorative top band
  slide1.addShape(pptx.shapes.RECTANGLE, {
    x: 0, y: 0, w: '100%', h: 0.8,
    fill: { color: COLORS.primary }
  });

  // Title
  slide1.addText('乘法口诀表', {
    x: 0.5, y: 1.5, w: 9, h: 1.2,
    fontSize: 54,
    bold: true,
    color: COLORS.primary,
    fontFace: 'Georgia',
    align: 'center',
    fill: { type: 'none' }
  });

  // Subtitle
  slide1.addText('The Multiplication Table', {
    x: 0.5, y: 2.5, w: 9, h: 0.6,
    fontSize: 28,
    italics: true,
    color: COLORS.textMedium,
    fontFace: 'Georgia',
    align: 'center'
  });

  // Decorative line
  slide1.addShape(pptx.shapes.LINE, {
    x: 2, y: 3, w: 6, h: 0.1,
    line: { color: COLORS.secondary, width: 3 }
  });

  // Decorative elements
  slide1.addText('◆  ◆  ◆', {
    x: 0.5, y: 3.3, w: 9, h: 0.5,
    fontSize: 24,
    color: COLORS.secondary,
    fontFace: 'Georgia',
    align: 'center'
  });

  // Footer text
  slide1.addText('Mathematical Foundation · 数学基础', {
    x: 0.5, y: 6, w: 9, h: 0.4,
    fontSize: 16,
    italics: true,
    color: COLORS.textMedium,
    fontFace: 'Georgia',
    align: 'center'
  });

  // Slide 2: Complete Multiplication Table
  const slide2 = pptx.addSlide();

  // Background
  slide2.addShape(pptx.shapes.RECTANGLE, {
    x: 0, y: 0, w: '100%', h: 0.6,
    fill: { color: COLORS.primary }
  });

  // Title
  slide2.addText('完整乘法表 (1-9)', {
    x: 0.5, y: 0.1, w: 9, h: 0.5,
    fontSize: 32,
    bold: true,
    color: 'FFFFFF',
    fontFace: 'Georgia',
    align: 'center'
  });

  // Create the multiplication table
  const tableSize = 10; // 1 header + 9 numbers
  const cellWidth = 0.95;
  const cellHeight = 0.7;
  const startX = 0.3;
  const startY = 0.9;

  // Row colors for variety
  const rowColors = [
    COLORS.bgWarm, COLORS.bgLight, "FFF5E6", "FAF0E6",
    "FDF5E6", "F5F0E6", "FFF0F5", "F0F5F5", "F5F0FF", "FFF8DC"
  ];

  for (let i = 0; i < tableSize; i++) {
    for (let j = 0; j < tableSize; j++) {
      const x = startX + j * cellWidth;
      const y = startY + i * cellHeight;

      // Determine cell styling
      let fillColor = rowColors[i];
      let textColor = COLORS.textDark;
      let isBold = false;
      let fontSize = 20;

      // Header row (i=0)
      if (i === 0) {
        fillColor = COLORS.primary;
        textColor = 'FFFFFF';
        isBold = true;
        fontSize = 22;
      }
      // First column (j=0)
      else if (j === 0) {
        fillColor = COLORS.secondary;
        textColor = 'FFFFFF';
        isBold = true;
        fontSize = 22;
      }
      // Diagonal (perfect squares)
      else if (i === j) {
        fillColor = 'FFF8DC';
        textColor = COLORS.primary;
        isBold = true;
        fontSize = 22;
      }

      // Add cell background
      slide2.addShape(pptx.shapes.RECTANGLE, {
        x: x, y: y, w: cellWidth - 0.02, h: cellHeight - 0.02,
        fill: { color: fillColor },
        line: { color: 'E8D5C4', width: 1 },
        rectRadius: 0.1
      });

      // Add cell text
      let cellText = '';
      if (i === 0 && j === 0) {
        cellText = '×';
      } else if (i === 0) {
        cellText = j.toString();
      } else if (j === 0) {
        cellText = i.toString();
      } else {
        cellText = (i * j).toString();
      }

      slide2.addText(cellText, {
        x: x + 0.05, y: y, w: cellWidth - 0.1, h: cellHeight - 0.05,
        fontSize: fontSize,
        bold: isBold,
        color: textColor,
        fontFace: 'Georgia',
        align: 'center',
        valign: 'middle'
      });
    }
  }

  // Slide 3-11: Individual multiplication tables (1-9)
  for (let num = 1; num <= 9; num++) {
    const slide = pptx.addSlide();

    // Header band
    slide.addShape(pptx.shapes.RECTANGLE, {
      x: 0, y: 0, w: '100%', h: 0.7,
      fill: { color: COLORS.primary }
    });

    // Title with current number
    slide.addText(`${num} 的乘法口诀`, {
      x: 0.5, y: 0.1, w: 9, h: 0.6,
      fontSize: 36,
      bold: true,
      color: 'FFFFFF',
      fontFace: 'Georgia',
      align: 'center'
    });

    // Create equations vertically
    const eqY = 1.2;
    const eqHeight = 0.7;

    for (let i = 1; i <= 9; i++) {
      const result = num * i;
      const isHighlighted = i === num; // Highlight the square

      // Background for equation row
      if (isHighlighted) {
        slide.addShape(pptx.shapes.RECTANGLE, {
          x: 1, y: eqY + (i - 1) * eqHeight, w: 8, h: eqHeight - 0.05,
          fill: { color: 'FFF8DC' },
          rectRadius: 0.15
        });
      }

      // Equation text
      const equation = `${num} × ${i} = ${result}`;
      slide.addText(equation, {
        x: 1.5, y: eqY + (i - 1) * eqHeight, w: 7, h: eqHeight - 0.1,
        fontSize: isHighlighted ? 32 : 26,
        bold: isHighlighted,
        color: isHighlighted ? COLORS.primary : COLORS.textDark,
        fontFace: 'Georgia',
        align: 'center',
        valign: 'middle'
      });

      // Chinese mnemonic for common combinations
      const mnemonics = {
        '1 × 1': '一一得一',
        '2 × 2': '二二得四',
        '3 × 3': '三三得九',
        '4 × 4': '四四十六',
        '5 × 5': '五五二十五',
        '6 × 6': '六六三十六',
        '7 × 7': '七七四十九',
        '8 × 8': '八八六十四',
        '9 × 9': '九九八十一'
      };

      if (mnemonics[`${num} × ${i}`]) {
        slide.addText(mnemonics[`${num} × ${i}`], {
          x: 1.5, y: eqY + (i - 1) * eqHeight + 0.35, w: 7, h: 0.3,
          fontSize: 16,
          italics: true,
          color: COLORS.textMedium,
          fontFace: 'Georgia',
          align: 'center'
        });
      }
    }

    // Decorative footer
    slide.addText('━'.repeat(20), {
      x: 0.5, y: 7, w: 9, h: 0.3,
      fontSize: 14,
      color: COLORS.secondary,
      fontFace: 'Arial',
      align: 'center'
    });
  }

  // Save the presentation
  await pptx.writeFile({ fileName: '乘法口诀表.pptx' });
  console.log('✨ 殿堂级乘法口诀表 PPT 创建成功！');
}

createMultiplicationPPT().catch(console.error);
