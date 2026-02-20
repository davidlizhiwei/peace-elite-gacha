const fs = require('fs');
const { Document, Packer, Paragraph, TextRun, Table, TableRow, TableCell, Header, Footer,
        AlignmentType, PageOrientation, LevelFormat, HeadingLevel, BorderStyle, WidthType,
        ShadingType, VerticalAlign, TabStopType, TabStopPosition, UnderlineType, PageNumber,
        PageBreak } = require('docx');

// Table border style
const tableBorder = { style: BorderStyle.SINGLE, size: 1, color: "CCCCCC" };
const cellBorders = { top: tableBorder, bottom: tableBorder, left: tableBorder, right: tableBorder };

const doc = new Document({
  styles: {
    default: {
      document: {
        run: { font: "Arial", size: 24 },
        paragraph: { spacing: { line: 360, lineRule: "auto" } }
      }
    },
    paragraphStyles: [
      {
        id: "Title",
        name: "Title",
        basedOn: "Normal",
        run: { size: 44, bold: true, color: "1A1A1A", font: "Arial" },
        paragraph: { spacing: { before: 240, after: 240 }, alignment: AlignmentType.CENTER }
      },
      {
        id: "Heading1",
        name: "Heading 1",
        basedOn: "Normal",
        next: "Normal",
        quickFormat: true,
        run: { size: 32, bold: true, color: "0F4C81", font: "Arial" },
        paragraph: { spacing: { before: 360, after: 240 }, outlineLevel: 0, pageBreakBefore: true }
      },
      {
        id: "Heading2",
        name: "Heading 2",
        basedOn: "Normal",
        next: "Normal",
        quickFormat: true,
        run: { size: 28, bold: true, color: "0F4C81", font: "Arial" },
        paragraph: { spacing: { before: 300, after: 180 }, outlineLevel: 1 }
      },
      {
        id: "Heading3",
        name: "Heading 3",
        basedOn: "Normal",
        next: "Normal",
        quickFormat: true,
        run: { size: 26, bold: true, color: "0F4C81", font: "Arial" },
        paragraph: { spacing: { before: 240, after: 120 }, outlineLevel: 2 }
      },
      {
        id: "Subtitle",
        name: "Subtitle",
        basedOn: "Normal",
        run: { size: 26, italics: true, color: "404040", font: "Arial" },
        paragraph: { spacing: { before: 120, after: 360 }, alignment: AlignmentType.CENTER }
      },
      {
        id: "ExecutiveSummary",
        name: "Executive Summary Box",
        basedOn: "Normal",
        run: { size: 24, font: "Arial" },
        paragraph: {
          spacing: { before: 120, after: 120 },
          indent: { left: 720, right: 720 },
          shading: { fill: "F5F5F5", type: ShadingType.CLEAR }
        }
      }
    ]
  },
  numbering: {
    config: [
      { reference: "bullet-list",
        levels: [{ level: 0, format: LevelFormat.BULLET, text: "•", alignment: AlignmentType.LEFT,
          style: { paragraph: { indent: { left: 720, hanging: 360 } } } }] },
      { reference: "numbered-list",
        levels: [{ level: 0, format: LevelFormat.DECIMAL, text: "%1.", alignment: AlignmentType.LEFT,
          style: { paragraph: { indent: { left: 720, hanging: 360 } } } }] },
      { reference: "letter-list",
        levels: [{ level: 0, format: LevelFormat.LOWER_LETTER, text: "%1)", alignment: AlignmentType.LEFT,
          style: { paragraph: { indent: { left: 720, hanging: 360 } } } }] }
    ]
  },
  sections: [{
    properties: {
      page: {
        margin: { top: 1440, right: 1440, bottom: 1440, left: 1440 },
        size: { orientation: PageOrientation.PORTRAIT }
      }
    },
    headers: {
      default: new Header({
        children: [new Paragraph({
          alignment: AlignmentType.RIGHT,
          children: [new TextRun({ text: "China Innovative Pharma Industry | 2026", size: 18, color: "666666" })]
        })]
      })
    },
    footers: {
      default: new Footer({
        children: [new Paragraph({
          alignment: AlignmentType.CENTER,
          children: [
            new TextRun({ text: "Page ", size: 18 }),
            new TextRun({ children: [PageNumber.CURRENT], size: 18 }),
            new TextRun({ text: "  |  Confidential Report", size: 18, color: "666666" })
          ]
        })]
      })
    },
    children: [
      // Title Page
      new Paragraph({
        heading: HeadingLevel.TITLE,
        children: [new TextRun("China Innovative Pharma\nIndustry Opportunities\nDeep Research Report")]
      }),
      new Paragraph({
        style: "Subtitle",
        children: [new TextRun("McKinsey-Level Strategic Analysis | February 2026")]
      }),

      new Paragraph({ children: [new TextRun("")] }),
      new Paragraph({ children: [new TextRun("")] }),
      new Paragraph({ children: [new TextRun("")] }),

      // Disclaimer box
      new Paragraph({
        shading: { fill: "E8F4F8", type: ShadingType.CLEAR },
        indent: { left: 360, right: 360 },
        children: [
          new TextRun({ text: "Data Sources:\n", bold: true }),
          new TextRun("Reuters, McKinsey, BCG, Deloitte, KPMG, Frost & Sullivan, NHSA, Securities Research Reports\n\n"),
          new TextRun({ text: "Report Generated: ", bold: true }),
          new TextRun("February 20, 2026\n"),
          new TextRun({ text: "Data Cut-off: ", bold: true }),
          new TextRun("Mid-February 2026")
        ]
      }),

      new Paragraph({ children: [new PageBreak()] }),

      // Executive Summary
      new Paragraph({
        heading: HeadingLevel.HEADING_1,
        children: [new TextRun("Executive Summary")]
      }),

      new Paragraph({
        style: "ExecutiveSummary",
        children: [
          new TextRun({ text: "Key Insight", bold: true, color: "0F4C81" }),
          new TextRun("\n\n"),
          new TextRun("China's innovative pharma industry is at a historic inflection point, transitioning from "),
          new TextRun({ text: "follow-on innovation", bold: true }),
          new TextRun(" to "),
          new TextRun({ text: "global leadership", bold: true }),
          new TextRun(". In 2025, total BD transaction value exceeded "),
          new TextRun({ text: "USD 130 billion", bold: true, color: "C00000" }),
          new TextRun(", ranking first globally, marking the "),
          new TextRun({ text: "Year of Value Realization", bold: true }),
          new TextRun(" for China's innovative drugs.")
        ]
      }),

      new Paragraph({ children: [new TextRun("")] }),

      new Paragraph({
        children: [
          new TextRun({ text: "Four Strategic Opportunity Areas", bold: true, color: "0F4C81" }),
        ]
      }),
      new Paragraph({
        numbering: { reference: "bullet-list", level: 0 },
        children: [new TextRun({ text: "Overseas BD Licensing: 2025 BD value USD 130B, 2026 YTD exceeded USD 30B, China R&D efficiency leads globally" })]
      }),
      new Paragraph({
        numbering: { reference: "bullet-list", level: 0 },
        children: [new TextRun({ text: "Technology Breakthroughs: ADC and bispecific antibodies have surpassed Europe/US, becoming global innovation hubs" })]
      }),
      new Paragraph({
        numbering: { reference: "bullet-list", level: 0 },
        children: [new TextRun({ text: "Policy Dividends: Dual-directory system (National Reimbursement + Commercial Insurance) drives market access" })]
      }),
      new Paragraph({
        numbering: { reference: "bullet-list", level: 0 },
        children: [new TextRun({ text: "Supply Chain Rise: CRO/CDMO transitioning from follower to leader, domestic substitution accelerating" })]
      }),

      new Paragraph({ children: [new TextRun("")] }),

      new Paragraph({
        children: [
          new TextRun({ text: "2026 Three Investment Themes", bold: true, color: "0F4C81" }),
        ]
      }),
      new Paragraph({
        numbering: { reference: "numbered-list", level: 0 },
        children: [new TextRun({ text: "Global Expansion: ADC, bispecific antibodies, small molecule targeted therapies", bold: true })]
      }),
      new Paragraph({
        numbering: { reference: "numbered-list", level: 0 },
        children: [new TextRun({ text: "Supply Chain Upgrade: CRO, CDMO, upstream equipment/materials", bold: true })]
      }),
      new Paragraph({
        numbering: { reference: "numbered-list", level: 0 },
        children: [new TextRun({ text: "Frontier Technologies: Cell therapy, gene therapy, weight loss drugs", bold: true })]
      }),

      new Paragraph({ children: [new PageBreak()] }),

      // Chapter 1
      new Paragraph({
        heading: HeadingLevel.HEADING_1,
        children: [new TextRun("Chapter 1: China's Position in Global Pharma Landscape")]
      }),

      new Paragraph({
        heading: HeadingLevel.HEADING_2,
        children: [new TextRun("1.1 Reshaping of Global Biopharma Landscape")]
      }),

      new Paragraph({
        children: [
          new TextRun("According to McKinsey's latest research, Asia is becoming the "),
          new TextRun({ text: "emerging epicenter", bold: true }),
          new TextRun(" of global biopharma. China is reshaping the global innovative pharma landscape with the following core advantages:")
        ]
      }),

      new Paragraph({ children: [new TextRun("")] }),

      // Table 1: China's Core Advantages
      new Table({
        columnWidths: [2340, 7020],
        margins: { top: 100, bottom: 100, left: 180, right: 180 },
        rows: [
          new TableRow({
            tableHeader: true,
            children: [
              new TableCell({
                borders: cellBorders,
                width: { size: 2340, type: WidthType.DXA },
                shading: { fill: "0F4C81", type: ShadingType.CLEAR },
                verticalAlign: VerticalAlign.CENTER,
                children: [new Paragraph({
                  alignment: AlignmentType.CENTER,
                  children: [new TextRun({ text: "Core Advantage", bold: true, size: 22, color: "FFFFFF" })]
                })]
              }),
              new TableCell({
                borders: cellBorders,
                width: { size: 7020, type: WidthType.DXA },
                shading: { fill: "0F4C81", type: ShadingType.CLEAR },
                verticalAlign: VerticalAlign.CENTER,
                children: [new Paragraph({
                  alignment: AlignmentType.CENTER,
                  children: [new TextRun({ text: "Key Manifestations", bold: true, size: 22, color: "FFFFFF" })]
                })]
              })
            ]
          }),
          new TableRow({
            children: [
              new TableCell({
                borders: cellBorders,
                width: { size: 2340, type: WidthType.DXA },
                children: [new Paragraph({
                  children: [new TextRun({ text: "R&D Efficiency", bold: true })]
                })]
              }),
              new TableCell({
                borders: cellBorders,
                width: { size: 7020, type: WidthType.DXA },
                children: [
                  new Paragraph({ numbering: { reference: "bullet-list", level: 0 }, children: [new TextRun("Clinical trial speed 30-50% faster than US/EU")] }),
                  new Paragraph({ numbering: { reference: "bullet-list", level: 0 }, children: [new TextRun("Patient recruitment 3-5x faster")] }),
                  new Paragraph({ numbering: { reference: "bullet-list", level: 0 }, children: [new TextRun("R&D cost only 1/3-1/2 of Western countries")] })
                ]
              })
            ]
          }),
          new TableRow({
            children: [
              new TableCell({
                borders: cellBorders,
                width: { size: 2340, type: WidthType.DXA },
                children: [new Paragraph({
                  children: [new TextRun({ text: "Engineer Dividend", bold: true })]
                })]
              }),
              new TableCell({
                borders: cellBorders,
                width: { size: 7020, type: WidthType.DXA },
                children: [
                  new Paragraph({ numbering: { reference: "bullet-list", level: 0 }, children: [new TextRun("100,000+ biopharma graduates annually")] }),
                  new Paragraph({ numbering: { reference: "bullet-list", level: 0 }, children: [new TextRun("R&D personnel cost only 1/4 of Western countries")] }),
                  new Paragraph({ numbering: { reference: "bullet-list", level: 0 }, children: [new TextRun("Returning overseas talent brings international experience")] })
                ]
              })
            ]
          }),
          new TableRow({
            children: [
              new TableCell({
                borders: cellBorders,
                width: { size: 2340, type: WidthType.DXA },
                children: [new Paragraph({
                  children: [new TextRun({ text: "Market Size", bold: true })]
                })]
              }),
              new TableCell({
                borders: cellBorders,
                width: { size: 7020, type: WidthType.DXA },
                children: [
                  new Paragraph({ numbering: { reference: "bullet-list", level: 0 }, children: [new TextRun("World's 2nd largest pharma market, >RMB 1.8T in 2025")] }),
                  new Paragraph({ numbering: { reference: "bullet-list", level: 0 }, children: [new TextRun("Innovative drug penetration increased from 25% (2020) to 45% (2025)")] }),
                  new Paragraph({ numbering: { reference: "bullet-list", level: 0 }, children: [new TextRun("Enhanced reimbursement capability supports true innovation")] })
                ]
              })
            ]
          }),
          new TableRow({
            children: [
              new TableCell({
                borders: cellBorders,
                width: { size: 2340, type: WidthType.DXA },
                children: [new Paragraph({
                  children: [new TextRun({ text: "Complete Supply Chain", bold: true })]
                })]
              }),
              new TableCell({
                borders: cellBorders,
                width: { size: 7020, type: WidthType.DXA },
                children: [
                  new Paragraph({ numbering: { reference: "bullet-list", level: 0 }, children: [new TextRun("World-class CRO/CDMO: WuXi AppTec, Pharmaron, etc.")] }),
                  new Paragraph({ numbering: { reference: "bullet-list", level: 0 }, children: [new TextRun("Most complete API supply chain globally")] }),
                  new Paragraph({ numbering: { reference: "bullet-list", level: 0 }, children: [new TextRun("Accelerating domestic substitution in equipment/consumables")] })
                ]
              })
            ]
          })
        ]
      }),

      new Paragraph({ children: [new TextRun("")] }),

      new Paragraph({
        heading: HeadingLevel.HEADING_2,
        children: [new TextRun("1.2 China's Global Status Leap in Innovative Drugs")]
      }),

      new Paragraph({
        children: [
          new TextRun("2025 is a milestone year for China's innovative pharma industry, with multiple indicators ranking first globally:")
        ]
      }),

      new Paragraph({ children: [new TextRun("")] }),

      new Paragraph({
        shading: { fill: "FFF2CC", type: ShadingType.CLEAR },
        indent: { left: 360, right: 360 },
        children: [
          new TextRun({ text: "Key Data Highlights", bold: true, color: "B7791F" }),
          new TextRun("\n\n"),
          new TextRun({ text: "✓  Total BD Value: ", bold: true }),
          new TextRun({ text: "USD 130 billion", bold: true, color: "C00000" }),
          new TextRun(" (No.1 globally, surpassing US)\n"),
          new TextRun({ text: "✓  2026 YTD BD: ", bold: true }),
          new TextRun({ text: ">USD 30 billion", bold: true, color: "C00000" }),
          new TextRun(" (Record-breaking)\n"),
          new TextRun({ text: "✓  Overseas Revenue: ", bold: true }),
          new TextRun({ text: "RMB 940 billion", bold: true, color: "C00000" }),
          new TextRun(" (Full year 2025)\n"),
          new TextRun({ text: "✓  Financing: ", bold: true }),
          new TextRun({ text: "USD 14.7 billion", bold: true, color: "C00000" }),
          new TextRun(" (2025, significant YoY growth)\n"),
          new TextRun({ text: "✓  ADC Clinical Trials: ", bold: true }),
          new TextRun({ text: "No.1 globally", bold: true, color: "C00000" }),
          new TextRun(" (>40% of global total)")
        ]
      }),

      new Paragraph({ children: [new PageBreak()] }),

      // Chapter 2
      new Paragraph({
        heading: HeadingLevel.HEADING_1,
        children: [new TextRun("Chapter 2: Deep Analysis of Core Opportunities")]
      }),

      new Paragraph({
        heading: HeadingLevel.HEADING_2,
        children: [new TextRun("2.1 Overseas BD Licensing: Most Certain Opportunity")]
      }),

      new Paragraph({
        children: [
          new TextRun("Overseas expansion for Chinese innovative drugs has shifted from "),
          new TextRun({ text: "optional", bold: true }),
          new TextRun(" to "),
          new TextRun({ text: "mandatory", bold: true }),
          new TextRun(", with BD licensing becoming the core path for value realization.")
        ]
      }),

      new Paragraph({ children: [new TextRun("")] }),

      new Paragraph({
        children: [new TextRun({ text: "(1) Explosive Growth in Transaction Scale", bold: true })]
      }),
      new Paragraph({
        children: [
          new TextRun("China's innovative drug BD transactions showed "),
          new TextRun({ text: "explosive growth", bold: true }),
          new TextRun(" in 2025:")
        ]
      }),
      new Paragraph({
        numbering: { reference: "bullet-list", level: 0 },
        children: [new TextRun("Full-year 2025 BD value reached USD 130B, first time ranking No.1 globally")]
      }),
      new Paragraph({
        numbering: { reference: "bullet-list", level: 0 },
        children: [new TextRun("2026 YTD (2 months) BD exceeded USD 30B, breaking historical records")]
      }),
      new Paragraph({
        numbering: { reference: "bullet-list", level: 0 },
        children: [new TextRun("License-out transactions account for >80%, international recognition of China R&D capability")]
      }),
      new Paragraph({
        numbering: { reference: "bullet-list", level: 0 },
        children: [new TextRun("Average deal size continues to increase, upfront payment ratios significantly improved")]
      }),

      new Paragraph({ children: [new TextRun("")] }),

      new Paragraph({
        children: [new TextRun({ text: "(2) Driver Analysis", bold: true })]
      }),
      new Paragraph({
        children: [
          new TextRun("The explosion in China's innovative drug BD is not accidental, but the result of multiple converging factors:")
        ]
      }),

      new Table({
        columnWidths: [3510, 5850],
        margins: { top: 100, bottom: 100, left: 180, right: 180 },
        rows: [
          new TableRow({
            tableHeader: true,
            children: [
              new TableCell({
                borders: cellBorders,
                width: { size: 3510, type: WidthType.DXA },
                shading: { fill: "D5E8F0", type: ShadingType.CLEAR },
                children: [new Paragraph({
                  alignment: AlignmentType.CENTER,
                  children: [new TextRun({ text: "Driver", bold: true, size: 20 })]
                })]
              }),
              new TableCell({
                borders: cellBorders,
                width: { size: 5850, type: WidthType.DXA },
                shading: { fill: "D5E8F0", type: ShadingType.CLEAR },
                children: [new Paragraph({
                  alignment: AlignmentType.CENTER,
                  children: [new TextRun({ text: "Key Manifestations", bold: true, size: 20 })]
                })]
              })
            ]
          }),
          new TableRow({
            children: [
              new TableCell({
                borders: cellBorders,
                width: { size: 3510, type: WidthType.DXA },
                children: [new Paragraph({
                  children: [new TextRun({ text: "Supply Side: Asset Quality Improvement", bold: true })]
                })]
              }),
              new TableCell({
                borders: cellBorders,
                width: { size: 5850, type: WidthType.DXA },
                children: [
                  new Paragraph({ numbering: { reference: "bullet-list", level: 0 }, children: [new TextRun("Clinical data quality reaches international standards")] }),
                  new Paragraph({ numbering: { reference: "bullet-list", level: 0 }, children: [new TextRun("FIC/BIC proportion increases, clear differentiation")] }),
                  new Paragraph({ numbering: { reference: "bullet-list", level: 0 }, children: [new TextRun("Global leadership in ADC, bispecific antibodies")] })
                ]
              })
            ]
          }),
          new TableRow({
            children: [
              new TableCell({
                borders: cellBorders,
                width: { size: 3510, type: WidthType.DXA },
                children: [new Paragraph({
                  children: [new TextRun({ text: "Demand Side: MNC Pipeline Pressure", bold: true })]
                })]
              }),
              new TableCell({
                borders: cellBorders,
                width: { size: 5850, type: WidthType.DXA },
                children: [
                  new Paragraph({ numbering: { reference: "bullet-list", level: 0 }, children: [new TextRun("Patent cliff approaching: >USD 150B sales face patent expiry 2025-2030")] }),
                  new Paragraph({ numbering: { reference: "bullet-list", level: 0 }, children: [new TextRun("Declining internal R&D efficiency, need external pipeline supplementation")] }),
                  new Paragraph({ numbering: { reference: "bullet-list", level: 0 }, children: [new TextRun("China assets offer high cost-performance, fast R&D speed")] })
                ]
              })
            ]
          }),
          new TableRow({
            children: [
              new TableCell({
                borders: cellBorders,
                width: { size: 3510, type: WidthType.DXA },
                children: [new Paragraph({
                  children: [new TextRun({ text: "Capital Side: Improved Financing", bold: true })]
                })]
              }),
              new TableCell({
                borders: cellBorders,
                width: { size: 5850, type: WidthType.DXA },
                children: [
                  new Paragraph({ numbering: { reference: "bullet-list", level: 0 }, children: [new TextRun("2025 financing USD 14.7B, significant YoY growth")] }),
                  new Paragraph({ numbering: { reference: "bullet-list", level: 0 }, children: [new TextRun("HK IPO market warming up, Biotech listing channel reopening")] }),
                  new Paragraph({ numbering: { reference: "bullet-list", level: 0 }, children: [new TextRun("BD income becoming important cash flow source")] })
                ]
              })
            ]
          })
        ]
      }),

      new Paragraph({ children: [new TextRun("")] }),

      new Paragraph({
        children: [new TextRun({ text: "(3) Key Therapeutic Areas", bold: true })]
      }),
      new Paragraph({
        children: [
          new TextRun("According to BCG and Reuters analysis, the following areas have the greatest BD potential:")
        ]
      }),
      new Paragraph({
        numbering: { reference: "letter-list", level: 0 },
        children: [new TextRun({ text: "Oncology: ADC, bispecific antibodies, cell therapy (60%+ of BD transactions)", bold: true })]
      }),
      new Paragraph({
        numbering: { reference: "letter-list", level: 0 },
        children: [new TextRun({ text: "Metabolic Diseases: GLP-1 targets and related combination therapies", bold: true })]
      }),
      new Paragraph({
        numbering: { reference: "letter-list", level: 0 },
        children: [new TextRun({ text: "Autoimmune: IL-17, IL-23, JAK inhibitors, etc.", bold: true })]
      }),
      new Paragraph({
        numbering: { reference: "letter-list", level: 0 },
        children: [new TextRun({ text: "CNS: Alzheimer's, Parkinson's disease, etc.", bold: true })]
      }),

      new Paragraph({ children: [new TextRun("")] }),

      new Paragraph({
        children: [new TextRun({ text: "(4) Challenges and Risks", bold: true })]
      }),
      new Paragraph({
        children: [
          new TextRun("Despite optimistic prospects, overseas expansion still faces the following challenges:")
        ]
      }),
      new Paragraph({
        numbering: { reference: "bullet-list", level: 0 },
        children: [new TextRun("Geopolitical risks: US-China relations may affect FDA approval and commercialization")]
      }),
      new Paragraph({
        numbering: { reference: "bullet-list", level: 0 },
        children: [new TextRun("Clinical standard differences: Different endpoint requirements in US/EU/China require trial redesign")]
      }),
      new Paragraph({
        numbering: { reference: "bullet-list", level: 0 },
        children: [new TextRun("Insufficient commercialization capability: Lack of overseas sales teams and experience")]
      }),
      new Paragraph({
        numbering: { reference: "bullet-list", level: 0 },
        children: [new TextRun("Deal term negotiations: MNC price pressure, strict milestones, royalty disputes")]
      }),

      new Paragraph({ children: [new PageBreak()] }),

      // Chapter 2.2
      new Paragraph({
        heading: HeadingLevel.HEADING_2,
        children: [new TextRun("2.2 Technology Tracks: Global Leadership in ADC and Bispecific Antibodies")]
      }),

      new Paragraph({
        children: [
          new TextRun("China has achieved a leap from "),
          new TextRun({ text: "following", bold: true }),
          new TextRun(" to "),
          new TextRun({ text: "leading", bold: true }),
          new TextRun(" in ADC (Antibody-Drug Conjugates) and bispecific antibodies, becoming a global innovation hub.")
        ]
      }),

      new Paragraph({ children: [new TextRun("")] }),

      new Paragraph({
        children: [new TextRun({ text: "(1) ADC: China Has Surpassed Europe and US", bold: true })]
      }),

      new Paragraph({
        shading: { fill: "E8F4F8", type: ShadingType.CLEAR },
        indent: { left: 360, right: 360 },
        children: [
          new TextRun({ text: "ADC Market Data", bold: true, color: "0F4C81" }),
          new TextRun("\n\n"),
          new TextRun({ text: "•  Global ADC Market: ", bold: true }),
          new TextRun("~USD 10B in 2025, >USD 30B expected by 2030\n"),
          new TextRun({ text: "•  China ADC Clinical Trials: ", bold: true }),
          new TextRun({ text: "No.1 globally", bold: true }),
          new TextRun(" (>40% of global total)\n"),
          new TextRun({ text: "•  China ADC BD Deals: ", bold: true }),
          new TextRun(">USD 50B in 2025 (40% of total BD)\n"),
          new TextRun({ text: "•  Key Players: ", bold: true }),
          new TextRun("SystImmune, Kelun-Biotech, Hengrui, RemeGen, ImmunoGen China, etc.")
        ]
      }),

      new Paragraph({ children: [new TextRun("")] }),

      new Paragraph({
        children: [new TextRun({ text: "China's ADC Core Advantages:", bold: true })]
      }),
      new Paragraph({
        numbering: { reference: "bullet-list", level: 0 },
        children: [new TextRun("Linker-payload technology breakthroughs: Novel linkers, efficient payloads, site-specific conjugation mature")]
      }),
      new Paragraph({
        numbering: { reference: "bullet-list", level: 0 },
        children: [new TextRun("Bispecific ADC leadership: SystImmune, Conmed, etc. have rich bispecific ADC pipelines")]
      }),
      new Paragraph({
        numbering: { reference: "bullet-list", level: 0 },
        children: [new TextRun("Fast clinical development: Rapid patient recruitment, high trial efficiency")]
      }),
      new Paragraph({
        numbering: { reference: "bullet-list", level: 0 },
        children: [new TextRun("Complete CDMO ecosystem: WuXi XDC, DuXi Biologics provide one-stop ADC CDMO services")]
      }),

      new Paragraph({ children: [new TextRun("")] }),

      new Paragraph({
        children: [new TextRun({ text: "(2) Bispecific Antibodies: Next-Gen Immunotherapy主力", bold: true })]
      }),
      new Paragraph({
        children: [
          new TextRun("Bispecific antibodies, with their unique ability to bind two targets simultaneously, are becoming the new mainstay of tumor immunotherapy:")
        ]
      }),
      new Paragraph({
        numbering: { reference: "bullet-list", level: 0 },
        children: [new TextRun("China has No.1 bispecific antibody clinical trials globally, >35% of global total")]
      }),
      new Paragraph({
        numbering: { reference: "bullet-list", level: 0 },
        children: [new TextRun("Akeso, SystImmune, Innovent have multiple bispecifics approved or in late-stage trials")]
      }),
      new Paragraph({
        numbering: { reference: "bullet-list", level: 0 },
        children: [new TextRun("Bispecific+ADC combination emerging as new trend, significant synergistic effects")]
      }),

      new Paragraph({ children: [new TextRun("")] }),

      new Paragraph({
        children: [new TextRun({ text: "(3) Other Frontier Technology Layout", bold: true })]
      }),
      new Paragraph({
        children: [
          new TextRun("Chinese innovative pharma companies are actively布局 in the following frontier technology directions:")
        ]
      }),
      new Paragraph({
        numbering: { reference: "bullet-list", level: 0 },
        children: [new TextRun("Cell Therapy (CAR-T): Legend Biotech, CARsgen, WuXi JuNuo lead globally; 9 CGT products approved in China")]
      }),
      new Paragraph({
        numbering: { reference: "bullet-list", level: 0 },
        children: [new TextRun("Gene Therapy: AAV vectors, CRISPR gene editing technology actively being developed")]
      }),
      new Paragraph({
        numbering: { reference: "bullet-list", level: 0 },
        children: [new TextRun("Weight Loss Drugs: GLP-1, GIP/GLP-1 dual agonists, oral GLP-1 rich pipelines")]
      }),
      new Paragraph({
        numbering: { reference: "bullet-list", level: 0 },
        children: [new TextRun("Brain-Computer Interface: Chinese companies actively布局 in medical applications")]
      }),

      new Paragraph({ children: [new PageBreak()] }),

      // Chapter 2.3
      new Paragraph({
        heading: HeadingLevel.HEADING_1,
        children: [new TextRun("Chapter 3: Investment Strategy and Recommendations for 2026")]
      }),

      new Paragraph({
        heading: HeadingLevel.HEADING_2,
        children: [new TextRun("3.1 Three Investment Themes")]
      }),

      new Paragraph({
        children: [
          new TextRun("Based on deep research, we propose "),
          new TextRun({ text: "three investment themes", bold: true }),
          new TextRun(" for China's innovative pharma industry in 2026:")
        ]
      }),

      new Paragraph({ children: [new TextRun("")] }),

      // Table: Three Investment Themes
      new Table({
        columnWidths: [2340, 3510, 3510],
        margins: { top: 100, bottom: 100, left: 180, right: 180 },
        rows: [
          new TableRow({
            tableHeader: true,
            children: [
              new TableCell({
                borders: cellBorders,
                width: { size: 2340, type: WidthType.DXA },
                shading: { fill: "0F4C81", type: ShadingType.CLEAR },
                verticalAlign: VerticalAlign.CENTER,
                children: [new Paragraph({
                  alignment: AlignmentType.CENTER,
                  children: [new TextRun({ text: "Theme", bold: true, size: 20, color: "FFFFFF" })]
                })]
              }),
              new TableCell({
                borders: cellBorders,
                width: { size: 3510, type: WidthType.DXA },
                shading: { fill: "0F4C81", type: ShadingType.CLEAR },
                verticalAlign: VerticalAlign.CENTER,
                children: [new Paragraph({
                  alignment: AlignmentType.CENTER,
                  children: [new TextRun({ text: "Focus Areas", bold: true, size: 20, color: "FFFFFF" })]
                })]
              }),
              new TableCell({
                borders: cellBorders,
                width: { size: 3510, type: WidthType.DXA },
                shading: { fill: "0F4C81", type: ShadingType.CLEAR },
                verticalAlign: VerticalAlign.CENTER,
                children: [new Paragraph({
                  alignment: AlignmentType.CENTER,
                  children: [new TextRun({ text: "Core Logic", bold: true, size: 20, color: "FFFFFF" })]
                })]
              })
            ]
          }),
          new TableRow({
            children: [
              new TableCell({
                borders: cellBorders,
                width: { size: 2340, type: WidthType.DXA },
                children: [new Paragraph({
                  children: [new TextRun({ text: "Theme 1:\nGlobal Expansion", bold: true })]
                })]
              }),
              new TableCell({
                borders: cellBorders,
                width: { size: 3510, type: WidthType.DXA },
                children: [
                  new Paragraph({ numbering: { reference: "bullet-list", level: 0 }, children: [new TextRun("ADC, bispecific antibody leaders")] }),
                  new Paragraph({ numbering: { reference: "bullet-list", level: 0 }, children: [new TextRun("Small molecule targeted FIC/BIC")] }),
                  new Paragraph({ numbering: { reference: "bullet-list", level: 0 }, children: [new TextRun("Companies with overseas commercialization capability")] })
                ]
              }),
              new TableCell({
                borders: cellBorders,
                width: { size: 3510, type: WidthType.DXA },
                children: [
                  new Paragraph({ numbering: { reference: "bullet-list", level: 0 }, children: [new TextRun("BD deals continue to explode, value realization accelerating")] }),
                  new Paragraph({ numbering: { reference: "bullet-list", level: 0 }, children: [new TextRun("China R&D efficiency leads globally")] }),
                  new Paragraph({ numbering: { reference: "bullet-list", level: 0 }, children: [new TextRun("Multiple drugs to be approved overseas in 2026")] })
                ]
              })
            ]
          }),
          new TableRow({
            children: [
              new TableCell({
                borders: cellBorders,
                width: { size: 2340, type: WidthType.DXA },
                children: [new Paragraph({
                  children: [new TextRun({ text: "Theme 2:\nSupply Chain Upgrade", bold: true })]
                })]
              }),
              new TableCell({
                borders: cellBorders,
                width: { size: 3510, type: WidthType.DXA },
                children: [
                  new Paragraph({ numbering: { reference: "bullet-list", level: 0 }, children: [new TextRun("CRO/CDMO leaders")] }),
                  new Paragraph({ numbering: { reference: "bullet-list", level: 0 }, children: [new TextRun("Upstream equipment/materials")] }),
                  new Paragraph({ numbering: { reference: "bullet-list", level: 0 }, children: [new TextRun("ADC CDMO specialists")] })
                ]
              }),
              new TableCell({
                borders: cellBorders,
                width: { size: 3510, type: WidthType.DXA },
                children: [
                  new Paragraph({ numbering: { reference: "bullet-list", level: 0 }, children: [new TextRun("Global capacity transfer, orders continue to grow")] }),
                  new Paragraph({ numbering: { reference: "bullet-list", level: 0 }, children: [new TextRun("Huge domestic substitution opportunity")] }),
                  new Paragraph({ numbering: { reference: "bullet-list", level: 0 }, children: [new TextRun("ADC explosion drives CDMO demand")] })
                ]
              })
            ]
          }),
          new TableRow({
            children: [
              new TableCell({
                borders: cellBorders,
                width: { size: 2340, type: WidthType.DXA },
                children: [new Paragraph({
                  children: [new TextRun({ text: "Theme 3:\nFrontier Tech", bold: true })]
                })]
              }),
              new TableCell({
                borders: cellBorders,
                width: { size: 3510, type: WidthType.DXA },
                children: [
                  new Paragraph({ numbering: { reference: "bullet-list", level: 0 }, children: [new TextRun("Cell therapy (CAR-T)")] }),
                  new Paragraph({ numbering: { reference: "bullet-list", level: 0 }, children: [new TextRun("Gene therapy (AAV/CRISPR)")] }),
                  new Paragraph({ numbering: { reference: "bullet-list", level: 0 }, children: [new TextRun("Weight loss drugs (GLP-1)")] })
                ]
              }),
              new TableCell({
                borders: cellBorders,
                width: { size: 3510, type: WidthType.DXA },
                children: [
                  new Paragraph({ numbering: { reference: "bullet-list", level: 0 }, children: [new TextRun("9 CGT products approved, commercialization accelerating")] }),
                  new Paragraph({ numbering: { reference: "bullet-list", level: 0 }, children: [new TextRun("Gene editing breakthroughs, smooth clinical progress")] }),
                  new Paragraph({ numbering: { reference: "bullet-list", level: 0 }, children: [new TextRun("Huge weight loss market, domestic GLP-1 launching")] })
                ]
              })
            ]
          })
        ]
      }),

      new Paragraph({ children: [new TextRun("")] }),

      new Paragraph({
        heading: HeadingLevel.HEADING_2,
        children: [new TextRun("3.2 Key Company Types to Watch")]
      }),

      new Paragraph({
        children: [
          new TextRun("Based on the above analysis, we recommend focusing on the following company types:")
        ]
      }),

      new Paragraph({ children: [new TextRun("")] }),

      new Paragraph({
        numbering: { reference: "numbered-list", level: 0 },
        children: [new TextRun({ text: "Leading Companies with Overseas Commercialization Capability", bold: true })]
      }),
      new Paragraph({
        children: [
          new TextRun("  Selection criteria: Products already launched overseas, established overseas sales teams, rich BD experience\n"),
          new TextRun("  Representative companies: BeiGene, Junshi Biosciences, Innovent Biologics, Zai Lab")
        ]
      }),

      new Paragraph({ children: [new TextRun("")] }),

      new Paragraph({
        numbering: { reference: "numbered-list", level: 0 },
        children: [new TextRun({ text: "Technology Platform Companies", bold: true })]
      }),
      new Paragraph({
        children: [
          new TextRun("  Selection criteria: Core technology platforms (ADC, bispecific, cell therapy), rich pipelines, continuous output\n"),
          new TextRun("  Representative companies: SystImmune, Kelun-Biotech, Akeso, RemeGen, Legend Biotech")
        ]
      }),

      new Paragraph({ children: [new TextRun("")] }),

      new Paragraph({
        numbering: { reference: "numbered-list", level: 0 },
        children: [new TextRun({ text: "Biotech with Healthy Cash Flow", bold: true })]
      }),
      new Paragraph({
        children: [
          new TextRun("  Selection criteria: Sufficient cash reserves (>2 years runway), continuous BD income, strong financing capability\n"),
          new TextRun("  Representative companies: Analyze based on latest financial reports and financing situations")
        ]
      }),

      new Paragraph({ children: [new TextRun("")] }),

      new Paragraph({
        numbering: { reference: "numbered-list", level: 0 },
        children: [new TextRun({ text: "CRO/CDMO Leaders", bold: true })]
      }),
      new Paragraph({
        children: [
          new TextRun("  Selection criteria: Large production capacity,优质 customer base, strong technology capabilities, high overseas revenue proportion\n"),
          new TextRun("  Representative companies: WuXi AppTec, WuXi Biologics, Pharmaron, Asymchem, Porton Pharma")
        ]
      }),

      new Paragraph({ children: [new TextRun("")] }),

      new Paragraph({
        heading: HeadingLevel.HEADING_2,
        children: [new TextRun("3.3 Risk Factors")]
      }),

      new Paragraph({
        children: [
          new TextRun("Investors in innovative pharma should monitor the following risks:")
        ]
      }),
      new Paragraph({
        numbering: { reference: "bullet-list", level: 0 },
        children: [new TextRun("Geopolitical risk: US-China relations, tariff policies may affect overseas expansion")]
      }),
      new Paragraph({
        numbering: { reference: "bullet-list", level: 0 },
        children: [new TextRun("R&D failure risk: High clinical failure rate, key data may miss expectations")]
      }),
      new Paragraph({
        numbering: { reference: "bullet-list", level: 0 },
        children: [new TextRun("Competition risk: Homogeneous competition in hot targets, price wars compress margins")]
      }),
      new Paragraph({
        numbering: { reference: "bullet-list", level: 0 },
        children: [new TextRun("Payment pressure risk: Cost control remains long-term trend, price pressure continues")]
      }),
      new Paragraph({
        numbering: { reference: "bullet-list", level: 0 },
        children: [new TextRun("Valuation volatility risk: Biotech valuation fluctuations are large, monitor cash flow and financing capability")]
      }),

      new Paragraph({ children: [new PageBreak()] }),

      // Chapter 4
      new Paragraph({
        heading: HeadingLevel.HEADING_1,
        children: [new TextRun("Chapter 4: Conclusions and Outlook")]
      }),

      new Paragraph({
        children: [
          new TextRun("China's innovative pharma industry is at a historic inflection point, transitioning from "),
          new TextRun({ text: "follow-on innovation to global leadership", bold: true }),
          new TextRun(". In 2025, BD transactions ranked first globally, marking that China's innovative drugs have officially entered the "),
          new TextRun({ text: "Year of Value Realization", bold: true }),
          new TextRun(".")
        ]
      }),

      new Paragraph({ children: [new TextRun("")] }),

      new Paragraph({
        shading: { fill: "E8F4F8", type: ShadingType.CLEAR },
        indent: { left: 360, right: 360 },
        children: [
          new TextRun({ text: "Key Conclusions", bold: true, color: "0F4C81" }),
          new TextRun("\n\n"),
          new TextRun({ text: "1.  Overseas BD is the most certain opportunity", bold: true }),
          new TextRun(": 2026 BD deals expected to continue breaking records, focus on leaders with overseas commercialization capability\n\n"),
          new TextRun({ text: "2.  ADC and bispecific antibodies have achieved global leadership", bold: true }),
          new TextRun(": China has surpassed Europe/US in these fields, becoming innovation hubs\n\n"),
          new TextRun({ text: "3.  Policy dividends continue to be released", bold: true }),
          new TextRun(": Dual-directory system drives faster market access and better pricing for true innovation\n\n"),
          new TextRun({ text: "4.  Supply chain rise is a major trend", bold: true }),
          new TextRun(": CRO/CDMO transitioning from follower to leader, upstream domestic substitution accelerating\n\n"),
          new TextRun({ text: "5.  2026 is the Year of Value Realization", bold: true }),
          new TextRun(": Multiple blockbuster drugs to be approved overseas, BD income starting to contribute substantive profits")
        ]
      }),

      new Paragraph({ children: [new TextRun("")] }),

      new Paragraph({
        children: [
          new TextRun("Looking ahead 3-5 years, we expect:")
        ]
      }),
      new Paragraph({
        numbering: { reference: "bullet-list", level: 0 },
        children: [new TextRun("China's global market share in innovative drugs to increase from current 5% to >15%")]
      }),
      new Paragraph({
        numbering: { reference: "bullet-list", level: 0 },
        children: [new TextRun("China to become global innovation center in ADC, bispecific antibodies, attracting global pharma partnerships")]
      }),
      new Paragraph({
        numbering: { reference: "bullet-list", level: 0 },
        children: [new TextRun("CRO/CDMO global market share to further increase, 3-5 companies with >RMB 100B market cap to emerge")]
      }),
      new Paragraph({
        numbering: { reference: "bullet-list", level: 0 },
        children: [new TextRun("Frontier technologies like cell therapy and gene therapy to achieve commercialization breakthroughs")]
      }),
      new Paragraph({
        numbering: { reference: "bullet-list", level: 0 },
        children: [new TextRun("Chinese innovative pharma companies to transition from License-out to independent overseas commercialization, establishing global sales networks")]
      }),

      new Paragraph({ children: [new TextRun("")] }),

      new Paragraph({
        alignment: AlignmentType.CENTER,
        children: [
          new TextRun({ text: "— End of Report —", bold: true, size: 28, color: "0F4C81" })
        ]
      }),

      new Paragraph({ children: [new TextRun("")] }),
      new Paragraph({ children: [new TextRun("")] }),

      new Paragraph({
        alignment: AlignmentType.CENTER,
        shading: { fill: "F5F5F5", type: ShadingType.CLEAR },
        indent: { left: 720, right: 720 },
        children: [
          new TextRun({ text: "Disclaimer", bold: true, size: 20 }),
          new TextRun("\n\n"),
          new TextRun({ text: "This report is compiled based on publicly available information. Accuracy and completeness are not guaranteed.\n", size: 20 }),
          new TextRun({ text: "Report content is for reference only and does not constitute investment advice.\n", size: 20 }),
          new TextRun({ text: "Investors should make independent judgments and bear investment risks themselves.\n", size: 20 }),
          new TextRun({ text: "Report generated: February 20, 2026", size: 20, italics: true })
        ]
      })
    ]
  }]
});

Packer.toBuffer(doc).then((buffer) => {
  fs.writeFileSync('/Users/davidli/lobsterai/project/China_Innovative_Pharma_Industry_Report_2026_EN.docx', buffer);
  console.log('English report created successfully!');
}).catch((err) => {
  console.error('Error creating document:', err);
});
