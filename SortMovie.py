import pandas as pd

ExpectSort = {}
Result = {}

excel = pd.read_excel("YahooMovie.xlsx")
Title = excel["Chinese Title"]
Expect = excel["Expection"]
Satisfaction = excel["Satisfaction"]
Good = excel["Good"]
Bad = excel["Bad"]
Normal = excel["Normal"]
i=0

for Titles in Title:
    total = float(Good[i])+float(Bad[i])+float(Normal[i])
    if total !=0 :
        ExpectSort[Titles] =((float(Satisfaction[i])*20*0.65) + float(Expect[i][:-1])*0.35) +(float(Good[i])-float(Bad[i]))/total
    else:
        ExpectSort[Titles] = ((float(Satisfaction[i]) * 20 * 0.65) + float(Expect[i][:-1]) * 0.35)
    i +=1

def sort_by_value(d):
    items=d.items()
    backitems=[[v[1],v[0]] for v in items]
    backitems.sort(reverse=True)
    return [backitems[i][1] for i in range(0,len(backitems))]

Sort = sort_by_value(ExpectSort)

for sort in Sort:
    Result[sort] = ExpectSort[sort]

resultItems = Result.items()
Totle = []
ResultTitle =[]

for resultitem in resultItems:
    ResultTitle.append(resultitem[0])
    Totle.append(resultitem[1])



writer = pd.ExcelWriter("Ranking result.xlsx")
df = pd.DataFrame({"Chinese Title":ResultTitle,"Totle Score":Totle})
df.to_excel(writer,index=False,sheet_name='sheet1')
writer.save()