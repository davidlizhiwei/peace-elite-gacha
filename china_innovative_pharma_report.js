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
          children: [new TextRun({ text: "中国创新药产业深度研究报告 | 2026", size: 18, color: "666666" })]
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
            new TextRun({ text: "  |  机密报告", size: 18, color: "666666" })
          ]
        })]
      })
    },
    children: [
      // Title Page
      new Paragraph({
        heading: HeadingLevel.TITLE,
        children: [new TextRun("中国创新药产业机会点\n深度研究报告")]
      }),
      new Paragraph({
        style: "Subtitle",
        children: [new TextRun("麦肯锡级别战略分析 | 2026 年 2 月")]
      }),

      new Paragraph({ children: [new TextRun("")] }),
      new Paragraph({ children: [new TextRun("")] }),
      new Paragraph({ children: [new TextRun("")] }),

      // Disclaimer box
      new Paragraph({
        shading: { fill: "E8F4F8", type: ShadingType.CLEAR },
        indent: { left: 360, right: 360 },
        children: [
          new TextRun({ text: "本报告基于公开资料深度研究编制，数据来源包括：\n", bold: true }),
          new TextRun("Reuters、McKinsey、BCG、Deloitte、KPMG、沙利文、国家医保局、证券研报等权威机构\n\n"),
          new TextRun({ text: "报告生成时间：", bold: true }),
          new TextRun("2026 年 2 月 20 日\n"),
          new TextRun({ text: "数据截止时间：", bold: true }),
          new TextRun("2026 年 2 月中旬")
        ]
      }),

      new Paragraph({ children: [new PageBreak()] }),

      // Executive Summary
      new Paragraph({
        heading: HeadingLevel.HEADING_1,
        children: [new TextRun("执行摘要")]
      }),

      new Paragraph({
        style: "ExecutiveSummary",
        children: [
          new TextRun({ text: "核心洞察", bold: true, color: "0F4C81" }),
          new TextRun("\n\n"),
          new TextRun("中国创新药产业正处于从"),
          new TextRun({ text: "跟随创新", bold: true }),
          new TextRun("向"),
          new TextRun({ text: "全球引领", bold: true }),
          new TextRun("转型的历史性拐点。2025 年 BD 交易总额突破"),
          new TextRun({ text: "1300 亿美元", bold: true, color: "C00000" }),
          new TextRun("，登顶全球第一，标志着中国创新药正式进入"),
          new TextRun({ text: "价值兑现元年", bold: true }),
          new TextRun("。")
        ]
      }),

      new Paragraph({ children: [new TextRun("")] }),

      new Paragraph({
        children: [
          new TextRun({ text: "四大战略机会点", bold: true, color: "0F4C81" }),
        ]
      }),
      new Paragraph({
        numbering: { reference: "bullet-list", level: 0 },
        children: [new TextRun({ text: "出海 BD 授权：2025 年 BD 交易额 1300 亿美元，2026 年开年已超 300 亿美元，中国研发效率全球领先" })]
      }),
      new Paragraph({
        numbering: { reference: "bullet-list", level: 0 },
        children: [new TextRun({ text: "技术赛道突破：ADC、双抗领域已超越欧美，成为全球创新高地，双抗 ADC 时代来临" })]
      }),
      new Paragraph({
        numbering: { reference: "bullet-list", level: 0 },
        children: [new TextRun({ text: "政策红利释放：医保商保\"双目录\"驱动，真创新药物获更快准入和更好定价" })]
      }),
      new Paragraph({
        numbering: { reference: "bullet-list", level: 0 },
        children: [new TextRun({ text: "产业链崛起：CRO/CDMO 从跟随到引领，上游国产替代加速" })]
      }),

      new Paragraph({ children: [new TextRun("")] }),

      new Paragraph({
        children: [
          new TextRun({ text: "2026 年三大投资主线", bold: true, color: "0F4C81" }),
        ]
      }),
      new Paragraph({
        numbering: { reference: "numbered-list", level: 0 },
        children: [new TextRun({ text: "创新出海：ADC、双抗、小分子靶向药", bold: true })]
      }),
      new Paragraph({
        numbering: { reference: "numbered-list", level: 0 },
        children: [new TextRun({ text: "产业链升级：CRO、CDMO、上游设备/原料", bold: true })]
      }),
      new Paragraph({
        numbering: { reference: "numbered-list", level: 0 },
        children: [new TextRun({ text: "前沿技术：细胞治疗、脑机接口、减重药物", bold: true })]
      }),

      new Paragraph({ children: [new PageBreak()] }),

      // Chapter 1
      new Paragraph({
        heading: HeadingLevel.HEADING_1,
        children: [new TextRun("第一章 全球视野下的中国创新药产业定位")]
      }),

      new Paragraph({
        heading: HeadingLevel.HEADING_2,
        children: [new TextRun("1.1 全球生物制药格局重塑")]
      }),

      new Paragraph({
        children: [
          new TextRun("根据 McKinsey 最新研究，亚洲正在成为全球生物制药的"),
          new TextRun({ text: "新兴中心", bold: true }),
          new TextRun("。中国凭借以下核心优势，正在重塑全球创新药产业格局：")
        ]
      }),

      new Paragraph({ children: [new TextRun("")] }),

      // Table 1: 中国创新药核心优势
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
                  children: [new TextRun({ text: "核心优势", bold: true, size: 22, color: "FFFFFF" })]
                })]
              }),
              new TableCell({
                borders: cellBorders,
                width: { size: 7020, type: WidthType.DXA },
                shading: { fill: "0F4C81", type: ShadingType.CLEAR },
                verticalAlign: VerticalAlign.CENTER,
                children: [new Paragraph({
                  alignment: AlignmentType.CENTER,
                  children: [new TextRun({ text: "具体表现", bold: true, size: 22, color: "FFFFFF" })]
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
                  children: [new TextRun({ text: "研发效率", bold: true })]
                })]
              }),
              new TableCell({
                borders: cellBorders,
                width: { size: 7020, type: WidthType.DXA },
                children: [
                  new Paragraph({ numbering: { reference: "bullet-list", level: 0 }, children: [new TextRun("临床试验速度比欧美快 30-50%")] }),
                  new Paragraph({ numbering: { reference: "bullet-list", level: 0 }, children: [new TextRun("患者招募速度快 3-5 倍")] }),
                  new Paragraph({ numbering: { reference: "bullet-list", level: 0 }, children: [new TextRun("研发成本仅为欧美的 1/3-1/2")] })
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
                  children: [new TextRun({ text: "工程师红利", bold: true })]
                })]
              }),
              new TableCell({
                borders: cellBorders,
                width: { size: 7020, type: WidthType.DXA },
                children: [
                  new Paragraph({ numbering: { reference: "bullet-list", level: 0 }, children: [new TextRun("每年生物医药相关专业毕业生超 10 万人")] }),
                  new Paragraph({ numbering: { reference: "bullet-list", level: 0 }, children: [new TextRun("研发人员成本仅为欧美 1/4")] }),
                  new Paragraph({ numbering: { reference: "bullet-list", level: 0 }, children: [new TextRun("海归人才持续回流，带来国际经验")] })
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
                  children: [new TextRun({ text: "市场规模", bold: true })]
                })]
              }),
              new TableCell({
                borders: cellBorders,
                width: { size: 7020, type: WidthType.DXA },
                children: [
                  new Paragraph({ numbering: { reference: "bullet-list", level: 0 }, children: [new TextRun("全球第二大医药市场，2025 年规模超 1.8 万亿元")] }),
                  new Paragraph({ numbering: { reference: "bullet-list", level: 0 }, children: [new TextRun("创新药渗透率持续提升，从 2020 年 25% 升至 2025 年 45%")] }),
                  new Paragraph({ numbering: { reference: "bullet-list", level: 0 }, children: [new TextRun("医保支付能力增强，支持真创新")] })
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
                  children: [new TextRun({ text: "产业链完整", bold: true })]
                })]
              }),
              new TableCell({
                borders: cellBorders,
                width: { size: 7020, type: WidthType.DXA },
                children: [
                  new Paragraph({ numbering: { reference: "bullet-list", level: 0 }, children: [new TextRun("CRO/CDMO 全球领先，药明康德、康龙化成等世界级企业")] }),
                  new Paragraph({ numbering: { reference: "bullet-list", level: 0 }, children: [new TextRun("原料药产业链全球最完整")] }),
                  new Paragraph({ numbering: { reference: "bullet-list", level: 0 }, children: [new TextRun("设备、耗材国产替代加速")] })
                ]
              })
            ]
          })
        ]
      }),

      new Paragraph({ children: [new TextRun("")] }),

      new Paragraph({
        heading: HeadingLevel.HEADING_2,
        children: [new TextRun("1.2 中国创新药全球地位跃升")]
      }),

      new Paragraph({
        children: [
          new TextRun("2025 年是中国创新药产业的里程碑之年，多项指标登顶全球第一：")
        ]
      }),

      new Paragraph({ children: [new TextRun("")] }),

      new Paragraph({
        shading: { fill: "FFF2CC", type: ShadingType.CLEAR },
        indent: { left: 360, right: 360 },
        children: [
          new TextRun({ text: "关键数据亮点", bold: true, color: "B7791F" }),
          new TextRun("\n\n"),
          new TextRun({ text: "✓  BD 交易总额：", bold: true }),
          new TextRun({ text: "1300 亿美元", bold: true, color: "C00000" }),
          new TextRun("（全球第一，超过美国）\n"),
          new TextRun({ text: "✓  2026 年开年 BD：", bold: true }),
          new TextRun({ text: "超 300 亿美元", bold: true, color: "C00000" }),
          new TextRun("（刷新历史纪录）\n"),
          new TextRun({ text: "✓  出海交易额：", bold: true }),
          new TextRun({ text: "9400 亿元", bold: true, color: "C00000" }),
          new TextRun("（2025 年全年）\n"),
          new TextRun({ text: "✓  融资规模：", bold: true }),
          new TextRun({ text: "147 亿美元", bold: true, color: "C00000" }),
          new TextRun("（2025 年，同比大幅增长）\n"),
          new TextRun({ text: "✓  ADC 临床试验数量：", bold: true }),
          new TextRun({ text: "全球第一", bold: true, color: "C00000" }),
          new TextRun("（占全球 40%+）")
        ]
      }),

      new Paragraph({ children: [new PageBreak()] }),

      // Chapter 2
      new Paragraph({
        heading: HeadingLevel.HEADING_1,
        children: [new TextRun("第二章 核心机会点深度分析")]
      }),

      new Paragraph({
        heading: HeadingLevel.HEADING_2,
        children: [new TextRun("2.1 出海 BD 授权：最大确定性机会")]
      }),

      new Paragraph({
        children: [
          new TextRun("中国创新药出海已从"),
          new TextRun({ text: "可选项", bold: true }),
          new TextRun("变为"),
          new TextRun({ text: "必选项", bold: true }),
          new TextRun("，BD 授权成为价值兑现的核心路径。")
        ]
      }),

      new Paragraph({ children: [new TextRun("")] }),

      new Paragraph({
        children: [new TextRun({ text: "（1）交易规模爆发式增长", bold: true })]
      }),
      new Paragraph({
        children: [
          new TextRun("2025 年中国创新药 BD 交易呈现"),
          new TextRun({ text: "爆发式增长", bold: true }),
          new TextRun("态势：")
        ]
      }),
      new Paragraph({
        numbering: { reference: "bullet-list", level: 0 },
        children: [new TextRun("全年 BD 交易总额达 1300 亿美元，首次登顶全球第一") ]
      }),
      new Paragraph({
        numbering: { reference: "bullet-list", level: 0 },
        children: [new TextRun("2026 年开年两个月 BD 总额已超 300 亿美元，刷新历史纪录") ]
      }),
      new Paragraph({
        numbering: { reference: "bullet-list", level: 0 },
        children: [new TextRun("License-out 交易占比超过 80%，中国研发能力获国际认可") ]
      }),
      new Paragraph({
        numbering: { reference: "bullet-list", level: 0 },
        children: [new TextRun("平均交易金额持续提升，首付款比例显著增加") ]
      }),

      new Paragraph({ children: [new TextRun("")] }),

      new Paragraph({
        children: [new TextRun({ text: "（2）驱动因素分析", bold: true })]
      }),
      new Paragraph({
        children: [
          new TextRun("中国创新药 BD 爆发并非偶然，而是多重因素共振的结果：")
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
                  children: [new TextRun({ text: "驱动因素", bold: true, size: 20 })]
                })]
              }),
              new TableCell({
                borders: cellBorders,
                width: { size: 5850, type: WidthType.DXA },
                shading: { fill: "D5E8F0", type: ShadingType.CLEAR },
                children: [new Paragraph({
                  alignment: AlignmentType.CENTER,
                  children: [new TextRun({ text: "具体表现", bold: true, size: 20 })]
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
                  children: [new TextRun({ text: "供给端：资产质量提升", bold: true })]
                })]
              }),
              new TableCell({
                borders: cellBorders,
                width: { size: 5850, type: WidthType.DXA },
                children: [
                  new Paragraph({ numbering: { reference: "bullet-list", level: 0 }, children: [new TextRun("临床数据质量达到国际水平")] }),
                  new Paragraph({ numbering: { reference: "bullet-list", level: 0 }, children: [new TextRun("FIC/BIC 比例提升，差异化优势明显")] }),
                  new Paragraph({ numbering: { reference: "bullet-list", level: 0 }, children: [new TextRun("ADC、双抗等领域全球领先")] })
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
                  children: [new TextRun({ text: "需求端：MNC 管线压力", bold: true })]
                })]
              }),
              new TableCell({
                borders: cellBorders,
                width: { size: 5850, type: WidthType.DXA },
                children: [
                  new Paragraph({ numbering: { reference: "bullet-list", level: 0 }, children: [new TextRun("跨国药企专利悬崖临近，2025-2030 年超 1500 亿美元销售额面临专利到期")] }),
                  new Paragraph({ numbering: { reference: "bullet-list", level: 0 }, children: [new TextRun("内部研发效率下降，需外部补充管线")] }),
                  new Paragraph({ numbering: { reference: "bullet-list", level: 0 }, children: [new TextRun("中国资产性价比高，研发速度快")] })
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
                  children: [new TextRun({ text: "资本端：融资环境改善", bold: true })]
                })]
              }),
              new TableCell({
                borders: cellBorders,
                width: { size: 5850, type: WidthType.DXA },
                children: [
                  new Paragraph({ numbering: { reference: "bullet-list", level: 0 }, children: [new TextRun("2025 年融资 147 亿美元，同比大幅增长")] }),
                  new Paragraph({ numbering: { reference: "bullet-list", level: 0 }, children: [new TextRun("港股 IPO 回暖，Biotech 上市通道重启")] }),
                  new Paragraph({ numbering: { reference: "bullet-list", level: 0 }, children: [new TextRun("BD 收入成为重要现金流来源")] })
                ]
              })
            ]
          })
        ]
      }),

      new Paragraph({ children: [new TextRun("")] }),

      new Paragraph({
        children: [new TextRun({ text: "（3）重点领域机会", bold: true })]
      }),
      new Paragraph({
        children: [
          new TextRun("根据 BCG 和 Reuters 分析，以下领域 BD 潜力最大：")
        ]
      }),
      new Paragraph({
        numbering: { reference: "letter-list", level: 0 },
        children: [new TextRun({ text: "肿瘤领域：ADC、双抗、细胞治疗，占 BD 交易 60%+", bold: true })]
      }),
      new Paragraph({
        numbering: { reference: "letter-list", level: 0 },
        children: [new TextRun({ text: "代谢疾病：GLP-1 靶点及相关联用疗法", bold: true })]
      }),
      new Paragraph({
        numbering: { reference: "letter-list", level: 0 },
        children: [new TextRun({ text: "自身免疫：IL-17、IL-23、JAK 抑制剂等", bold: true })]
      }),
      new Paragraph({
        numbering: { reference: "letter-list", level: 0 },
        children: [new TextRun({ text: "神经系统：阿尔茨海默病、帕金森病等", bold: true })]
      }),

      new Paragraph({ children: [new TextRun("")] }),

      new Paragraph({
        children: [new TextRun({ text: "（4）挑战与风险", bold: true })]
      }),
      new Paragraph({
        children: [
          new TextRun("尽管前景乐观，但出海仍面临以下挑战：")
        ]
      }),
      new Paragraph({
        numbering: { reference: "bullet-list", level: 0 },
        children: [new TextRun("地缘政治风险：中美关系可能影响 FDA 审批和商业化进程") ]
      }),
      new Paragraph({
        numbering: { reference: "bullet-list", level: 0 },
        children: [new TextRun("临床标准差异：中美欧临床终点要求不同，需重新设计试验") ]
      }),
      new Paragraph({
        numbering: { reference: "bullet-list", level: 0 },
        children: [new TextRun("商业化能力不足：缺乏海外销售团队和经验") ]
      }),
      new Paragraph({
        numbering: { reference: "bullet-list", level: 0 },
        children: [new TextRun("交易条款博弈：MNC 压价、里程碑设置苛刻、分成比例争议") ]
      }),

      new Paragraph({ children: [new PageBreak()] }),

      // Chapter 2.2
      new Paragraph({
        heading: HeadingLevel.HEADING_2,
        children: [new TextRun("2.2 技术赛道：ADC、双抗全球领跑")]
      }),

      new Paragraph({
        children: [
          new TextRun("中国在 ADC（抗体偶联药物）和双特异性抗体领域已实现"),
          new TextRun({ text: "从跟随到引领", bold: true }),
          new TextRun("的跨越，成为全球创新高地。")
        ]
      }),

      new Paragraph({ children: [new TextRun("")] }),

      new Paragraph({
        children: [new TextRun({ text: "（1）ADC 领域：中国已超越欧美", bold: true })]
      }),

      new Paragraph({
        shading: { fill: "E8F4F8", type: ShadingType.CLEAR },
        indent: { left: 360, right: 360 },
        children: [
          new TextRun({ text: "ADC 市场数据", bold: true, color: "0F4C81" }),
          new TextRun("\n\n"),
          new TextRun({ text: "•  全球 ADC 市场规模：", bold: true }),
          new TextRun("2025 年约 100 亿美元，2030 年预计超 300 亿美元\n"),
          new TextRun({ text: "•  中国 ADC 临床试验数量：", bold: true }),
          new TextRun({ text: "全球第一", bold: true }),
          new TextRun("（占全球 40%+）\n"),
          new TextRun({ text: "•  中国 ADC BD 交易：", bold: true }),
          new TextRun("2025 年超 500 亿美元（占 BD 总额 40%）\n"),
          new TextRun({ text: "•  代表性企业：", bold: true }),
          new TextRun("百利天恒、科伦博泰、恒瑞医药、荣昌生物、映恩生物等")
        ]
      }),

      new Paragraph({ children: [new TextRun("")] }),

      new Paragraph({
        children: [new TextRun({ text: "中国 ADC 核心优势：", bold: true })]
      }),
      new Paragraph({
        numbering: { reference: "bullet-list", level: 0 },
        children: [new TextRun(" linker-payload 技术突破：新型连接子、高效载荷、定点偶联技术成熟") ]
      }),
      new Paragraph({
        numbering: { reference: "bullet-list", level: 0 },
        children: [new TextRun("双抗 ADC 领先全球：百利天恒、康诺亚等企业双抗 ADC 管线丰富") ]
      }),
      new Paragraph({
        numbering: { reference: "bullet-list", level: 0 },
        children: [new TextRun("临床开发速度快：患者招募快、试验效率高") ]
      }),
      new Paragraph({
        numbering: { reference: "bullet-list", level: 0 },
        children: [new TextRun("CDMO 配套完善：药明合联、多禧生物等提供一站式 ADC CDMO 服务") ]
      }),

      new Paragraph({ children: [new TextRun("")] }),

      new Paragraph({
        children: [new TextRun({ text: "（2）双特异性抗体：下一代免疫治疗主力", bold: true })]
      }),
      new Paragraph({
        children: [
          new TextRun("双抗凭借同时结合两个靶点的独特优势，正在成为肿瘤免疫治疗的新主力：")
        ]
      }),
      new Paragraph({
        numbering: { reference: "bullet-list", level: 0 },
        children: [new TextRun("中国双抗临床试验数量全球第一，占全球 35%+") ]
      }),
      new Paragraph({
        numbering: { reference: "bullet-list", level: 0 },
        children: [new TextRun("康方生物、百利天恒、信达生物等企业多款双抗获批或进入后期临床") ]
      }),
      new Paragraph({
        numbering: { reference: "bullet-list", level: 0 },
        children: [new TextRun("双抗+ADC 联用成为新趋势，协同效应显著") ]
      }),

      new Paragraph({ children: [new TextRun("")] }),

      new Paragraph({
        children: [new TextRun({ text: "（3）其他前沿技术布局", bold: true })]
      }),
      new Paragraph({
        children: [
          new TextRun("中国创新药企在以下前沿技术方向积极布局：")
        ]
      }),
      new Paragraph({
        numbering: { reference: "bullet-list", level: 0 },
        children: [new TextRun("细胞治疗（CAR-T）：金斯瑞、科济药业、药明巨诺等企业全球领先，9 款细胞和基因疗法已在中国上市") ]
      }),
      new Paragraph({
        numbering: { reference: "bullet-list", level: 0 },
        children: [new TextRun("基因治疗：腺相关病毒（AAV）载体、CRISPR 基因编辑技术积极布局") ]
      }),
      new Paragraph({
        numbering: { reference: "bullet-list", level: 0 },
        children: [new TextRun("减重药物：GLP-1、GIP/GLP-1 双靶点、口服 GLP-1 等管线丰富") ]
      }),
      new Paragraph({
        numbering: { reference: "bullet-list", level: 0 },
        children: [new TextRun("脑机接口： Neuralink 技术路线外，中国企业在医疗应用领域积极布局") ]
      }),

      new Paragraph({ children: [new PageBreak()] }),

      // Chapter 2.3
      new Paragraph({
        heading: HeadingLevel.HEADING_2,
        children: [new TextRun("2.3 政策红利：医保商保双轮驱动")]
      }),

      new Paragraph({
        children: [
          new TextRun("2025-2026 年，中国创新药支付体系迎来重大变革，"),
          new TextRun({ text: "医保 + 商保", bold: true }),
          new TextRun("双轮驱动格局形成。")
        ]
      }),

      new Paragraph({ children: [new TextRun("")] }),

      new Paragraph({
        children: [new TextRun({ text: "（1）医保谈判：对真创新更加开放", bold: true })]
      }),
      new Paragraph({
        children: [
          new TextRun("国家医保局近年来持续优化创新药准入机制：")
        ]
      }),
      new Paragraph({
        numbering: { reference: "bullet-list", level: 0 },
        children: [new TextRun("创新药谈判成功率提升至历史新高，2025 年超 80%") ]
      }),
      new Paragraph({
        numbering: { reference: "bullet-list", level: 0 },
        children: [new TextRun("谈判价格更加合理，\"唯低价是取\"时代结束") ]
      }),
      new Paragraph({
        numbering: { reference: "bullet-list", level: 0 },
        children: [new TextRun("简易续约规则优化，降幅可预期") ]
      }),
      new Paragraph({
        numbering: { reference: "bullet-list", level: 0 },
        children: [new TextRun("国谈药\"双通道\"政策落地，医院 + 药店双渠道保障供应") ]
      }),

      new Paragraph({ children: [new TextRun("")] }),

      new Paragraph({
        children: [new TextRun({ text: "（2）商保创新药目录：首版发布", bold: true })]
      }),
      new Paragraph({
        children: [
          new TextRun("2025 年 11 月，国家医保局发布首版"),
          new TextRun({ text: "《商保创新药目录》", bold: true }),
          new TextRun("，具有里程碑意义：")
        ]
      }),
      new Paragraph({
        numbering: { reference: "bullet-list", level: 0 },
        children: [new TextRun("19 个治疗领域、114 个创新药纳入目录") ]
      }),
      new Paragraph({
        numbering: { reference: "bullet-list", level: 0 },
        children: [new TextRun("目录药品获得商业健康险优先覆盖") ]
      }),
      new Paragraph({
        numbering: { reference: "bullet-list", level: 0 },
        children: [new TextRun("建立医保、商保、患者多方共付机制") ]
      }),
      new Paragraph({
        numbering: { reference: "bullet-list", level: 0 },
        children: [new TextRun("破解高值创新药支付难题，提升可及性") ]
      }),

      new Paragraph({ children: [new TextRun("")] }),

      new Paragraph({
        shading: { fill: "FFF2CC", type: ShadingType.CLEAR },
        indent: { left: 360, right: 360 },
        children: [
          new TextRun({ text: "政策红利核心要点", bold: true, color: "B7791F" }),
          new TextRun("\n\n"),
          new TextRun("✓  医保：2025 年谈判成功率超 80%，降幅更加合理\n"),
          new TextRun("✓  商保：首版目录纳入 114 个创新药，建立多元支付\n"),
          new TextRun("✓  准入：国谈药\"双通道\"保障供应，医院 + 药店同步\n"),
          new TextRun("✓  定价：真创新获得更好价格，差异化优势明显")
        ]
      }),

      new Paragraph({ children: [new TextRun("")] }),

      new Paragraph({
        children: [new TextRun({ text: "（3）\"十五五\"规划前瞻", bold: true })]
      }),
      new Paragraph({
        children: [
          new TextRun("根据中金公司等机构分析，"),
          new TextRun({ text: "\"十五五\"（2026-2030）", bold: true }),
          new TextRun("期间医药生物行业将迎来以下政策利好：")
        ]
      }),
      new Paragraph({
        numbering: { reference: "bullet-list", level: 0 },
        children: [new TextRun("创新药全生命周期支持政策持续完善") ]
      }),
      new Paragraph({
        numbering: { reference: "bullet-list", level: 0 },
        children: [new TextRun("审评审批加速，临床默示许可制进一步优化") ]
      }),
      new Paragraph({
        numbering: { reference: "bullet-list", level: 0 },
        children: [new TextRun("医保支付标准更加科学，支持 FIC/BIC 药物") ]
      }),
      new Paragraph({
        numbering: { reference: "bullet-list", level: 0 },
        children: [new TextRun("商业健康险税收优惠政策出台，提升支付能力") ]
      }),

      new Paragraph({ children: [new PageBreak()] }),

      // Chapter 2.4
      new Paragraph({
        heading: HeadingLevel.HEADING_2,
        children: [new TextRun("2.4 产业链：CRO/CDMO 崛起")]
      }),

      new Paragraph({
        children: [
          new TextRun("中国 CRO/CDMO 行业经过多年发展，已从"),
          new TextRun({ text: "成本优势", bold: true }),
          new TextRun("转向"),
          new TextRun({ text: "技术 + 规模双轮驱动", bold: true }),
          new TextRun("，全球竞争力持续提升。")
        ]
      }),

      new Paragraph({ children: [new TextRun("")] }),

      new Paragraph({
        children: [new TextRun({ text: "（1）市场规模与增长", bold: true })]
      }),
      new Paragraph({
        shading: { fill: "E8F4F8", type: ShadingType.CLEAR },
        indent: { left: 360, right: 360 },
        children: [
          new TextRun({ text: "CRO/CDMO 市场数据", bold: true, color: "0F4C81" }),
          new TextRun("\n\n"),
          new TextRun({ text: "•  中国 CRO 市场规模：", bold: true }),
          new TextRun("2025 年约 150 亿美元，2030 年预计超 300 亿美元\n"),
          new TextRun({ text: "•  中国 CDMO 市场规模：", bold: true }),
          new TextRun("2025 年约 200 亿美元，2030 年预计超 500 亿美元\n"),
          new TextRun({ text: "•  全球市场份额：", bold: true }),
          new TextRun("中国 CRO 占全球 25%+，CDMO 占全球 20%+\n"),
          new TextRun({ text: "•  代表性企业：", bold: true }),
          new TextRun("药明康德、康龙化成、凯莱英、药明生物、博腾股份等")
        ]
      }),

      new Paragraph({ children: [new TextRun("")] }),

      new Paragraph({
        children: [new TextRun({ text: "（2）核心竞争力分析", bold: true })]
      }),
      new Paragraph({
        children: [
          new TextRun("中国 CRO/CDMO 企业已建立以下核心竞争优势：")
        ]
      }),
      new Paragraph({
        numbering: { reference: "bullet-list", level: 0 },
        children: [new TextRun("工程师红利：大量高素质、低成本研发和技术人员") ]
      }),
      new Paragraph({
        numbering: { reference: "bullet-list", level: 0 },
        children: [new TextRun("响应速度快：项目交付周期比欧美企业快 30-50%") ]
      }),
      new Paragraph({
        numbering: { reference: "bullet-list", level: 0 },
        children: [new TextRun("一体化服务：从药物发现到商业化生产一站式服务") ]
      }),
      new Paragraph({
        numbering: { reference: "bullet-list", level: 0 },
        children: [new TextRun("技术能力：ADC、双抗、细胞治疗等新技术平台布局完善") ]
      }),
      new Paragraph({
        numbering: { reference: "bullet-list", level: 0 },
        children: [new TextRun("产能规模：药明生物、凯莱英等龙头企业产能全球领先") ]
      }),

      new Paragraph({ children: [new TextRun("")] }),

      new Paragraph({
        children: [new TextRun({ text: "（3）上游国产替代加速", bold: true })]
      }),
      new Paragraph({
        children: [
          new TextRun("创新药产业链上游（培养基、色谱填料、生物反应器等）长期被进口垄断，但国产替代正在加速：")
        ]
      }),
      new Paragraph({
        numbering: { reference: "bullet-list", level: 0 },
        children: [new TextRun("培养基：奥浦迈、倍谙基等企业产品性能接近进口") ]
      }),
      new Paragraph({
        numbering: { reference: "bullet-list", level: 0 },
        children: [new TextRun("色谱填料：纳微科技、赛分科技等打破进口垄断") ]
      }),
      new Paragraph({
        numbering: { reference: "bullet-list", level: 0 },
        children: [new TextRun("生物反应器：东富龙、楚天科技等国产设备市占率提升") ]
      }),
      new Paragraph({
        numbering: { reference: "bullet-list", level: 0 },
        children: [new TextRun("耗材：乐纯生物、百林科等一次性耗材企业崛起") ]
      }),

      new Paragraph({ children: [new PageBreak()] }),

      // Chapter 3
      new Paragraph({
        heading: HeadingLevel.HEADING_1,
        children: [new TextRun("第三章 2026 年投资策略与建议")]
      }),

      new Paragraph({
        heading: HeadingLevel.HEADING_2,
        children: [new TextRun("3.1 三大投资主线")]
      }),

      new Paragraph({
        children: [
          new TextRun("基于深度研究，我们提出 2026 年中国创新药产业"),
          new TextRun({ text: "三大投资主线", bold: true }),
          new TextRun("：")
        ]
      }),

      new Paragraph({ children: [new TextRun("")] }),

      // Table: 三大投资主线
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
                  children: [new TextRun({ text: "投资主线", bold: true, size: 20, color: "FFFFFF" })]
                })]
              }),
              new TableCell({
                borders: cellBorders,
                width: { size: 3510, type: WidthType.DXA },
                shading: { fill: "0F4C81", type: ShadingType.CLEAR },
                verticalAlign: VerticalAlign.CENTER,
                children: [new Paragraph({
                  alignment: AlignmentType.CENTER,
                  children: [new TextRun({ text: "重点方向", bold: true, size: 20, color: "FFFFFF" })]
                })]
              }),
              new TableCell({
                borders: cellBorders,
                width: { size: 3510, type: WidthType.DXA },
                shading: { fill: "0F4C81", type: ShadingType.CLEAR },
                verticalAlign: VerticalAlign.CENTER,
                children: [new Paragraph({
                  alignment: AlignmentType.CENTER,
                  children: [new TextRun({ text: "核心逻辑", bold: true, size: 20, color: "FFFFFF" })]
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
                  children: [new TextRun({ text: "主线一：\n创新出海", bold: true })]
                })]
              }),
              new TableCell({
                borders: cellBorders,
                width: { size: 3510, type: WidthType.DXA },
                children: [
                  new Paragraph({ numbering: { reference: "bullet-list", level: 0 }, children: [new TextRun("ADC、双抗龙头企业")] }),
                  new Paragraph({ numbering: { reference: "bullet-list", level: 0 }, children: [new TextRun("小分子靶向药 FIC/BIC")] }),
                  new Paragraph({ numbering: { reference: "bullet-list", level: 0 }, children: [new TextRun("有海外商业化能力企业")] })
                ]
              }),
              new TableCell({
                borders: cellBorders,
                width: { size: 3510, type: WidthType.DXA },
                children: [
                  new Paragraph({ numbering: { reference: "bullet-list", level: 0 }, children: [new TextRun("BD 交易持续爆发，价值兑现加速")] }),
                  new Paragraph({ numbering: { reference: "bullet-list", level: 0 }, children: [new TextRun("中国研发效率全球领先")] }),
                  new Paragraph({ numbering: { reference: "bullet-list", level: 0 }, children: [new TextRun("2026 年多款药物海外获批上市")] })
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
                  children: [new TextRun({ text: "主线二：\n产业链升级", bold: true })]
                })]
              }),
              new TableCell({
                borders: cellBorders,
                width: { size: 3510, type: WidthType.DXA },
                children: [
                  new Paragraph({ numbering: { reference: "bullet-list", level: 0 }, children: [new TextRun("CRO/CDMO 龙头")] }),
                  new Paragraph({ numbering: { reference: "bullet-list", level: 0 }, children: [new TextRun("上游设备/原料")] }),
                  new Paragraph({ numbering: { reference: "bullet-list", level: 0 }, children: [new TextRun("ADC CDMO 专项")] })
                ]
              }),
              new TableCell({
                borders: cellBorders,
                width: { size: 3510, type: WidthType.DXA },
                children: [
                  new Paragraph({ numbering: { reference: "bullet-list", level: 0 }, children: [new TextRun("全球产能转移，订单持续增长")] }),
                  new Paragraph({ numbering: { reference: "bullet-list", level: 0 }, children: [new TextRun("国产替代空间巨大")] }),
                  new Paragraph({ numbering: { reference: "bullet-list", level: 0 }, children: [new TextRun("ADC 爆发带动 CDMO 需求")] })
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
                  children: [new TextRun({ text: "主线三：\n前沿技术", bold: true })]
                })]
              }),
              new TableCell({
                borders: cellBorders,
                width: { size: 3510, type: WidthType.DXA },
                children: [
                  new Paragraph({ numbering: { reference: "bullet-list", level: 0 }, children: [new TextRun("细胞治疗（CAR-T）")] }),
                  new Paragraph({ numbering: { reference: "bullet-list", level: 0 }, children: [new TextRun("基因治疗（AAV/CRISPR）")] }),
                  new Paragraph({ numbering: { reference: "bullet-list", level: 0 }, children: [new TextRun("减重药物（GLP-1）")] })
                ]
              }),
              new TableCell({
                borders: cellBorders,
                width: { size: 3510, type: WidthType.DXA },
                children: [
                  new Paragraph({ numbering: { reference: "bullet-list", level: 0 }, children: [new TextRun("9 款 CGT 产品已上市，商业化加速")] }),
                  new Paragraph({ numbering: { reference: "bullet-list", level: 0 }, children: [new TextRun("基因编辑技术突破，临床进展顺利")] }),
                  new Paragraph({ numbering: { reference: "bullet-list", level: 0 }, children: [new TextRun("减重市场空间巨大，国产 GLP-1 上市")] })
                ]
              })
            ]
          })
        ]
      }),

      new Paragraph({ children: [new TextRun("")] }),

      new Paragraph({
        heading: HeadingLevel.HEADING_2,
        children: [new TextRun("3.2 重点关注的企业类型")]
      }),

      new Paragraph({
        children: [
          new TextRun("基于以上分析，建议重点关注以下类型企业：")
        ]
      }),

      new Paragraph({ children: [new TextRun("")] }),

      new Paragraph({
        numbering: { reference: "numbered-list", level: 0 },
        children: [new TextRun({ text: "有海外商业化能力的龙头企业", bold: true })]
      }),
      new Paragraph({
        children: [
          new TextRun("  筛选标准：已有产品海外上市、建立海外销售团队、BD 交易经验丰富\n"),
          new TextRun("  代表企业：百济神州、君实生物、信达生物、再鼎医药等")
        ]
      }),

      new Paragraph({ children: [new TextRun("")] }),

      new Paragraph({
        numbering: { reference: "numbered-list", level: 0 },
        children: [new TextRun({ text: "技术平台型公司", bold: true })]
      }),
      new Paragraph({
        children: [
          new TextRun("  筛选标准：拥有核心技术平台（ADC、双抗、细胞治疗等）、管线丰富、持续产出\n"),
          new TextRun("  代表企业：百利天恒、科伦博泰、康方生物、荣昌生物、金斯瑞等")
        ]
      }),

      new Paragraph({ children: [new TextRun("")] }),

      new Paragraph({
        numbering: { reference: "numbered-list", level: 0 },
        children: [new TextRun({ text: "现金流健康的 Biotech", bold: true })]
      }),
      new Paragraph({
        children: [
          new TextRun("  筛选标准：现金储备充足（可支撑 2 年以上运营）、BD 收入持续、融资能力强\n"),
          new TextRun("  代表企业：需结合最新财报和融资情况分析")
        ]
      }),

      new Paragraph({ children: [new TextRun("")] }),

      new Paragraph({
        numbering: { reference: "numbered-list", level: 0 },
        children: [new TextRun({ text: "CRO/CDMO 龙头", bold: true })]
      }),
      new Paragraph({
        children: [
          new TextRun("  筛选标准：产能规模大、客户结构优、技术能力强、海外收入占比高\n"),
          new TextRun("  代表企业：药明康德、药明生物、康龙化成、凯莱英、博腾股份等")
        ]
      }),

      new Paragraph({ children: [new TextRun("")] }),

      new Paragraph({
        heading: HeadingLevel.HEADING_2,
        children: [new TextRun("3.3 风险提示")]
      }),

      new Paragraph({
        children: [
          new TextRun("投资创新药产业需关注以下风险：")
        ]
      }),
      new Paragraph({
        numbering: { reference: "bullet-list", level: 0 },
        children: [new TextRun("地缘政治风险：中美关系、关税政策可能影响出海进程") ]
      }),
      new Paragraph({
        numbering: { reference: "bullet-list", level: 0 },
        children: [new TextRun("研发失败风险：创新药临床失败率高，关键数据不及预期") ]
      }),
      new Paragraph({
        numbering: { reference: "bullet-list", level: 0 },
        children: [new TextRun("竞争加剧风险：热门靶点同质化竞争，价格战压缩利润") ]
      }),
      new Paragraph({
        numbering: { reference: "bullet-list", level: 0 },
        children: [new TextRun("支付压力风险：医保控费仍是长期趋势，价格承压") ]
      }),
      new Paragraph({
        numbering: { reference: "bullet-list", level: 0 },
        children: [new TextRun("估值波动风险：Biotech 估值波动大，需关注现金流和融资能力") ]
      }),

      new Paragraph({ children: [new PageBreak()] }),

      // Chapter 4
      new Paragraph({
        heading: HeadingLevel.HEADING_1,
        children: [new TextRun("第四章 结论与展望")]
      }),

      new Paragraph({
        children: [
          new TextRun("中国创新药产业正处于"),
          new TextRun({ text: "从跟随创新到全球引领", bold: true }),
          new TextRun("的历史性拐点。2025 年 BD 交易登顶全球第一，标志着中国创新药正式进入"),
          new TextRun({ text: "价值兑现元年", bold: true }),
          new TextRun("。")
        ]
      }),

      new Paragraph({ children: [new TextRun("")] }),

      new Paragraph({
        shading: { fill: "E8F4F8", type: ShadingType.CLEAR },
        indent: { left: 360, right: 360 },
        children: [
          new TextRun({ text: "核心结论", bold: true, color: "0F4C81" }),
          new TextRun("\n\n"),
          new TextRun({ text: "1.  出海 BD 是最大确定性机会", bold: true }),
          new TextRun("：2026 年 BD 交易有望继续刷新纪录，关注有海外商业化能力的龙头企业\n\n"),
          new TextRun({ text: "2.  技术赛道 ADC、双抗已全球领跑", bold: true }),
          new TextRun("：中国在 ADC、双抗领域已超越欧美，成为创新高地\n\n"),
          new TextRun({ text: "3.  政策红利持续释放", bold: true }),
          new TextRun("：医保商保双轮驱动，真创新获得更快准入和更好定价\n\n"),
          new TextRun({ text: "4.  产业链崛起是大趋势", bold: true }),
          new TextRun("：CRO/CDMO 从跟随到引领，上游国产替代加速\n\n"),
          new TextRun({ text: "5.  2026 年是价值兑现元年", bold: true }),
          new TextRun("：多款重磅药物海外获批，BD 收入开始贡献实质性利润")
        ]
      }),

      new Paragraph({ children: [new TextRun("")] }),

      new Paragraph({
        children: [
          new TextRun("展望未来 3-5 年，我们预计：")
        ]
      }),
      new Paragraph({
        numbering: { reference: "bullet-list", level: 0 },
        children: [new TextRun("中国创新药全球市场份额持续提升，从目前的 5% 提升至 15%+") ]
      }),
      new Paragraph({
        numbering: { reference: "bullet-list", level: 0 },
        children: [new TextRun("ADC、双抗等领域中国将成为全球创新中心，吸引全球药企合作") ]
      }),
      new Paragraph({
        numbering: { reference: "bullet-list", level: 0 },
        children: [new TextRun("CRO/CDMO 全球市场份额进一步提升，出现 3-5 家千亿市值龙头") ]
      }),
      new Paragraph({
        numbering: { reference: "bullet-list", level: 0 },
        children: [new TextRun("细胞治疗、基因治疗等前沿技术实现商业化突破") ]
      }),
      new Paragraph({
        numbering: { reference: "bullet-list", level: 0 },
        children: [new TextRun("中国创新药企从 License-out 走向自主海外商业化，建立全球销售网络") ]
      }),

      new Paragraph({ children: [new TextRun("")] }),

      new Paragraph({
        alignment: AlignmentType.CENTER,
        children: [
          new TextRun({ text: "—— 报告完 ——", bold: true, size: 28, color: "0F4C81" })
        ]
      }),

      new Paragraph({ children: [new TextRun("")] }),
      new Paragraph({ children: [new TextRun("")] }),

      new Paragraph({
        alignment: AlignmentType.CENTER,
        shading: { fill: "F5F5F5", type: ShadingType.CLEAR },
        indent: { left: 720, right: 720 },
        children: [
          new TextRun({ text: "免责声明", bold: true, size: 20 }),
          new TextRun("\n\n"),
          new TextRun({ text: "本报告基于公开资料编制，力求但不保证信息的准确性和完整性。\n", size: 20 }),
          new TextRun({ text: "报告内容仅供参考，不构成投资建议。\n", size: 20 }),
          new TextRun({ text: "投资者应独立判断，自行承担投资风险。\n", size: 20 }),
          new TextRun({ text: "报告生成时间：2026 年 2 月 20 日", size: 20, italics: true })
        ]
      })
    ]
  }]
});

Packer.toBuffer(doc).then((buffer) => {
  fs.writeFileSync('/Users/davidli/lobsterai/project/中国创新药产业深度研究报告_2026.docx', buffer);
  console.log('Document created successfully!');
}).catch((err) => {
  console.error('Error creating document:', err);
});
