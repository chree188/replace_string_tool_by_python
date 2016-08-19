# encoding: utf-8
#-*_coding:utf8-*-
import re
import sys
import os
import os.path
import chardet
import shutil


rootdir = os.path.join(sys.path[0], "src")


def replace_string_by_tuplpcfg(directory):
    t_list = []

    r = open("replacestring_cfg.lua","r")
    for line in r:
        ind = line.split("=")
        a = ind[0].strip().strip("\n")
        b = ind[1].strip().strip("\n")
        t_tuple = (a,b)
        t_list.append(t_tuple)
    r.close()

    print '-- replace string start --'
    for a,b in t_list:
        print a + " = " + b
    print '-- replace string end --\n'
        
    replace_string_by_tuplp(directory, t_list)


def replace_string_by_tuplp(directory, tuple_list):
    dir_path = os.path.join(sys.path[0], directory)
    #print "dir_path:" + dir_path

    dir_new = re.sub(directory, directory + "_new", dir_path)
    if os.path.exists(dir_new):
        shutil.rmtree(dir_new)

    print "replace start."
    change_line_amount = 0
    for parent,dirnames,filenames in os.walk(dir_path):
        for filename in filenames:
            file_full_name = os.path.join(parent,filename)
            #print "file_full_name:" + file_full_name
            
            if filename.find('.lua') == -1:
                continue

            dir_path_new = re.sub(directory, directory + "_new", parent)
            #print "dir_path_new:" + dir_path_new
            
            isExists=os.path.exists(dir_path_new)
            if not isExists:
                os.makedirs(dir_path_new)

            file_full_name_new = re.sub(directory, directory + "_new", file_full_name)
            f = open(file_full_name_new, 'w')

            
            r = open(file_full_name, 'r')
            for line in r:
                wline = line
                #wline = wline.replace("\\", "\\\\")
                wline = wline.replace("\'", "\"")
                split_str = re.split("\"", wline)

                changed = False
                if len(split_str) > 1:
                    index = 0
                    list_result_str = []
                    for item_str in split_str:
                        if (index+1) % 2 == 0:
                            result_str = item_str
                            for str_src, str_dir in tuple_list:
                                #re_match_str = get_re_match_str(str_src)
                                re_match_str = str_src

                                if check_except_string(result_str) == False:
                                    if re.search(re_match_str,result_str):
                                        result_str = result_str.replace(str_src, str_dir)
                                        changed = True
                            list_result_str.append(result_str)
                        else:
                            list_result_str.append(item_str)
                        index = index + 1
                        
                    new_line = ""
                    index = 0
                    for s in list_result_str:
                        index = index + 1
                        if index == len(list_result_str):
                            new_line = new_line + s
                        else:
                            new_line = new_line + s + "\""
                    wline = new_line

                if changed:
                    change_line_amount = change_line_amount + 1
                    print "index: %d" % change_line_amount +".file from: " + file_full_name
                    _type = sys.getfilesystemencoding()
                    print r"changed line: " + line.decode('utf-8').encode(_type).strip("\n")
                    print r"now line: " + wline.decode('utf-8').encode(_type).strip("\n") + "\n"

                f.write(wline)
            r.close()
            f.close()
    print "replace end. total line: %d" % change_line_amount


#字符串中有"/","Sys"符号的忽略
except_list = ["/", "Sys"]
def check_except_string(cstr):
    for except_item in except_list:
         if cstr.find(except_item) > -1:
             return True
    return False


def get_re_match_str(st):
    return "%s([^/]|$)" % st
            
'''
def get_re_str(st):
    return r"[\"|'][^\"]*%s[^\"]*[\"|']" % st
'''

#replace_string_by_tuplp("src", (("太阳","月亮"),("大","小")))

#replace_string_by_tuplpcfg("src")

if __name__ == '__main__':
    replace_string_by_tuplpcfg("src")












