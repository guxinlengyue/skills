param(
  [Parameter(Mandatory=$true)][string]$Path
)

$imgExt = '.jpg','.jpeg','.png','.heic','.gif','.bmp','.tif','.tiff','.webp'
Get-ChildItem -LiteralPath $Path -File | Where-Object { $imgExt -contains $_.Extension.ToLower() } | ForEach-Object {
  if ($_.Attributes -band [IO.FileAttributes]::ReadOnly) {
    $_.Attributes = $_.Attributes -bxor [IO.FileAttributes]::ReadOnly
  }
}
