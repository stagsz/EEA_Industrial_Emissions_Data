# Download EU ETS Database from EEA
# Downloads the latest EU ETS data from the European Environment Agency

$OutputDir = "C:\Users\staff\anthropicFun\EEA_Industrial_Emissions_Data\data\market\EU_ETS_Data"
$DownloadURL = "https://www.eea.europa.eu/data-and-maps/data/european-union-emissions-trading-scheme-17/eu-ets-data-download-latest-version/ETS_Database_v51.zip"
$ZipFile = "$OutputDir\ETS_Database_v51.zip"

Write-Host "`n=== EU ETS Data Download from EEA ===" -ForegroundColor Cyan
Write-Host "Output Directory: $OutputDir`n"

# Check if directory exists
if (-not (Test-Path $OutputDir)) {
    New-Item -ItemType Directory -Path $OutputDir | Out-Null
    Write-Host "Created directory: $OutputDir" -ForegroundColor Green
}

# Download the file
Write-Host "Downloading EU ETS Database (v51)..." -ForegroundColor Yellow
Write-Host "Source: Union Registry Data from EEA" -ForegroundColor Gray

try {
    $ProgressPreference = 'SilentlyContinue'
    Invoke-WebRequest -Uri $DownloadURL -OutFile $ZipFile -TimeoutSec 300
    
    if (Test-Path $ZipFile) {
        $FileSize = (Get-Item $ZipFile).Length / 1MB
        Write-Host "Downloaded successfully: ETS_Database_v51.zip ($('{0:F2}' -f $FileSize) MB)" -ForegroundColor Green
        
        # Extract the zip file
        Write-Host "`nExtracting data files..." -ForegroundColor Yellow
        Expand-Archive -Path $ZipFile -DestinationPath $OutputDir -Force
        Write-Host "Extraction complete!" -ForegroundColor Green
        
        # List extracted files
        Write-Host "`nExtracted files:" -ForegroundColor Cyan
        Get-ChildItem -Path $OutputDir -File -Recurse | Select-Object -ExpandProperty FullName | ForEach-Object {
            $RelativePath = $_.Replace("$OutputDir\", "")
            Write-Host "  $RelativePath" -ForegroundColor Gray
        }
        
        Write-Host "`nEU ETS data is ready for analysis!" -ForegroundColor Green
        Write-Host "Location: $OutputDir`n"
    } else {
        Write-Host "Download failed!" -ForegroundColor Red
    }
} catch {
    Write-Host "Error downloading file: $_" -ForegroundColor Red
}
