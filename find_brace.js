const fs = require('fs');
const content = fs.readFileSync('C:\\Users\\asist\\.openclaw\\workspace\\projects\\aktieprojekt\\temp_script.js', 'utf8');
const lines = content.split('\n');

let braceCount = 0;
let maxBraceCount = 0;
let maxBraceLine = 0;
let lineBraceCounts = [];

for (let i = 0; i < lines.length; i++) {
    const line = lines[i];
    let lineDelta = 0;
    for (let j = 0; j < line.length; j++) {
        const ch = line[j];
        if (ch === '{') {
            braceCount++;
            lineDelta++;
        } else if (ch === '}') {
            braceCount--;
            lineDelta--;
        }
    }
    lineBraceCounts.push({ line: i + 1, count: braceCount, delta: lineDelta });
    if (braceCount > maxBraceCount) {
        maxBraceCount = braceCount;
        maxBraceLine = i + 1;
    }
}

// Find where the count becomes positive and never returns to 0
// Look for the first line where braceCount > 0 and stays > 0 to end
let unclosedStart = -1;
let prevCount = 0;
for (let i = 0; i < lineBraceCounts.length; i++) {
    const lc = lineBraceCounts[i];
    if (lc.count > 0 && prevCount === 0) {
        unclosedStart = lc.line;
    }
    if (lc.count === 0 && prevCount > 0) {
        // It closed! So the issue might be somewhere else
        unclosedStart = -1;
    }
    prevCount = lc.count;
}

console.log(`Final brace count: ${braceCount}`);
console.log(`Max brace count: ${maxBraceCount} at line ${maxBraceLine}`);
console.log(`Unclosed start: ${unclosedStart}`);

// Find where braces are > 0 persistently from some point to end
// The final "excess" braces must be in the last open block
// Show lines around where count stays elevated
let elevatedLines = lineBraceCounts.filter(lc => lc.count > 0);
if (elevatedLines.length > 0) {
    console.log(`\nFirst line with excess braces: ${elevatedLines[0].line}`);
    console.log(`Last line with excess braces: ${elevatedLines[elevatedLines.length - 1].line}`);
}

// Find the first persistent open
let startExcess = -1;
for (let i = 0; i < lineBraceCounts.length; i++) {
    if (lineBraceCounts[i].count > 0) {
        startExcess = lineBraceCounts[i].line;
        break;
    }
}
console.log(`\nFirst line with open brace: ${startExcess}`);

// Show context around the end
console.log('\nLines 1980-2003:');
for (let i = 1979; i < lineBraceCounts.length; i++) {
    const lc = lineBraceCounts[i];
    const src = lines[i];
    console.log(`  ${lc.line}: count=${lc.count} delta=${lc.delta} | ${src.trim().substring(0, 80)}`);
}
