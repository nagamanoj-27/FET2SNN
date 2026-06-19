[void][System.Reflection.Assembly]::LoadWithPartialName("System.Drawing")
$img = [System.Drawing.Image]::FromFile("C:\Users\CYNIX\.gemini\antigravity\brain\77231db2-b70b-426d-994a-39164eda131a\media__1781614920257.png")
$bmp = New-Object System.Drawing.Bitmap($img)
Write-Output "Image Dimensions: $($bmp.Width)x$($bmp.Height)"
for ($y = 0; $y -lt $bmp.Height; $y++) {
    for ($x = 0; $x -lt $bmp.Width; $x++) {
        $p = $bmp.GetPixel($x, $y)
        if ($p.R -lt 240 -or $p.G -lt 240 -or $p.B -lt 240) {
            Write-Output "Pixel at ($x,$y): R=$($p.R), G=$($p.G), B=$($p.B) (Hex: #$($p.R.ToString('X2'))$($p.G.ToString('X2'))$($p.B.ToString('X2')))"
        }
    }
}
