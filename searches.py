import json
import datetime
import os

#which year do you want to create a book for?
year = "2015"

gutter = 10 #margin for cutting guides
cut = 5 #length of the cutting guides
size(450 + gutter*2, 660 + gutter*2)

searches = []
dates = []
hours = []
searches_month = []

searches_txt = ''
dates_txt = ''
hours_txt = ''
txt = FormattedString()
txt += ''

hyphenation(False)

offset = 14
w = 280 #textbox width
h = 520 #textbox height
y = 70
#for left pages
x1 = width()/2 - w/2 - offset
#for right pages
x2 = width()/2 - w/2 + offset

stroke(0.8)

#print installedFonts()
#dates_font = "RobotoMono-BoldItalic"
dates_font = "Menlo-BoldItalic"
hours_font = "RobotoMono-Thin"
#searches_font = "Menlo"
searches_font = "Menlo"  # Menlo # "LucidaGrande" 
pagenum_font = "Menlo"
title_font = "Menlo-Italic"
titlePage_font = "Menlo-Italic"
summary_font = "Menlo"

margin_title_w = 100
margin_title_h = 50

#dates_size = 9
dates_size = 8
hours_size = 4.3
#searches_size = 7 
searches_size = 7 # 7  # 7.5
pagenum_size = 6
titlePage_size = 6
title_size = 9
summary_size = 7
lh = 12
hours_baseline = 0

lastDate = "0000000000"
validSearches = 0

path = "Searches"
json_files = [pos_json for pos_json in os.listdir(path) if pos_json.endswith('.json') if pos_json.startswith(year)]

print "year:", year

for i in range(12):
    searches_month.append(0)

first = 1 
for js in json_files:
    with open(os.path.join(path, js)) as data_file:
        print js
        data = json.load(data_file)
        num_searches = len(data["event"])
        
        for i in reversed(range(num_searches)):
            time = data["event"][i]["query"]["id"][0]["timestamp_usec"]
            
            search = data["event"][i]["query"]["query_text"]
            #we clean up searches for directions
            if "->" in search or "," in search:
                pass
                
            else:
                date = datetime.datetime.utcfromtimestamp(int(time)/1000000).strftime('%A, %d %b')
                #date = datetime.datetime.utcfromtimestamp(int(time)/1000000).strftime('%A, %B %-d')
                hour = datetime.datetime.utcfromtimestamp(int(time)/1000000).strftime('%H:%M')
                #print date
                validSearches += 1
                searches.append(search)
                dates.append(date)
                hours.append(hour)
        
                if date[:7] == lastDate[:7]: # same day
                    txt.append(search + '', font=searches_font, fontSize=searches_size, lineHeight=lh)
                    txt.append(' ' + hour + '   ', font=hours_font, fontSize=hours_size, lineHeight=lh, baselineShift=hours_baseline)
                    txt.baselineShift(0)
                    
                else:
                    txt.lineHeight(lh+1) # different day
                    if first:
                        txt.append(date, font=dates_font, fontSize=dates_size)
                        first = 0
                    else:
                        txt.append('\n' + '\n' + '\n' + date, font=dates_font, fontSize=dates_size)  #.upper()
                    txt.append('\n' + '\n', font=searches_font, fontSize=searches_size, lineHeight=lh-5)
                    txt.append(search + '', font=searches_font, fontSize=searches_size, lineHeight=lh)
                    txt.append(' ' + hour + '   ', font=hours_font, fontSize=hours_size, lineHeight=lh, baselineShift=hours_baseline)
                    txt.baselineShift(0)
                
                month_num = int(datetime.datetime.fromtimestamp(int(time)/1000000).strftime('%m')) - 1
                searches_month[month_num] += 1
                
                lastDate = date

