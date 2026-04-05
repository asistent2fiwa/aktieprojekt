# Push ai-trading-v3.html to GitHub
$filePath = "C:\Users\asist\.openclaw\workspace\projects\aktieprojekt\ai-trading-v3.html"
$content = [System.Convert]::ToBase64String([System.IO.File]::ReadAllBytes($filePath))

# Get SHA if file exists
$sha = $null
try {
    $sha = (gh api repos/asistent2fiwa/aktie-projekt/contents/ai-trading-v3.html --jq '.sha' 2>$null)
} catch {}

$params = @(
    "repos/asistent2fiwa/aktie-projekt/contents/ai-trading-v3.html",
    "--method", "PUT",
    "--field", "message=Add ai-trading-v3.html with session protection",
    "--field", "content=$content"
)
if ($sha) {
    $params += "--field", "sha=$sha"
}

& gh api @params
