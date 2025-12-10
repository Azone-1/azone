# DNS Propagation Check Script
# Run: .\DNS_CHECK.ps1

Write-Host "=========================================" -ForegroundColor Green
Write-Host "🌐 DNS Propagation Check" -ForegroundColor Green
Write-Host "=========================================" -ForegroundColor Green
Write-Host ""

$domain = "paing.xyz"
$dnsServers = @(
    "1.1.1.1",      # Cloudflare
    "8.8.8.8",      # Google
    "208.67.222.222" # OpenDNS
)

Write-Host "Checking DNS for: $domain" -ForegroundColor Cyan
Write-Host ""

foreach ($dns in $dnsServers) {
    Write-Host "DNS Server: $dns" -ForegroundColor Yellow
    try {
        $result = nslookup $domain $dns 2>&1
        $ip = ($result | Select-String -Pattern "Address:" | Select-Object -Last 1).ToString()
        if ($ip) {
            Write-Host "  ✅ $ip" -ForegroundColor Green
        } else {
            Write-Host "  ❌ No IP found" -ForegroundColor Red
        }
    } catch {
        Write-Host "  ❌ Error: $_" -ForegroundColor Red
    }
    Write-Host ""
}

Write-Host "=========================================" -ForegroundColor Green
Write-Host "Expected IP: 18.138.169.114" -ForegroundColor Cyan
Write-Host "=========================================" -ForegroundColor Green

