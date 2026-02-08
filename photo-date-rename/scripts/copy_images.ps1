param(
  [Parameter(Mandatory=$true)][string]$Source,
  [Parameter(Mandatory=$true)][string]$Dest
)

$imgExt = '.jpg','.jpeg','.png','.heic','.gif','.bmp','.tif','.tiff','.webp'
New-Item -ItemType Directory -Path $Dest -Force | Out-Null
Get-ChildItem -LiteralPath $Source -File | Where-Object { $imgExt -contains $_.Extension.ToLower() } | ForEach-Object {
  Copy-Item -LiteralPath $_.FullName -Destination (Join-Path $Dest $_.Name)
}
