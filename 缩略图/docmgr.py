#extern "C"__declspec(dllexport)
import ctypes
import pythoncom
import win32com.client

#sw = ctypes.WinDLL(r'C:\Program Files\Common Files\SolidWorks Shared\swdocumentmgr.dll')
sw = win32com.client.Dispatch("SwDocumentMgr.SwDMClassFactory")

d=sw.GetApplication('123142')
d = sw.GetApplication('123142')
#d.GetApplication('123142')

#ISwDMClassFactory::GetApplication
sw.GetTableDisplayList()

print('1')