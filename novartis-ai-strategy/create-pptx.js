const pptxgen = require('pptxgenjs');
const html2pptx = require('/Users/davidli/Library/Application Support/LobsterAI/SKILLs/pptx/scripts/html2pptx.js');
const path = require('path');

async function createPresentation() {
    const pptx = new pptxgen();
    pptx.layout = 'LAYOUT_16x9';
    pptx.author = '李智伟 - 诺华制药';
    pptx.title = '诺华制药数字化与 AI 治理实践';

    const slideDir = '/Users/davidli/lobsterai/project/novartis-ai-strategy/';

    // Slide 1: Title
    console.log('Creating slide 1: Title...');
    await html2pptx(path.join(slideDir, 'presentation.html'), pptx);

    // Slide 2: Table of Contents
    console.log('Creating slide 2: TOC...');
    await html2pptx(path.join(slideDir, 'slide2.html'), pptx);

    // Slide 3: Novartis Overview
    console.log('Creating slide 3: Overview...');
    await html2pptx(path.join(slideDir, 'slide3.html'), pptx);

    // Slide 4: AI Three Layers
    console.log('Creating slide 4: AI Layers...');
    await html2pptx(path.join(slideDir, 'slide4.html'), pptx);

    // Slide 5: AI Governance
    console.log('Creating slide 5: Governance...');
    await html2pptx(path.join(slideDir, 'slide5.html'), pptx);

    // Slide 6: Three Elements
    console.log('Creating slide 6: Three Elements...');
    await html2pptx(path.join(slideDir, 'slide6.html'), pptx);

    // Slide 7: IT Position & Project Selection
    console.log('Creating slide 7: IT Position...');
    await html2pptx(path.join(slideDir, 'slide7.html'), pptx);

    // Slide 8: Security & Compliance
    console.log('Creating slide 8: Security...');
    await html2pptx(path.join(slideDir, 'slide8.html'), pptx);

    // Slide 9: Model Strategy
    console.log('Creating slide 9: Model Strategy...');
    await html2pptx(path.join(slideDir, 'slide9.html'), pptx);

    // Slide 10: Cloud First
    console.log('Creating slide 10: Cloud First...');
    await html2pptx(path.join(slideDir, 'slide10.html'), pptx);

    // Slide 11: Digital Innovation
    console.log('Creating slide 11: Innovation...');
    await html2pptx(path.join(slideDir, 'slide11.html'), pptx);

    // Slide 12: Summary
    console.log('Creating slide 12: Summary...');
    await html2pptx(path.join(slideDir, 'slide12.html'), pptx);

    // Save presentation
    console.log('Saving presentation...');
    await pptx.writeFile({ fileName: '诺华制药 AI 治理实践.pptx' });
    console.log('Presentation created successfully!');
}

createPresentation().catch(console.error);
