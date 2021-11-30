# songfiles_rename
# 曲谱文件批量重命名


The python code provides a rename batch procedure for song files, which contains song names and artist names in their file names. The format will be "Songname - Artirst.pdf".
This is done by split the original file names, and try to detect song names and artist names to geneerated the new formatted file names.

本项目的代码用于对大量歌曲曲谱（台湾谱）文件进行批量重命名，格式为"歌曲名 - 歌手名.pdf"。基本思路是识别原文件名中的各种分隔字符，然后提取出歌曲名和歌手名，当前部分文件识别不是很准确。建立本项目的初衷是处理8087份pdf台湾谱，这些曲谱来自不同源，不仅有大量重复，其命名还非常混乱，如下所示：
![image](https://user-images.githubusercontent.com/6952405/143989018-7a86de94-fb2a-48b6-b863-d45faf4a1af5.png)
![image](https://user-images.githubusercontent.com/6952405/143989037-57dbfc67-94b4-4d59-bcad-19149ade22a0.png)
![image](https://user-images.githubusercontent.com/6952405/143988856-655b407e-a3ad-4dae-b37e-e6834e7abe5d.png)

我首先通过合并文件夹并进行去重，整理出8087份不重复的文件，并使用python代码进行批量重命名。主要逻辑包括：
1. 文件名繁体转简体
2. 使用正则表达式分割原文件名，去掉类似010和A这样开头的数字和字母，并试图把歌曲名和歌手名分割出来
3. 分割后的字符串，提取出第一个有意义的语句作为歌曲名，提取出第二个有意义的语句作为歌手名
4. 使用 歌曲名 - 歌手名.pdf 作为新的文件名
当然以上步骤存在一些自动化处理无法覆盖的文件，大概有10个左右，我手工处理了这些文件。

处理后的文件名如下所示：
![image](https://user-images.githubusercontent.com/6952405/143989469-9c426c52-a7e6-47a0-8d1c-84665b091d33.png)