# function to print the cutting guides on each page                   
def printGuides(): 
    stroke(0)
    strokeWidth(0.2)
    
    fill(None)
    line((gutter, 0), (gutter, cut))
    line((0, gutter), (cut, gutter))
    line((width()-gutter, 0), (width()-gutter, cut))
    line((width(), gutter), (width()-cut, gutter))
    line((0, height()-gutter), (cut, height()-gutter))
    line((gutter, height()), (gutter, height()-cut))
    line((width()-gutter, height()), (width()-gutter, height()-cut))
    line((width(), height()-gutter), (width()-cut, height()-gutter))

# print the title on the first page
font(title_font)
fontSize(title_size)
fill(0)
stroke(None)
textBox("Searches " + year, (width()/2+80, height()/2, 200, 10))
printGuides()

#blank page
newPage(width(), height()) 
printGuides()

overflow_txt = txt
p = 1

while overflow_txt:
    newPage(width(), height())
    
    #If the first char of the new page is a new line we remove the new line
    while str(overflow_txt[:1]) == "\n":
        overflow_txt = overflow_txt[1:]
    
    if p == 1:
        overflow_txt = textBox(overflow_txt,(x2, y, w, h-200), align="left")
        #txt = overflow_txt
        font(pagenum_font)
        fontSize(pagenum_size)
        fill(0)
        text(str(p+1), (x2 + w/2, 35))

    
    elif p % 2 == 0:
        overflow_txt = textBox(overflow_txt,(x1, y, w, h), align="left")
        font(pagenum_font)
        fontSize(pagenum_size)
        fill(0)
        text(str(p+1), (x1 + w/2, 45))
        font(titlePage_font)
        fontSize(titlePage_size)
        fill(0)
        textBox("SEARCHES", (width() - margin_title_w, height() - margin_title_h, 40, 10), align="right")
        

    else:
        overflow_txt = textBox(overflow_txt,(x2, y, w, h), align="left")
        font(pagenum_font)
        fontSize(pagenum_size)
        fill(0)
        text(str(p+1), (x2 + w/2, 45))
        font(titlePage_font)
        fontSize(titlePage_size)
        fill(0)
        textBox(year, (margin_title_w - 40, height() - margin_title_h, 40, 10), align="left")

    printGuides()
    p += 1

# a blank page before the summary
newPage(width(), height()) 
p += 1
printGuides()
newPage(width(), height())
if p%2==0:
    shift = -offset
else: shift = offset

summary_x = 140
summary_y = 400

font(summary_font)
fontSize(summary_size)
fill(0)

textBox("Year:", (summary_x+shift, summary_y+15, 200, 10))
textBox(year, (summary_x+100+shift, summary_y+15, 250, 10))

textBox("Total searches:", (summary_x+shift, summary_y, 200, 10))
textBox(str(validSearches), (summary_x+100+shift, summary_y, 250, 10))

textBox("Average per month:", (summary_x+shift, summary_y-15, 200, 10))
textBox(str(round(validSearches/12,1)), (summary_x+100+shift, summary_y-15, 250, 10))

textBox("Average per day:", (summary_x+shift, summary_y-30, 200, 10))
textBox(str(round(validSearches/365,1)), (summary_x+100+shift, summary_y-30, 250, 10))

textBox("Searches each month:", (summary_x+shift, summary_y-45, 200, 10))
for i in range(0, 12):
    month = datetime.date(1900, i+1, 1).strftime('%b')
    textBox(month + ": " + str(searches_month[i]), (summary_x+100+shift, summary_y-45-15*i, 250, 10))
    rect(summary_x+150+shift, summary_y-40-15*i, searches_month[i]/validSearches*300, 3)

stroke(0)
strokeWidth(0.2)   
line(100 + shift,100,width()-100 + shift,100)
stroke(None)
fontSize(summary_size)
lineHeight(10)
textBox("This book has been generated with DrawBot, drawbot.com\n A project by Ishac Bertran, ishback.com", (100 + shift, 50, width()-200, 40), align="center")
printGuides()

print 'pageCount', pageCount()
print searches_month
print 'validSearches', validSearches




    