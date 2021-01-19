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

#panel config
panel_width = 800
panel_hight = 600

zone0_x = 0
zone0_y = 10
zone1_x = panel_width/3
zone1_y = 10
zone2_x = panel_width/3*2
zone2_y = 10
zone3_x = 0
zone3_y = panel_hight/2.68 + 10
zone4_x = panel_width/2
zone4_y = panel_hight/2.68 + 10

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

#    draw.line((zone1_x, 0, zone1_x, zone3_y), fill = 0)
#    draw.line((zone2_x, 0, zone2_x, zone3_y), fill = 0)
    draw.line((0, zone3_y, panel_width, zone3_y), fill = 0)
    draw.line((zone4_x, zone4_y, zone4_x, panel_hight), fill = 0)

    DrawMonth(zone0_x, zone0_y, position0Year, position0Month)
    DrawMonth(zone1_x, zone1_y, currentYear, currentMonth)
    DrawMonth(zone2_x, zone2_y, position2Year, position2Month)
    DrawBeginTask(zone3_x, zone3_y)
    DrawDueTask(zone4_x,zone4_y)
def DrawBeginTask(original_x, original_y):
    cfg = ConfigParser()
    cfg.read(runningDir + '/tasks/task.ini')
    row = 0
    fontTitle = ImageFont.truetype(runningDir + '/pic/Font.ttc', 20) 
    fontTask = ImageFont.truetype(runningDir + '/pic/Font.ttc', 19)
    fontTime = ImageFont.truetype(runningDir + '/pic/Font.ttc', 17)  
    draw.text((original_x + 162, original_y + 10), u'待办事项', font = fontTitle, fill = 0)
    for f in cfg['BeginTasks']:
        if row > 10:
            draw.text((original_x + 12, original_y + 40 + row*28), "......", font = fontTask, fill = 0)
            break
        task = cfg.get(u'BeginTasks',f)
        title = task.split('|')[0]
        beginTime = task.split('|')[1]
        dueTime = task.split('|')[2]
        title = TrimString(title, 15)
        draw.text((original_x + 4, original_y + 48 + row*28), title, font = fontTask, fill = 0)
        if(beginTime != "null"):
            beginTime = beginTime.split(' ')[2][0:5]
            draw.text((original_x + 305, original_y + 48 + row*28), beginTime, font = fontTime, fill = 0)
        if(dueTime != "null"):
            dueTime = dueTime.split(' ')[2][0:5]
            draw.text((original_x + 355, original_y + 48 + row*28), dueTime, font = fontTime, fill = 0)
        row = row + 1
def DrawDueTask(original_x, original_y):
    cfg = ConfigParser()
    cfg.read(runningDir + '/tasks/task.ini')
    row = 0
    fontTitle = ImageFont.truetype(runningDir + '/pic/Font.ttc', 20) 
    fontTask = ImageFont.truetype(runningDir + '/pic/Font.ttc', 19) 
    fontTime = ImageFont.truetype(runningDir + '/pic/Font.ttc', 18) 
    draw.text((original_x + 162, original_y + 10), u'今日截止', font = fontTitle, fill = 0)
    for f in cfg['DueTasks']:
        if row > 10:
            draw.text((original_x + 12, original_y + 40 + row*28), "......", font = fontTask, fill = 0)
            break
        task = cfg.get(u'DueTasks',f)
        title = task.split('|')[0]
        beginTime = task.split('|')[1]
        dueTime = task.split('|')[2]
        title = TrimString(title, 15)
        draw.text((original_x + 4, original_y + 48 + row*28), title, font = fontTask, fill = 0)
        if(beginTime != "null"):
            beginTime = beginTime.split(' ')[2][0:5]
            draw.text((original_x + 305, original_y + 48 + row*28), beginTime, font = fontTime, fill = 0)
        if(dueTime != "null"):
            dueTime = dueTime.split(' ')[2][0:5]
            draw.text((original_x + 355, original_y + 48 + row*28), dueTime, font = fontTime, fill = 0)
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
def DrawMonth(original_x, original_y,year, month):
    dateMatrix = calendar.monthcalendar(year, month)
    fontTitle = ImageFont.truetype(runningDir + '/pic/Font.ttc', 18) 
    draw.text((original_x + 100, original_y), str(year)+u'年'+str(month)+u'月', font = fontTitle, fill = 0) 
    weekList = [u'一',u'二',u'三',u'四',u'五',u'六',u'日']

    for i in range(0,7):
        draw.text((original_x + 2 + i*36, original_y + 25), weekList[i], font = fontTitle, fill = 0) 
    for row in range(len(dateMatrix)):
        for col in range(len(dateMatrix[row])):
            DrawDate(dateMatrix, row, col,original_x,original_y,year,month)        

