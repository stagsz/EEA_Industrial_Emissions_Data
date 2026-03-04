$OutputDir = "C:\Users\staff\anthropicFun\EEA_Industrial_Emissions_Data\data\market\EU_ETS_Data"
$Url = "https://www.eea.europa.eu/data-and-maps/data/european-union-emissions-trading-scheme-1/eu-ets-data-download-latest-version/ETS_Database_v51.zip"

Write-Host "Downloading EU ETS data..."
Write-Host "Output: $OutputDir"

try {
    Invoke-WebRequest -Uri $Url -OutFile "$OutputDir\ETS_Database.zip" -TimeoutSec 300
    Write-Host "Download successful!" -ForegroundColor Green
    Write-Host "File saved to: $OutputDir\ETS_Database.zip"
}
catch {
    Write-Host "Error: $_" -ForegroundColor Red
}
