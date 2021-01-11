#!/usr/bin/python3
# -*- coding:utf-8 -*-
import sys
import os
from configparser import ConfigParser
import time
from ctypes import *
import logging
import time
from PIL import Image,ImageDraw,ImageFont
import traceback
import calendar
import datetime
from datetime import date
from dateutil.parser import parse
from dateutil.rrule import rrule, DAILY


logging.basicConfig(level=logging.DEBUG)
calendar.setfirstweekday(firstweekday=0)
runningDir = os.path.dirname(os.path.realpath(__file__))
festivalsDays={}
holiDays={}
workDays={}

def DrawScreen(draw):
    today=datetime.date.today()
    Year = today.strftime('%Y')
    Month = today.strftime('%m')
    Day = today.strftime('%d')

    currentMonth = int(Month)
    currentYear = int(Year)
    position0Month = currentMonth - 1
    position0Year = currentYear
    position2Month = currentMonth + 1
    position2Year = currentYear     

    if(position0Month <= 0):
        position0Month = position0Month + 12
        position0Year = currentYear - 1
    if position2Month > 12:
        position2Month = position2Month - 12
        position2Year = position2Year + 1

    SetDayStatus(festivalsDays, holiDays, workDays, str(position0Year))
    SetDayStatus(festivalsDays, holiDays, workDays, str(currentYear))
    SetDayStatus(festivalsDays, holiDays, workDays, str(position2Year))

    draw.line((481, 0, 481, 400), fill = 0)
    draw.line((962, 0, 962, 400), fill = 0)
    draw.line((0, 400, 1448, 400), fill = 0)
    draw.line((724, 400, 724, 1072), fill = 0)

    DrawMonth(0, position0Year, position0Month)
    DrawMonth(1, currentYear, currentMonth)
    DrawMonth(2, position2Year, position2Month)
    DrawBeginTask(0, 400)
    DrawDueTask(724,400)
def DrawBeginTask(original_x, original_y):
    cfg = ConfigParser()
    cfg.read(runningDir + '/tasks/begintask.ini')
    row = 0
    fontTitle = ImageFont.truetype(runningDir + '/pic/Font.ttc', 42) 
    fontTask = ImageFont.truetype(runningDir + '/pic/Font.ttc', 35) 
    draw.text((original_x + 262, original_y + 15), u'待办事项', font = fontTitle, fill = 0)
    for f in cfg['Tasks']:
        if row > 10:
            draw.text((original_x + 12, original_y + 60 + row*50), "......", font = fontTask, fill = 0)
            break
        task = cfg.get(u'Tasks',f)
        title = task.split('|')[0]
        beginTime = task.split('|')[1]
        dueTime = task.split('|')[2]
        title = TrimString(title, 14)
        draw.text((original_x + 14, original_y + 80 + row*50), title, font = fontTask, fill = 0)
        if(beginTime != "null"):
            draw.text((original_x + 530, original_y + 80 + row*50), beginTime, font = fontTask, fill = 0)
        if(dueTime != "null"):
            draw.text((original_x + 630, original_y + 80 + row*50), dueTime, font = fontTask, fill = 0)
        row = row + 1
def DrawDueTask(original_x, original_y):
    cfg = ConfigParser()
    cfg.read(runningDir + '/tasks/duetask.ini')
    row = 0
    fontTitle = ImageFont.truetype(runningDir + '/pic/Font.ttc', 42) 
    fontTask = ImageFont.truetype(runningDir + '/pic/Font.ttc', 35) 
    draw.text((original_x + 262, original_y + 15), u'今日截止', font = fontTitle, fill = 0)
    for f in cfg['Tasks']:
        if row > 10:
            draw.text((original_x + 14, original_y + 60 + row*50), "......", font = fontTask, fill = 0)
            break
        task = cfg.get(u'Tasks',f)
        title = task.split('|')[0]
        beginTime = task.split('|')[1]
        dueTime = task.split('|')[2]
        title = TrimString(title, 14)
        draw.text((original_x + 12, original_y + 80 + row*50), title, font = fontTask, fill = 0)
        if(beginTime != "null"):
            draw.text((original_x + 530, original_y + 80 + row*50), beginTime, font = fontTask, fill = 0)
        if(dueTime != "null"):
            draw.text((original_x + 630, original_y + 80 + row*50), dueTime, font = fontTask, fill = 0)
        row = row + 1
def TrimString(srcString, width):
        TrimedString = ""
        count = 0
        for i in range(len(srcString)):
            if len(srcString[i]) == len(srcString[i].encode('utf-8')):
                count = count + 0.5
            else:
                count = count + 1
        if count <= (width):
            return srcString
        else:          
            count = 0
            for i in range(len(srcString)):
                if len(srcString[i]) == len(srcString[i].encode('utf-8')):
                    count = count + 0.5
                else:
                    count = count + 1
                if count >= width:
                    break
                TrimedString = TrimedString + srcString[i]
        return TrimedString + "..."
