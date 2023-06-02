$files = Get-ChildItem . -Recurse -Exclude *.log, *.ps1
foreach ($f in $files){
	try {
	
		$outfile = $f.FullName + "_h265.mp4"
		$dt = Get-Date
		Add-Content -Value "$dt Compressing $outfile " -Path ffmpeg_compression.log
		ffmpeg -i $f.FullName -vcodec libx265 -crf 22 $outfile
		$dt = Get-Date
		Add-Content -Value "$dt Done $outfile" -Path ffmpeg_compression.log
		#Remove-Item -Path $f.FullName
		#Add-Content -Value "$dt ***Removed Done $f.FullName" -Path ffmpeg_compression.log
    } catch {
		Add-Content -Value "$dt Error while processing: $f.FullName" -Path ffmpeg_compression.log
    }
}
