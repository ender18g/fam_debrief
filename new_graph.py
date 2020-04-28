from reportlab.pdfgen.canvas import Canvas
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import Spacer, Paragraph, KeepTogether, SimpleDocTemplate, PageBreak, Image
from reportlab.lib.pagesizes import letter
from pyfiglet import figlet_format
from termcolor import colored
#import sheets
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import csv


# PRINT THE TITLE IN figlet_format

app_title = 'Debrief Report'
app_title = figlet_format(app_title)
app_title = colored(app_title,'blue')


print(app_title)


styles = getSampleStyleSheet()
styleN = styles['Normal']
styleH = styles['Heading3']

def createPlot(plotSel):

    comboData = []
    comboDict = {}

    for i in range(len(responseArray)):
        tempList= []
        try: tempList = responseArray[i][plotSel].split(',')
        except: continue
        #print(f"{str(i)} {str(plotSel)} {tempList}")
        for n in tempList:
            n = n.title()
            n = n.strip()
            comboData.append(n)

    comboData = list(filter(None,comboData))

    while "N/A" in comboData:
        comboData.remove("N/A")


    if comboData == []:
        print("No Data for Question " + str(plotSel))
        return 0


    comboData.sort()
    create_seaborn(comboData,plotSel)

    for n in comboData:
        comboDict[n]=comboData.count(n)

    data = list(comboDict.values())
    data = [(data),]
    names = list(comboDict.keys())

    #print(data)
    #print(names)
    highCount = max(list(comboDict.values()))


    from reportlab.graphics.shapes import Drawing
    from reportlab.graphics.charts.barcharts import VerticalBarChart
    drawing = Drawing()
    bc = VerticalBarChart()
    #bc.x = 50
    #bc.y = 50
    bc.height = 200
    bc.width = 400
    bc.data = data
    #bc.strokeColor = colors.black
    bc.valueAxis.valueMin = 0
    bc.valueAxis.valueMax = highCount
    bc.valueAxis.valueStep = 1
    bc.categoryAxis.labels.boxAnchor = 'ne'
    bc.categoryAxis.labels.dx = 9
    bc.categoryAxis.labels.dy = -2
    bc.categoryAxis.labels.angle = 30
    bc.categoryAxis.categoryNames = names
    drawing.add(bc)

    return drawing


def create_seaborn (data,num):
    sns.set(font_scale=1.5)
    data = pd.DataFrame(data,columns=['Instructor'])
    data.sort_values('Instructor')
    fig = plt.figure(figsize=(15,8))
    ax = fig.add_axes([.2,.2,.7,.7])
    ax = sns.countplot(x='Instructor',data=data)
    plt.xticks(rotation=80)
    ax.set_title(questions[num],fontsize=20)
    fig.savefig(file_name + '_' + str(num)+'.png',dpi=300)
    return None


###############IMPORT THE DATA FROM CSV
# import csv
# responseArray = []
file = 'responses.csv'
#
# responseFile = open(file)
# responseReader = csv.reader(responseFile)
# responseArray = list(responseReader)
#

#####################  THE MAIN DEAL ###################
questions = []
#responseArray = sheets.main()
with open(file) as f:
    reader = csv.reader(f)
    responseArray= list(reader)


for i in responseArray[0]:
    questions.append(i)
questions = responseArray.pop(0)

for num, x in enumerate(responseArray):
    print(f"{num}        {x[0]}")

start_r = input("Which responses would you like to start with? \n")
end_r = input("Which responses would you like to end with?\n")
responseArray=responseArray[int(start_r):int(end_r)+1]

file_name = "Output_Report"

#input("What would you like to name your PDF? \n")

numResponses = len(responseArray)

print("****** You have " + str(numResponses) + " responses processing ******\n\n")

### CREATE THE STORY############################
story = []
for n, q in enumerate(questions):
    print(str(n) + ")  "+q)

print("\n\n\nWhich questions would you like plotted? (separate numbers with spaces)")
todoList = [int(n) for n in input().split()]
#todoList=[1,3,5,7]  # These are the questions that require plots
for num, n in enumerate(todoList):
    created_Plot = createPlot(n)
    if created_Plot != 0:
        #story.append(Paragraph(questions[n],styleH))
        story.append(Spacer(20,20))
        #story.append(created_Plot)
        story.append(Image(file_name+'_'+str(n)+'.png', width=8*inch,
        height=4*inch, hAlign='CENTER'))
    if num%2==1:
        story.append(PageBreak())
    elif num==len(todoList)-1:
        story.append(PageBreak())
    else:
        story.append(Spacer(20,20))



for i in range(len(responseArray)):
    story.append(Image('sabrehawk.jpeg', width=1.15*inch,
    height=1*inch, hAlign='RIGHT'))
    story.append(Paragraph('FAMILIARIZATION STAGE DEBRIEF RESPONSE #' +
    str(i+1) +" of "  + str(numResponses),styleH))
    for j in range(len(responseArray[i])):
        story.append(Paragraph(questions[j],styleH))
        story.append(Paragraph(responseArray[i][j],
         styleN))
    story.append(PageBreak())

doc = SimpleDocTemplate(file_name + '.pdf',pagesize = letter,
                        topMargin = .2*inch,bottomMargin = .2*inch)

doc.build(story)
