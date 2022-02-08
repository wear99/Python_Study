import win32com
from win32com.shell import shell, shellcon

s=shell.SHGetFileInfo(r'E:\Users\SUN\Desktop\11122.bmp',0, shellcon.SHGFI_SYSICONINDEX | shellcon.SHGFI_ICON | shellcon.SHGFI_LARGEICON)

print('1')