param(
  [Parameter(Mandatory=$true)][string]$Source,
  [Parameter(Mandatory=$true)][string]$Dest,
  [string]$OutCsv = (Join-Path $Dest 'date_taken_index.csv')
)

$shell = New-Object -ComObject Shell.Application
$idx = 12 # 拍摄日期
$imgExt = '.jpg','.jpeg','.png','.heic','.gif','.bmp','.tif','.tiff','.webp'
$rows = @()
foreach ($p in @($Source,$Dest)) {
  $folder = $shell.NameSpace($p)
  Get-ChildItem -LiteralPath $p -File | Where-Object { $imgExt -contains $_.Extension.ToLower() } | ForEach-Object {
    $raw = $folder.GetDetailsOf($folder.ParseName($_.Name), $idx)
    $rows += [pscustomobject]@{ Folder = $p; Name = $_.Name; DateTakenRaw = $raw }
  }
}
$rows | Export-Csv -NoTypeInformation -Encoding UTF8 -Path $OutCsv
