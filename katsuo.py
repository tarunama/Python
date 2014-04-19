import csv

#各サイズのリストをつくる
s       = []
m       = []
l       = []
#平均のリストをつくる
Avg     = []

#CSVを読み込む
data    = "katsuo1000.csv"
csvfile = open(data)

for row in csv.reader(csvfile):
    #カツオのみを抽出する
    if(row[0] == "カツオ"):
        #サイズごとに分岐
        if(int(row[1]) < 50):
            s.append(row[1])
        elif(int(row[1]) > 74):
            l.append(row[1])
        else:
            m.append(row[1])
            
#サイズごとに分類されたリストをつくる
lst = [s, m, l]

#各サイズの平均を求める
for i in range(3):
    Avg.append(sum(map(int,lst[i])) / len(lst[i]))

#出力する
print('S(' , len(lst[0]) , '):' , round(Avg[0],2) , 'cm')
print('M(' , len(lst[1]) , '):' , round(Avg[1],2) , 'cm')
print('L(' , len(lst[2]) , '):' , round(Avg[2],2) , 'cm')

csvfile.close()
