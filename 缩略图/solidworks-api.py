import pythoncom
import win32com.client

# 或者使用下面的方法，使用启动独立的进程：
# w = win32com.client.DispatchEx('Word.2233')

#后台运行，不显示，不警告
#w.Visible = 0
#w.DisplayAlerts = 0


sw = win32com.client.Dispatch("SldWorks.Application")
sw.Visible = True

sDocFileName = 'E:\\Users\\SUN\\Desktop\\test1.sldprt'
nDocType = 'swDocPART'

#model=sw.OpenDoc6(sDocFileName, 'swDocPART',1, "", None, None)

model = sw.openDoc(sDocFileName, 1)   #打开文件，prt:1,ass:2,drw:3
r = model.SaveBMP('11122.bmp', 1000, 1000)  #另存在图片

#s=sw.GetPreviewBitmap(sDocFileName,'')
#print(model.GetPathName)
print("1")
