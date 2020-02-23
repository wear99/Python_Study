import win32com.client #系统客户端包

speaker = win32com.client.Dispatch("SAPI.SPVOICE")  #系统接口

a=[1,2,3,4]
str1=str(a)
print(str1)
speaker.speak(str1)
