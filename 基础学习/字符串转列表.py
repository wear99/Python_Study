laohu = 'are you sleeping are you sleeping brother john brother john'
laohu_list = laohu.split()   #使用空格将字符串进行分隔
print(laohu)
print(laohu_list)
print("g歌曲中共有%d个单词" % len(laohu_list))
x = input("请输入要查询的单词")
n = laohu_list.count(x)
print("你要查询的单词%s共出现了%d次" % (x,n))
