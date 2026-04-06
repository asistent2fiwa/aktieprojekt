$content = Get-Content 'C:\Users\asist\.openclaw\workspace\projects\aktieprojekt\ai-trading-v3.html' -Raw
$match = [regex]::Match($content, '(?s)<script>(.+?)</script>')
if ($match.Success) {
    $match.Groups[1].Value | Set-Content 'C:\Users\asist\.openclaw\workspace\projects\aktieprojekt\temp_script.js' -NoNewline
}
Write-Output 'Done'
