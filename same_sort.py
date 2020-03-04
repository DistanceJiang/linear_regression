# coding=utf-8

#从文件里提取二维数组
def readData(filePath):
    file=open(filePath,'r')
    lines=file.readlines()
    data=[]
    for line in lines:
        line.encode('utf-8')
        print(line)
        mid=line[1:-2].split(',')
        for i in range(len(mid)):
            mid[i]=mid[i].split(' ')[-1][1:-1]
        data.append(mid)
    return data

lists2D = readData('two_dimension.txt')
row = len(lists2D)#二维数组的行数
col = len(lists2D[0])#二维数组的列数
flag_lists = [[0 for i in range(col)] for j in range(row)]#创建二维数组对应的标志数组


def find_same(two_dimension_lists, x, y, sort_list):
    if x<0 or x>=row or y<0 or y>=col :
        return
    elif two_dimension_lists[x][y] == '无' :
        return
    elif two_dimension_lists[x][y] == '横线':
        if y>0 and two_dimension_lists[x][y-1] in ['横线','正斜线','反斜线'] and flag_lists[x][y-1] == 0:
            sort_list.append([x,y-1])
            flag_lists[x][y-1] = 1
            find_same(two_dimension_lists,x,y-1,sort_list)
        if y<col-1 and two_dimension_lists[x][y+1] in ['横线','正斜线','反斜线'] and flag_lists[x][y+1] == 0:
            sort_list.append([x,y+1])
            flag_lists[x][y+1] = 1
            find_same(two_dimension_lists,x,y+1,sort_list)
    elif two_dimension_lists[x][y] == '竖线':
        if x>0 and two_dimension_lists[x-1][y] in ['竖线','正斜线','反斜线'] and flag_lists[x-1][y] == 0:
            sort_list.append([x-1,y])
            flag_lists[x-1][y] = 1
            find_same(two_dimension_lists,x-1,y,sort_list)
        if x<row-1 and two_dimension_lists[x+1][y] in ['竖线','正斜线','反斜线'] and flag_lists[x+1][y] == 0:
            sort_list.append([x+1,y])
            flag_lists[x+1][y] = 1
            find_same(two_dimension_lists,x+1,y,sort_list)
    elif two_dimension_lists[x][y] == '正斜线':
        if x>0 and y<col-1 and two_dimension_lists[x-1][y+1] == '正斜线' and flag_lists[x-1][y+1] == 0:
            sort_list.append([x-1,y+1])
            flag_lists[x-1][y+1] = 1
            find_same(two_dimension_lists,x-1,y+1,sort_list)
        if x<row-1 and y>0 and two_dimension_lists[x+1][y-1] == '正斜线' and flag_lists[x+1][y-1] == 0:
            sort_list.append([x+1,y-1])
            flag_lists[x+1][y-1] = 1
            find_same(two_dimension_lists,x+1,y-1,sort_list)
        if y>0 and two_dimension_lists[x][y-1] in ['横线','反斜线'] and flag_lists[x][y-1] == 0:
            sort_list.append([x,y-1])
            flag_lists[x][y-1] = 1
            find_same(two_dimension_lists, x, y-1, sort_list)
        if y<col-1 and two_dimension_lists[x][y+1] in ['横线','反斜线'] and flag_lists[x][y+1] == 0:
            sort_list.append([x,y+1])
            flag_lists[x][y+1] = 1
            find_same(two_dimension_lists, x, y+1, sort_list)
        if x>0 and two_dimension_lists[x-1][y] in ['竖线','反斜线'] and flag_lists[x-1][y] == 0:
            sort_list.append([x-1,y])
            flag_lists[x-1][y] = 1
            find_same(two_dimension_lists, x-1, y, sort_list)
        if x<row-1 and two_dimension_lists[x+1][y] in ['竖线','反斜线'] and flag_lists[x+1][y] == 0:
            sort_list.append([x+1, y])
            flag_lists[x+1][y] = 1
            find_same(two_dimension_lists, x+1, y, sort_list)
    elif two_dimension_lists[x][y] == '反斜线':
        if x>0 and y>0 and two_dimension_lists[x-1][y-1] == '反斜线' and flag_lists[x-1][y-1] == 0:
            sort_list.append([x-1,y-1])
            flag_lists[x-1][y-1] = 1
            find_same(two_dimension_lists, x-1, y-1, sort_list)
        if x<row-1 and y<col-1 and two_dimension_lists[x+1][y+1] == '反斜线' and flag_lists[x+1][y+1] == 0:
            sort_list.append([x+1,y+1])
            flag_lists[x+1][y+1] = 1
            find_same(two_dimension_lists, x+1, y+1, sort_list)
        if y>0 and two_dimension_lists[x][y-1] in ['横线','正斜线'] and flag_lists[x][y-1] == 0:
            sort_list.append([x,y-1])
            flag_lists[x][y-1] = 1
            find_same(two_dimension_lists, x, y-1, sort_list)
        if y<col-1 and two_dimension_lists[x][y+1] in ['横线','正斜线'] and flag_lists[x][y+1] == 0:
            sort_list.append([x,y+1])
            flag_lists[x][y+1] = 1
            find_same(two_dimension_lists, x, y+1, sort_list)
        if x>0 and two_dimension_lists[x-1][y] in ['竖线','正斜线'] and flag_lists[x-1][y] == 0:
            sort_list.append([x-1,y])
            flag_lists[x-1][y] = 1
            find_same(two_dimension_lists, x-1, y, sort_list)
        if x<row-1 and two_dimension_lists[x+1][y] in ['竖线','正斜线'] and flag_lists[x+1][y] == 0:
            sort_list.append([x+1, y])
            flag_lists[x+1][y] = 1
            find_same(two_dimension_lists, x+1, y, sort_list)

def traverse_list2D(list2D):
    sort_lists = []
    k = -1
    for x in range(row):
        for y in range(col):
            if list2D[x][y] in ['横线','竖线','正斜线','反斜线'] and flag_lists[x][y] == 0:
                sort_lists.append([])
                k = k+1
                find_same(list2D,x,y,sort_lists[k])
    sort_lists = [t for t in sort_lists if t]
    for i in range(len(sort_lists)):
        print(sort_lists[i])
    return sort_lists

print(traverse_list2D(lists2D))