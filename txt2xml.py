#!/usr/bin/python
# -*- coding: utf-8 -*-

import re, time, sys, os

def txt2xml(file):
    servicename = file.split('\\')[-1][:-4]
    serviceInfo = getserviceInfo(servicename)
    
    if not os.path.isfile(file):
        print("'"+file+"' not found")
        return
    if(serviceInfo[0]==""):
        print("'"+servicename+"' not found in config.txt")
        return
    
    fp = open(serviceInfo[1], "w", encoding="utf-8")
    fp.write("<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n")
    fp.write("<MHPEventPG providerName=\"" + servicename + "\" downDate=\""+serviceInfo[2]+"\">\n")
    
    with open(file, "r") as f:
        data = f.read()
    #print(data)
    
    rule = re.compile(r'\d{4}-\d{2}-\d{2}', re.DOTALL)
    days = rule.findall(data.replace("/", "-"))
    #print(days)
    
    fp.write("\t<Service serviceKey=\"" + serviceInfo[0] + "\" type=\"Normal\" overwrite=\"True\" start=\"" + days[0] + " 00:00:00\" end=\"" + days[-1] + " 00:00:00\"/>\n")
    
    id1=1
    epgs = data.split("\n\n")
    for j in range(len(epgs)):
        rule = re.compile(r'\d{2}:\d{2} \S+', re.DOTALL)
        epg = rule.findall(epgs[j])
        
        print("----------\t"+days[j]+"\t----------")
        #print(epg)
        
        epglist1 =[]
        epglist2 =[]
        for i in range(len(epg)):
            tmp = epg[i].split(" ")
            if(i==0 and tmp[0]!="00:00"):
                epglist1.append(["00:00","续前节目"])
            epglist1.append(tmp)
            if(i==len(epg)-1 and tmp[0]!="24:00"):
                epglist1.append(["24:00",""])
        #print(epglist1)
        
        for i in range(len(epglist1)-1):
            tmp = ctime(epglist1[i][0],epglist1[i+1][0])
            if(tmp != "-1"):
                epglist2.append([epglist1[i][0]+":00",tmp,epglist1[i][1]])
            else:
                print("error:"+epglist1[i][0]+","+epglist1[i][1])
        #print(epglist2)
        
        id2=days[j].split("-")[2].lstrip('0')
        for i in range(len(epglist2)):
            id0=id2+str(id1).rjust(4,'0')
            id1=id1+1
            
            #print(id0)
            #print(epglist2[i])
            
            fp.write("\t<Event date=\"" + days[j] + "\" id=\"" + id0 + "\" actionType=\"INSERT\">\n")
            fp.write("\t\t<EventName lang=\"chi\" name=\"" + epglist2[i][2] + "\">\n")
            fp.write("\t\t\t<EventText/>\n")
            fp.write("\t\t</EventName>\n")
            if(j==len(epgs)-1 and i==len(epglist2)-1):
                fp.write("\t\t<Period start=\"" + epglist2[i][0] + "\" duration=\"010000\"/>\n")
            else:
                fp.write("\t\t<Period start=\"" + epglist2[i][0] + "\" duration=\"" + epglist2[i][1] + "\"/>\n")
            fp.write("\t\t<Content level1=\"1\" level2=\"0\"/>\n")
            fp.write("\t\t<Rating>\n")
            fp.write("\t\t\t<RatingInfo country=\"902\" rating=\"0\"/>\n")
            fp.write("\t\t</Rating>\n")
            fp.write("\t</Event>\n")
        
        print("count = "+str(len(epglist2)))
    
    fp.write("</MHPEventPG>\n")
    fp.close()
    
    return


def ctime(time1, time2):
    if(time2 == ""):
        time2 = "24:00"
    
    t1 = time1.split(":")
    t2 = time2.split(":")
    
    #t1h:t1[0],t1m:t1[1]
    #t2h:t2[0],t2m:t2[1]
    secs = (int(t2[0])*60 + int(t2[1]) -int(t1[0])*60 -int(t1[1]))*60
    if(secs <= 0):
        secs =-1
    return str(secs)


def getserviceInfo(servicename):
    serviceid=""
    savename=""
    tsid=""
    date = time.localtime()
    nowdate=time.strftime("%Y-%m-%d %H:%M:%S", date)
    
    with open("config.txt", "r") as f:
        data = f.read().splitlines()
    
    slist=[]
    for l in data:
        if(l[0]=="#"):
            continue
        slist.append(l.split(','))
    for l in slist:
        if(l[0]==servicename):
            serviceid=l[1]
            tsid=l[2]
            break
    
    if(tsid!=""):
        savename="ITV_TS"+tsid+"Service"+serviceid.rjust(3,'0')+time.strftime("%m%d%H%M", date)+".xml"
    
    return [serviceid, savename, nowdate]


if __name__ == "__main__":
    if(len(sys.argv)>1):
        txt2xml(sys.argv[1])
        #input("Any Key to exit..")
    #print(getserviceInfo("test"))
    