dim xHttp: Set xHttp = createobject("Microsoft.XMLHTTP")
dim bStrm: Set bStrm = createobject("Adodb.Stream")
xHttp.Open "GET", "http://fedeploycheck.fireeye.com/appliance-test/test-infection.exe", False
xHttp.Send

hdr = xHttp.getResponseHeader("Content-Disposition")

Wscript.Echo xHttp.repsponseText

with bStrm
    .type = 1 '//binary
    .open
    .write xHttp.responseBody
    .savetofile "c:\temp\test-infection.exe", 2 '//overwrite
end with



WScript.Echo "Press [ENTER] to continue..."
WScript.StdIn.ReadLine
WScript.Echo "Done."