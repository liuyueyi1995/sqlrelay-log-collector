import os

def collect_log(totallog_path,log_path):
    '''
    功能：将分散的多个日志文件整合到一个总日志中，并删除分日志
    参数：totallog_path，总日志所在路径
          log_path，分日志所在路径
    '''
    
    try:    
        log_list = os.listdir(log_path)
        print(log_list)
        with open(totallog_path,"a") as totallog:
            os.chdir(log_path)
            for each in log_list:
                if os.path.getsize(each):
                    with open(each,"r") as log:
                        lines = log.readlines()
                        totallog.writelines(lines)
                os.remove(each)
    except Exception as e:
        print(e)
    
        
def decorate_log(totallog_path,finallog_path):
    '''
    功能：将总日志转换成splunk需求的格式
    参数：totallog_path，总日志所在路径
    '''
    log_dict = {}
    i = 0
    
    if not os.path.exists(totallog_path):
        os.mknod(totallog_path)

    with open(totallog_path,"r") as totallog:
        with open(finallog_path,"a") as finallog:
            lines = totallog.readlines()
            for each in lines:
                tmp_list = each.split(":",1)
                log_dict[tmp_list[0]] = tmp_list[1][:-1] #[:-1]用于去掉换行符
                i += 1

                if i==7: #i等于7 一条日志有7行，所以每7行组成一个字典
                    sqlquery = log_dict["query"] #将query拆分成sql语句和用户
                    tmp = sqlquery.rsplit("#web-user=",1) #从后向前split拆分出最后一个"#web-user="之后的字段
                    log_dict["user"] = tmp[1]
                
                    if log_dict["status"]=="0":
                        status="[PASS]"
                        result="fetched "+log_dict["rows fetched"]+" rows during "+log_dict["execution time"]+"s"
                    elif log_dict["status"]=="2":
                        status="[DENY]"
                        result="fetched "+log_dict["rows fetched"]+" rows during "+log_dict["execution time"]+"s"
                    else:
                        status="[ERROR:"+log_dict["error number"]+"]"
                        result="during "+log_dict["execution time"]+"s"
        
                    string = log_dict["date time"]+" "+status+" "+log_dict["user"]+" \""+log_dict["query"]+"\" "+result+"\n"
                    finallog.writelines(string)
                
                    log_dict = {}
                    i = 0


if __name__=='__main__':
    
    collect_log(r"C:\Users\Yueyi\Desktop\dir1\logfile",r"C:\Users\Yueyi\Desktop\dir1\log") 
    decorate_log(r"C:\Users\Yueyi\Desktop\dir1\logfile",r"C:\Users\Yueyi\Desktop\dir1\finallog")