def DrawDate(dateMatrix, row, col,original_x,original_y,year,month):
    fontDate = ImageFont.truetype(runningDir + '/pic/Font.ttc', 16) 
    fontFestival = ImageFont.truetype(runningDir + '/pic/Font.ttc', 15) 
    today = datetime.date.today()
    currentDay = 0
    rowSpan = 34
    colSpan = 36
    monthValue = str(month)
    dayValue = str(dateMatrix[row][col])
    if month < 10:
        monthValue = '0' + str(month)
    if dateMatrix[row][col] < 10:
        dayValue = '0' + str(dateMatrix[row][col])
    keyValue = str(year) + monthValue + dayValue
    if today.strftime('%Y%m%d') == keyValue :
        currentDay = 1
        draw.rectangle((original_x + 0 + col*colSpan, original_y + 55 + row*rowSpan, original_x  + col*colSpan + 19, original_y + 72 + row*rowSpan), fill = 0)
    else:
        currentDay = 0
    if  dateMatrix[row][col] == 0:
        return
    if dateMatrix[row][col] < 10:
        draw.text((original_x + 5 + col*colSpan, original_y + 55 + row*rowSpan), str(dateMatrix[row][col]), font = fontDate, fill = currentDay) 
    else:    
        draw.text((original_x + 1 + col*colSpan, original_y + 55 + row*rowSpan), str(dateMatrix[row][col]), font = fontDate, fill = currentDay)   
    #绘制节日名称
    if (keyValue in festivalsDays.keys()):
        draw.text((original_x + 20 + col*colSpan, original_y + 48 + row*rowSpan), festivalsDays[keyValue][0], font = fontFestival, fill = 0)  
        draw.text((original_x + 20 + col*colSpan, original_y + 64 + row*rowSpan), festivalsDays[keyValue][1], font = fontFestival, fill = 0)  
    #绘制放假标志
    if (keyValue in holiDays.keys()):
        draw.rectangle((original_x + 0 + col*colSpan, original_y + 55 + row*rowSpan, original_x  + col*colSpan + 19, original_y + 72 + row*rowSpan), outline = 0)
    #绘制上班标志
    if (keyValue in workDays.keys()):
        draw.arc((original_x + 1 + col*colSpan, original_y + 55 + row*rowSpan, original_x  + col*colSpan + 19, original_y + 72 + row*rowSpan), 0, 360, fill = 0)

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
def TaskFileUpdated(LastSyncTime):
    Cfg = ConfigParser()
    Cfg.read(runningDir + '/tasks/task.ini')
    if(not Cfg.has_option('Info','Last sync time')):
        return 0
    CfgSyncTime = Cfg.get('Info','Last sync time')
    if(LastSyncTime[0] != CfgSyncTime):
        LastSyncTime[0] = CfgSyncTime 
        return 1
    else:
        return 0

try:
    logging.info("The daemon starts...")
    LastSyncTime = ['']
    while 1:
        if(TaskFileUpdated(LastSyncTime)):
            logging.info("Start to update...")
            Himage = Image.new('1', (800, 600), 255)  # 255: clear the frame
            draw = ImageDraw.Draw(Himage)
            DrawScreen(draw)
            Himage.save(runningDir + '/pic/epd.bmp', 'bmp')
            epdLib = cdll.LoadLibrary(runningDir + "/IT8951/epd.so")
            epdLib.epd_6inch_init() 
            epdLib.Display_epd_bmp()
            epdLib.edp_6inch_deinit()
            logging.info("Finish...")
        time.sleep(1)
except IOError as e:
    logging.info(e)
    
except KeyboardInterrupt:    
    logging.info("ctrl + c:")
    exit()
