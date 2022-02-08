import pythoncom
import win32com.client

sw = win32com.client.Dispatch("EModelViewer.EDrwViewer64")

sDocFileName = r'E:\Users\SUN\Desktop\test1.sldprt'

sw.openDoc(sDocFileName, True, False, True, "")

#s=sw.Save('111222.bmp', True, None)
s=sw.FileName
print("1")
