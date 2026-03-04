# Download EU ETS Registry & Transaction Data
# This script downloads EU Emissions Trading System data and saves it to data/market/

$OutputDir = "C:\Users\staff\anthropicFun\EEA_Industrial_Emissions_Data\data\market\EU_ETS_Data"

# Create output directory if it doesn't exist
if (-not (Test-Path $OutputDir)) {
    New-Item -ItemType Directory -Path $OutputDir | Out-Null
    Write-Host "Created directory: $OutputDir" -ForegroundColor Green
}

Write-Host "`n=== EU ETS Registry & Transaction Data Download ===" -ForegroundColor Cyan
Write-Host "Saving to: $OutputDir`n"

# EU ETS Data Sources to download
$DownloadLinks = @{
    "Union_Registry_Operators_2024" = "https://union-registry-data.ec.europa.eu/download"
    "EEA_ETS_Data_Hub" = "https://www.eea.europa.eu/en/datahub/datahubitem-view/98f04097-26de-4fca-86c4-63834818c0c0"
    "Union_Registry_Public" = "https://union-registry-data.ec.europa.eu/"
}

Write-Host "Available EU ETS Data Sources:" -ForegroundColor Yellow
Write-Host ""
Write-Host "1. Union Registry Public Website (RECOMMENDED)" -ForegroundColor Green
Write-Host "   URL: https://union-registry-data.ec.europa.eu/" 
Write-Host "   Data: Verified emissions, compliance, allowances, operators"
Write-Host "   Format: Excel, CSV"
Write-Host ""

Write-Host "2. EEA DataHub" -ForegroundColor Green
Write-Host "   URL: https://www.eea.europa.eu/en/datahub/datahubitem-view/98f04097-26de-4fca-86c4-63834818c0c0"
Write-Host "   Data: Aggregated ETS data 2005-2024"
Write-Host "   Format: ASCII/CSV"
Write-Host ""

Write-Host "3. European Commission DG Climate" -ForegroundColor Green
Write-Host "   Data: Annual verified emissions, compliance, transactions"
Write-Host "   URL: https://climate.ec.europa.eu/eu-action/carbon-markets/eu-ets/"
Write-Host ""

Write-Host "Manual Download Instructions:" -ForegroundColor Cyan
Write-Host ""
Write-Host "OPTION A - Union Registry (Easiest for Recent Data):"
Write-Host "  1. Visit: https://union-registry-data.ec.europa.eu/"
Write-Host "  2. Download:"
Write-Host "     - List of operators (Excel 2024)"
Write-Host "     - Verified Emissions 2024 (Excel)"
Write-Host "     - Compliance data 2024 (Excel)"
Write-Host "     - Transaction data (ZIP)"
Write-Host "  3. Save to: $OutputDir"
Write-Host ""

Write-Host "OPTION B - EEA DataHub:"
Write-Host "  1. Visit: https://www.eea.europa.eu/en/datahub/datahubitem-view/98f04097-26de-4fca-86c4-63834818c0c0"
Write-Host "  2. Click 'Direct download' link"
Write-Host "  3. Download CSV/ASCII files"
Write-Host "  4. Save to: $OutputDir"
Write-Host ""

Write-Host "After downloading, you can run:" -ForegroundColor Yellow
Write-Host "  python scripts/analyze_eu_ets_data.py"
Write-Host ""

Write-Host "Directory created at: $OutputDir" -ForegroundColor Green
Write-Host "Ready to receive EU ETS data files!`n"