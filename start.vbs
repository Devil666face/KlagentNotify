Set oShell = Wscript.CreateObject("WScript.Shell")
CommandLine = "%COMSPEC% /c C:\KlagentNotify\venv\Scripts\python.exe C:\KlagentNotify\bot.pyw"
oShell.Run CommandLine, 0, 0