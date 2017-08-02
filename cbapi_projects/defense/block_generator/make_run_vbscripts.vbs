dim curDate, objFSO, outFile, shell, fname

curDate = Year(Date) &_
 right("0" & Month(Date), 2) &_
 right("0" &Day(Date),2) &_ 
 "-" &_
 right("0" & Hour(Time),2) &_
 right("0" & Minute(Time),2) &_
 right("0" & Second(Time),2)


 Function TestFolderStatus(fldr)
   Set objFSO = CreateObject("Scripting.FileSystemObject")
   If Not (objFSO.FolderExists(fldr)) Then
      objFSO.CreateFolder(fldr)
   End If
End Function

set objFSO = CreateObject("Scripting.FileSystemObject")
set shell = CreateObject("WScript.Shell")
rem destPath = shell.SpecialFolders("Desktop")
destPath = "c:\test"

TestFolderStatus(destPath)
fname = destPath & "\" & curDate & ".vbs"
set outFile = objFSO.CreateTextFile(fname, True)

outFile.WriteLine "fname=""" & fname & """"
outFile.WriteLine "MsgBox ""We ran the new vbs file """ & "&vbCrLf &fname" & ", vbCritical, ""The New VBS Ran"""
outFile.Close

shell.CurrentDirectory = destPath
shell.Run fname, 1, True