def DrawMonth(position,year, month):
    dateMatrix = calendar.monthcalendar(year, month)
    original_x = original_y = 0
    if position == 0:
        original_x = 0
        original_y = 0
    elif position == 1:
        original_x = 482
        original_y = 0 
    elif position == 2:           
        original_x = 965
        original_y = 0
    fontTitle = ImageFont.truetype(runningDir + '/pic/Font.ttc', 38) 
    draw.text((original_x + 130, original_y), str(year)+u'年'+str(month)+u'月', font = fontTitle, fill = 0) 
    weekList = [u'一',u'二',u'三',u'四',u'五',u'六',u'日']

    for i in range(0,7):
        draw.text((original_x + 2 + i*65, original_y + 50), weekList[i], font = fontTitle, fill = 0) 
    for row in range(len(dateMatrix)):
        for col in range(len(dateMatrix[row])):
            DrawDate(dateMatrix, row, col,original_x,original_y,year,month)        

def DrawDate(dateMatrix, row, col,original_x,original_y,year,month):
    fontDate = ImageFont.truetype(runningDir + '/pic/Font.ttc', 32) 
    fontFestival = ImageFont.truetype(runningDir + '/pic/Font.ttc', 30) 
    today = datetime.date.today()
    currentDay = 0
    monthValue = str(month)
    dayValue = str(dateMatrix[row][col])
    if month < 10:
        monthValue = '0' + str(month)
    if dateMatrix[row][col] < 10:
        dayValue = '0' + str(dateMatrix[row][col])
    keyValue = str(year) + monthValue + dayValue
    if today.strftime('%Y%m%d') == keyValue :
        currentDay = 1
        draw.rectangle((original_x + 6 + col*65, original_y + 108 + row*58, original_x  + col*68 + 40, original_y + 145 + row*58), fill = 0)
    else:
        currentDay = 0

    if  dateMatrix[row][col] == 0:
        return
    if dateMatrix[row][col] < 10:
        draw.text((original_x + 16 + col*65, original_y + 110 + row*58), str(dateMatrix[row][col]), font = fontDate, fill = currentDay) 
    else:    
        draw.text((original_x + 6 + col*65, original_y + 110 + row*58), str(dateMatrix[row][col]), font = fontDate, fill = currentDay)   
    #绘制节日名称
    if (keyValue in festivalsDays.keys()):
        draw.text((original_x + 42 + col*65, original_y + 96 + row*58), festivalsDays[keyValue][0], font = fontFestival, fill = 0)  
        draw.text((original_x + 42 + col*65, original_y + 130 + row*58), festivalsDays[keyValue][1], font = fontFestival, fill = 0)  
    #绘制放假标志
    if (keyValue in holiDays.keys()):
        draw.rectangle((original_x + 7 + col*65, original_y + 108 + row*58, original_x  + col*65 + 43, original_y + 144 + row*58), outline = 0)
    #绘制上班标志
    if (keyValue in workDays.keys()):
        draw.arc((original_x + 5 + col*65, original_y + 109 + row*58, original_x  + col*65 + 44, original_y + 145 + row*58), 0, 360, fill = 0)

def SetDayStatus(festivalsDays,holidays, workDays, year):
    cfg = ConfigParser()
    cfg.read(runningDir + '/days/'+year+'.ini')
    for f in cfg['节日日期']:
        dates = cfg.get(u'节日日期',f)
        festivalsDays[year+cfg.get(u'节日日期',f)] = f
    for f in cfg['放假日期']:
        dates = cfg.get(u'放假日期',f)
        if '-' in dates:
            start = int(dates.split('-')[0]) + int(year)*10000
            end = int(dates.split('-')[1])  + int(year)*10000
            for i in rrule(DAILY, dtstart=parse(str(start)), until=parse(str(end))):
                holidays[i.date().strftime('%Y%m%d')] = f
        else:
            holidays[year+cfg.get(u'放假日期',f)] = f
    for f in cfg['调休上班日期']:
        dates = cfg.get(u'调休上班日期',f)
        if dates != '':
            dateList = dates.split(',')
            for d in dateList:
                workDays[year + d] = f
def TaskFileUpdated(LastUpdatedTime):
    BeginCfg = ConfigParser()
    BeginCfg.read(runningDir + '/tasks/begintask.ini')
    if(not BeginCfg.has_option('Info','Last update time')):
        return 0

    DueCfg = ConfigParser()
    DueCfg.read(runningDir + '/tasks/duetask.ini')
    if(not DueCfg.has_option('Info','Last update time')):
        return 0

    BeginCfgUpdateTime = BeginCfg.get('Info','Last update time')
    DueCfgUpdateTime = DueCfg.get('Info','Last update time')

    if(LastUpdatedTime[0] != BeginCfgUpdateTime or LastUpdatedTime[1] != DueCfgUpdateTime):
        LastUpdatedTime[0] = BeginCfg.get('Info','Last update time') 
        LastUpdatedTime[1] = DueCfg.get('Info','Last update time')
        return 1
    else:
        return 0

try:
    logging.info("The daemon starts...")
    LastUpdatedTime = ['','']
    while 1:
        if(TaskFileUpdated(LastUpdatedTime)):
            logging.info("Start to update...")
            Himage = Image.new('1', (1448, 1072), 255)  # 255: clear the frame
            draw = ImageDraw.Draw(Himage)
            DrawScreen(draw)
            Himage.save(runningDir + '/pic/epd.bmp', 'bmp')
            #epdLib = cdll.LoadLibrary("./IT8951/epd.so")
            #epdLib.epd_6inch_init() 
            #epdLib.Display_epd_bmp()
            #epdLib.edp_6inch_deinit()
            logging.info("Finish...")
        time.sleep(1)
except IOError as e:
    logging.info(e)
    
except KeyboardInterrupt:    
    logging.info("ctrl + c:")
    exit()
