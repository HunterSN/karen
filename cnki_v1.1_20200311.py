import os
import bs4
import requests
from urllib import request
import re
from selenium import webdriver
from time import sleep
import csv
from lxml import etree
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains

def cnkiSingle(drug):
    drugInput = "SU = " + drug
    print(drugInput)

    wuzhaiyao = drug + 'wuzhiyao.txt'
    youzhaiyao = drug + 'youzhaiyao.txt'
    weixia = drug + 'weixiazai.txt'
    outJiandan = open(wuzhaiyao,'a+')
    outShaixuan = open(youzhaiyao,'a+')
    weixiazai = open(weixia,'a+')
    outJiandan.close()
    outShaixuan.close()
    weixiazai.close()



    browserCnki = webdriver.Firefox()
    browserCnki.get('https://kns.cnki.net/kns/brief/result.aspx?dbprefix=SCDB&crossDbcodes=CJFQ,CDFD,CMFD,CPFD,IPFD,CCND,CCJD')
    print('登陆账号并点击“专业检索”后按回车键')
    zhunBei = input()
    # buttonGaoji = browserCnki.find_element_by_xpath('/html/body/form[1]/div[4]/div[2]/div/dl/dl/dt/ul/li[2]/a')
    # buttonGaoji.click()

    # 检索药物，获取计数
    searchDrug =browserCnki.find_element_by_id('expertvalue')
    searchDrug.send_keys(drugInput)
    searchButton = browserCnki.find_element_by_id('btnSearch')
    searchButton.click()
    sleep(8)
    browserCnki.switch_to_frame('iframeResult')
    drugCount = browserCnki.find_element_by_xpath('/html/body/form/table/tbody/tr[1]/td/table/tbody/tr[2]/td/table/tbody/tr/td[2]/div/div').text
    print(drugCount)

    #二次疾病筛选，获取计数，题名，作者，来源，发表时间，数据库
    browserCnki.switch_to_default_content()
    searchDrug.clear()
    searchWords = "SU = ’胸痹心痛’+’胸痹’+真心痛’+’增强型心绞痛’+’心脏动脉瘤’+’心源性猝死’+’心绞痛伴有痉挛’+’心绞痛’+’心肌梗死后心绞痛’+’无症状心肌缺血’+’稳定型心绞痛’+’特指类型慢性缺血性心脏病’+’缺血性心肌病’+’慢性缺血性心脏病’+’慢性冠状动脉供血不足’+’劳力型心绞痛’+’急性再发心肌梗死’+’急性心内膜下心肌梗死’+’急性心肌缺血’+’急性心肌梗死’+’急性透壁正后壁心肌梗塞’+’急性透壁右室心肌梗塞’+’急性透壁心肌梗塞’+’急性透壁高侧壁心肌梗塞’+’急性冠状动脉供血不足’+’急性冠脉综合征’+’急性非ST段抬高型心肌梗塞’+’急性ST段抬高型右室心肌梗塞’+’急性ST段抬高型心肌梗塞’+’混合型心绞痛’+’冠状动脉粥样硬化性心脏病’+’冠状动脉粥样硬化’+’冠状动脉支架内血栓形成’+’冠状动脉再狭窄’+’冠状动脉炎’+’冠状动脉血栓形成’+’冠状动脉性心脏病’+’冠状动脉狭窄’+’冠状动脉旁路术后心肌梗塞’+’冠状动脉瘤’+’冠状动脉痉挛’+’冠状动脉介入治疗术后心肌梗塞’+’冠状动脉疾病’+’冠状动脉动脉瘤’+’冠状动脉闭塞’+’冠脉-锁骨下动脉窃血综合征’+’非Q波心肌梗塞’+’动脉硬化性心脏病’+’陈旧性心肌梗死’+’不稳定性心绞痛’+’变异型心绞痛’"
    searchDrug.send_keys(searchWords)
    secButton = browserCnki.find_element_by_xpath('/html/body/form[1]/div[4]/div[2]/div/dl/div[2]/dl/dd[1]/div[1]/span/a')
    secButton.click()
    sleep(10)
    browserCnki.switch_to_frame('iframeResult')
    pageCount = browserCnki.find_element_by_xpath('/html/body/form/table/tbody/tr[1]/td/table/tbody/tr[2]/td/table/tbody/tr/td[2]/div/span[1]').text
    pageCount = int(str(pageCount).replace('1','').replace('/',''))
    print(pageCount)



    secdrugCount = browserCnki.find_element_by_xpath('/html/body/form/table/tbody/tr[1]/td/table/tbody/tr[2]/td/table/tbody/tr/td[2]/div/div').text
    print(secdrugCount)

    outJiandan = open(wuzhaiyao,'a+')
    outJiandan.write('一次检索' + '$' + drugCount + '\n')
    outJiandan.write('二次检索' + '$' + secdrugCount + '\n')
    outJiandan.write('二次检索页数' + '$' + str(pageCount) + '\n')
    outJiandan.close()

    startPage = 1
    pageCountt = pageCount


    #修改页数，还有验证码
    # tiaozhuanye = 1
    # startPage = 4
    # while tiaozhuanye < 4:
    #     browserCnki.find_element_by_xpath('/html/body/form/table/tbody/tr[3]/td/table/tbody/tr/td/div/a[1]').send_keys(Keys.RIGHT)
    #     sleep(2) 
    #     tiaozhuanye = tiaozhuanye + 1
    #     pass
 

    while startPage <= pageCountt:
        titleName = browserCnki.find_elements_by_xpath('/html/body/form/table/tbody/tr[2]/td/table/tbody/tr/td[2]')
        autorName = browserCnki.find_elements_by_xpath('/html/body/form/table/tbody/tr[2]/td/table/tbody/tr/td[3]')
        sourceName = browserCnki.find_elements_by_xpath('/html/body/form/table/tbody/tr[2]/td/table/tbody/tr/td[4]')
        publishTime = browserCnki.find_elements_by_xpath('/html/body/form/table/tbody/tr[2]/td/table/tbody/tr/td[5]')
        databaseName = browserCnki.find_elements_by_xpath('/html/body/form/table/tbody/tr[2]/td/table/tbody/tr/td[6]')
        # downloadButton = browserCnki.find_elements_by_xpath('/html/body/form/table/tbody/tr[2]/td/table/tbody/tr/td[8]')
        pCount = len(titleName)
        i = 1
        
        while i < pCount:
            outTitle = titleName[i].text
            outAutor = autorName[i].text
            outSource = sourceName[i].text
            outPublish = publishTime[i].text
            outDatabase = databaseName[i].text
            print(outTitle,outAutor,outSource,outPublish,outDatabase)
            outJiandan = open(wuzhaiyao,'a+')
            outJiandan.write(outTitle + '$' + outAutor + '$' + outSource + '$' + outPublish + '$' + outDatabase + '$' + str(startPage) + '$' + str(i) + '\n')
            outJiandan.close()            
            i = i + 1
            pass
        
        
        m = 1
        while m < pCount:
            ii = m + 1
            xpathIn = '/html/body/form/table/tbody/tr[2]/td/table/tbody/tr[' + str(ii) + ']/td[8]/a'
            sleep(1)
            handlers = browserCnki.window_handles
            browserCnki.switch_to_window(handlers[0])
            tiaozhuan = browserCnki.find_element_by_xpath(xpathIn)
            browserCnki.execute_script('arguments[0].click();',tiaozhuan)

            #验证码

            if m == 1 and startPage ==1:
                print('输入验证码并下载第一次后按回车键')
                ceshid = input()
                pass
            else:                       
                sleep(2)
                pass
        
            xpathIn = '/html/body/form/table/tbody/tr[2]/td/table/tbody/tr[' + str(ii) + ']/td[2]/a'
            
            sleep(1)
            handlers = browserCnki.window_handles
            browserCnki.switch_to_window(handlers[0])
            tiaozhuan = browserCnki.find_element_by_xpath(xpathIn)
            browserCnki.execute_script('arguments[0].click();',tiaozhuan)

            sleep(8)
            try:
                handlers = browserCnki.window_handles
                browserCnki.switch_to_window(handlers[1])


                try:
                    browserCnki.find_element_by_xpath('/html/body/div[6]/div[3]/div[3]/div[1]/p[1]/span[2]').click()
                    pass
                except :
                    print('短')
                    pass
                
                try:
                    danTitle = browserCnki.find_element_by_xpath('/html/body/div[6]/div[3]/div[1]/h2').text
                    danAutor = browserCnki.find_element_by_xpath('/html/body/div[6]/div[3]/div[1]/div[1]/span/a').text
                    danDanwei = browserCnki.find_element_by_xpath('/html/body/div[6]/div[3]/div[1]/div[2]/span/a').text
                    danSource = browserCnki.find_element_by_xpath('/html/body/div[6]/div[3]/div[3]/div[2]/div[2]/p[1]/a').text
                    danSourceTime = browserCnki.find_element_by_xpath('/html/body/div[6]/div[3]/div[3]/div[2]/div[2]/p[3]/a').text
                    danDOI = browserCnki.find_element_by_xpath('/html/body/div[6]/div[3]/div[3]/div[1]/p[3]').text
                    danKeywords = browserCnki.find_element_by_xpath('/html/body/div[6]/div[3]/div[3]/div[1]/p[2]').text
                    danAbstract = browserCnki.find_element_by_xpath('/html/body/div[6]/div[3]/div[3]/div[1]/p[1]/span[1]').text
                    print(danTitle,danAutor,danDanwei,danSource,danSourceTime,danDOI,danKeywords,danAbstract)
                    outShaixuan = open(youzhaiyao,'a+')
                    outShaixuan.write(danTitle+ '$' + danAutor+ '$' + danDanwei+ '$' + danSource+ '$' + danSourceTime+ '$' + danDOI+ '$' + danKeywords+ '$' + danAbstract+ '$' + str(startPage) + '$' + str(m) + '\n')
                    outShaixuan.close()
                    pass
                except :
                    handlers = browserCnki.window_handles
                    browserCnki.switch_to_window(handlers[0])
                    cuowuPianming = browserCnki.find_element_by_xpath(xpathIn).text
                    print(cuowuPianming + '信息不全，手动修正')
                    weixiazai = open(weixia,'a+')
                    weixiazai.write(cuowuPianming + '信息不全，手动修正'+'\n')
                    browserCnki.switch_to_window(handlers[1])
                    weixiazai.close()
                    browserCnki.close()
                    m = m + 1
                    continue
                    pass
                
                
                browserCnki.close()
                sleep(1)
                browserCnki.switch_to_window(handlers[0])
                
                sleep(1)
                
                pass
            except :
                handlers = browserCnki.window_handles
                browserCnki.switch_to_window(handlers[0])
                cuowuPianming = browserCnki.find_element_by_xpath(xpathIn).text
                print(cuowuPianming + '下载错误，手动下载')
                weixiazai = open(weixia,'a+')
                weixiazai.write(cuowuPianming + '下载错误，手动下载'+'\n')
                weixiazai.close()
                m = m + 1
                continue
                pass
            else:
                m = m + 1
                print(str(m))
                pass
        
            
            pass
        
        browserCnki.find_element_by_xpath('/html/body/form/table/tbody/tr[3]/td/table/tbody/tr/td/div/a[1]').send_keys(Keys.RIGHT)
        
        sleep(2) 
        startPage = startPage + 1
            







    
jiansu = "'心宝丸'"
    


cnkiSingle(jiansu)



