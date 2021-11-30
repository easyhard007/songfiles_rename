import re
from zhconv import convert
import xlwt
import xlrd
import os

#用来修正错误的歌手名
artistMap = {}
artistMap['+ 7F'] = '5566'
artistMap['+ 7F + K'] = '5566'
artistMap['A'] = 'A-lin'
artistMap['A lin'] = 'A-lin'
artistMap['谱'] = ''

#忽略删除首字母和首数字的歌曲名单
songProtect = {'281公里','C大调','K歌之王','K歌情人','A级娱乐','123木头人','101封情书','612星球','127日','101封情书','123我爱你','118最新排行'}

#特殊处理
specialProcess = {}
specialProcess['122 2012_五月天'] = {'song_name':'2012','artist':'五月天'}

#特殊歌手名
specialArtist = {'5566'}


def write_data_to_excel(datas,path):

    workbook = xlwt.Workbook(encoding = 'utf-8')
    worksheet = workbook.add_sheet('datas')
    style = xlwt.XFStyle() # 初始化样式
    font = xlwt.Font() # 为样式创建字体
    font.name = 'Times New Roman' 
    font.bold = True # 黑体
    style.font = font # 设定样式
    worksheet.write(0,0,  '歌曲名',style)
    worksheet.write(0,1,  '歌手名',style)
    worksheet.write(0,2,  '原文件名',style)
    worksheet.write(0,3, '重命名文件名',style)

    new_file_name_set = set()

    for i in range(0,len(datas)):
        data = datas[i]
        worksheet.write(i+1,0, data['song_name'])
        worksheet.write(i+1,1, data['artist'])
        worksheet.write(i+1,2, data['file_name'])
        if(data['artist']!=''):
            new_file_name = data['song_name'] + " - " + data['artist']+".pdf";
        else:
            new_file_name = data['song_name']+".pdf";
        if (new_file_name in new_file_name_set):
            new_file_name = new_file_name.replace('.pdf', ' (2).pdf')
        new_file_name_set.add(new_file_name)
        worksheet.write(i+1,3, new_file_name)

    workbook.save(path)


def analysis_file_names(path):
    datas = []

    with open(path,'r') as file:#r为标识符，表示只读
        contents = file.readlines()
    for filename in contents:
        filename_simp= convert(filename.strip(), 'zh-cn')
        filename_split = re.split('）|（|-|\(|\)|_|＿|—|\d{1,4}(\ ){1,3}\d{1,4}(\ ){1,3}\d{1,4}(\ ){1,3}|\d{1,4}(\ ){1,3}\d{1,4}(\ ){1,3}|\d{1,4}(\ ){1,3}',filename_simp)
        filename_noEmpty = [x for x in filename_split if x]
        filename_noNumbers = [x for x in filename_noEmpty if(not x.isdigit() and x!=' ')]
        for i in range(0,len(filename_noNumbers)):
            attr = filename_noNumbers[i]
            searchObj = re.search( r'[A-Z][\u4e00-\u9fa5]{1,}', attr, re.M|re.I)
            if(searchObj and searchObj.span()[0]==0 and attr not in songProtect):
                print(attr,attr[1:])
                filename_noNumbers[i] = attr[1:]
        # print(filename_noEmpty)
        dataDict = {}
        dataDict["song_name"] = ''
        dataDict["artist"] = ''
        dataDict["file_name"] = filename.replace('\n','')+".pdf"
        if (len(filename_noNumbers)==1): #只有歌名
            dataDict["song_name"] = filename_noNumbers[0].strip()
        if (len(filename_noNumbers)>=2): #有歌名跟歌手
            dataDict["song_name"] = filename_noNumbers[0].strip()
            dataDict["artist"] = filename_noNumbers[1].strip()
        if (len(filename_noNumbers)>=2): #有歌名跟歌手
            dataDict["song_name"] = filename_noNumbers[0].strip()
            dataDict["artist"] = filename_noNumbers[1].strip()

        #修改错误识别的歌手名
        if(dataDict["artist"] in artistMap.keys()):
            dataDict["artist"] = artistMap[dataDict["artist"]]
        for specialArtistName in specialArtist:
            if specialArtistName in filename.strip():
                dataDict["artist"] = specialArtistName
                print("特殊歌手：",dataDict)

        #修改以三个数字开头的歌名
        searchObj = re.search( r'[0-9]{3}[\u4e00-\u9fa5]{1,}', dataDict["song_name"], re.M|re.I)
        if(searchObj and searchObj.span()[0]==0 and dataDict["song_name"] not in songProtect):
            print(dataDict["song_name"],dataDict["song_name"][3:])
            dataDict["song_name"] = dataDict["song_name"][3:]

        # 避免空白
        if(dataDict["song_name"]==''):
            dataDict["song_name"] = filename.strip()

        # 特殊处理
        if(filename.strip() in specialProcess.keys()):
            dataDict["song_name"] = specialProcess[filename.strip()]["song_name"]
            dataDict["artist"] = specialProcess[filename.strip()]["artist"]
            print("特殊处理：",filename.strip(),dataDict["song_name"],dataDict["artist"])
            

        datas.append(dataDict)

    # for data in datas:
    #     print("歌曲名：",data["song_name"] ,"\t 歌手:",data["artist"],"\t 文件名:",data["file_name"])
    
    return datas

#根据datas批量修改文件夹中的文件名
def rename_files(excel_file,folder_path,log_path=None):
    fileList=os.listdir(folder_path)
    log_str = []
    if(log_path==None):
        log_path = folder_path+"/log_rename.txt"


    readbook = xlrd.open_workbook(excel_file)
    sheet = readbook.sheet_by_name('datas')#索引的方式，从0开始
    nrows = sheet.nrows
    fileNameList = (list(os.listdir(folder_path)))
    print("--------fileNames--------")
    for i in range(0,len(fileNameList)):
        print(fileNameList[i])
    print("------------------------")
    for i in range(1,nrows):
        oldname = os.path.join(folder_path,sheet.row(i)[2].value)
        newname = os.path.join(folder_path,sheet.row(i)[3].value)
        # if(oldname not in fileNameList):
        #     log_str.append(oldname+" not in the folder. Skipped.")
        #     continue
        if(newname in fileNameList):
            log_str.append(newname+" is in the folder. Skipped.")
            continue
        try:
            os.rename(oldname,newname)  
        except IOError:
            print(IOError)
            continue
        log_str.append("\""+sheet.row(i)[2].value +"\" is renamed to \""+sheet.row(i)[3].value)

    with open(log_path,"w") as logfile:  
        for i in range(0,len(log_str)):
            content = log_str[i] + "\n"
            logfile.write(content.encode("gbk", 'ignore').decode("gbk", "ignore"))
        
    
if __name__ == "__main__":
    datas = analysis_file_names("b.txt")
    write_data_to_excel(datas,"pdf批量重命名.xls")
    rename_files(r'pdf批量重命名.xls','C:/Users/easyh/Desktop/台湾谱/')
