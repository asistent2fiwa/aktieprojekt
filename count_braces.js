const fs = require('fs');
const content = fs.readFileSync('C:\\Users\\asist\\.openclaw\\workspace\\projects\\aktieprojekt\\temp_script.js', 'utf8');
const lines = content.split('\n');

let braceCount = 0;
let parenCount = 0;
let bracketCount = 0;
let lastUnbalancedLine = 0;
let lastUnbalancedCol = 0;
let lastUnbalancedType = '';
let braceHistory = [];

for (let i = 0; i < lines.length; i++) {
    const line = lines[i];
    for (let j = 0; j < line.length; j++) {
        const ch = line[j];
        if (ch === '{') {
            braceCount++;
            braceHistory.push({ line: i + 1, col: j + 1, type: 'open', char: '{' });
        } else if (ch === '}') {
            braceCount--;
            braceHistory.push({ line: i + 1, col: j + 1, type: 'close', char: '}' });
            if (braceCount < 0) {
                console.log(`NEGATIVE BRACE at line ${i + 1}, col ${j + 1}`);
                braceCount = 0;
            }
        } else if (ch === '(') {
            parenCount++;
        } else if (ch === ')') {
            parenCount--;
            if (parenCount < 0) {
                console.log(`NEGATIVE PAREN at line ${i + 1}, col ${j + 1}`);
                parenCount = 0;
            }
        }
    }
}

console.log(`Final brace count: ${braceCount}`);
console.log(`Final paren count: ${parenCount}`);
console.log(`Final bracket count: ${bracketCount}`);

// Find the first unclosed brace
let openBraces = 0;
for (let i = 0; i < braceHistory.length; i++) {
    const h = braceHistory[i];
    if (h.type === 'open') {
        openBraces++;
    } else {
        openBraces--;
    }
    if (openBraces < 0) {
        console.log(`Unmatched closing brace at line ${h.line}, col ${h.col}`);
        break;
    }
}

// Find where we have open braces left
let running = 0;
let firstExcessOpen = -1;
for (let i = 0; i < braceHistory.length; i++) {
    const h = braceHistory[i];
    if (h.type === 'open') {
        running++;
    } else {
        running--;
    }
    if (running > 0 && firstExcessOpen === -1) {
        // Check if from this point forward, we never close enough
        firstExcessOpen = i;
    }
}

// Print last 20 brace events
console.log('\nLast 40 brace events:');
for (let i = Math.max(0, braceHistory.length - 40); i < braceHistory.length; i++) {
    const h = braceHistory[i];
    console.log(`  line ${h.line}: ${h.type} ${h.char}`);
}
