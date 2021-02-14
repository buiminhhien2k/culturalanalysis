import pandas as pd
import numpy as np

culturalMetrics = pd.read_excel("data/6-dimensions-for-website-2015-08-16.xls")
borderingCountry = pd.read_csv("data/commonBorderIntbyCountryandBorderingCountryA.csv")

culturalMetrics.country = culturalMetrics.country.apply(lambda x: x.strip())
borderingCountry = borderingCountry.rename(columns = {"BorderingCountry":"country"}).apply(lambda x: x.str.strip())

data = pd.merge(borderingCountry,culturalMetrics, how="left",on=["country"],suffixes = ("","culturalMetrics."))


# print(data.pdi)
def removeNaN(a):

    country = a["country"]
    pdi = a["pdi"]
    if pd.isnull(pdi):
        pdi = data[data.Country == country].pdi.mean()
    idv = a["idv"]
    if pd.isnull(idv):
        idv = data[data.Country == country].idv.mean()
    mas = a["mas"]
    if pd.isnull(mas):
        mas = data[data.Country == country].mas.mean()
    uai = a["uai"]
    if pd.isnull(uai):
        uai = data[data.Country == country].uai.mean()
    ltowvs = a["ltowvs"]
    if pd.isnull(ltowvs):
        ltowvs = data[data.Country == country].ltowvs.mean()
    ivr = a["ivr"]
    if pd.isnull(ivr):
        ivr = data[data.Country == country].ivr.mean()
    
    return [a["ctr"], country]+[pdi, idv ,mas,  uai,ltowvs ,ivr]


culturalMetrics = culturalMetrics.apply(lambda row: removeNaN(row) if (
    pd.isnull(row["pdi"])
    or pd.isnull(row["idv"])
    or pd.isnull(row["mas"])
    or pd.isnull(row["uai"])
    or pd.isnull(row["ltowvs"])
    or pd.isnull(row["ivr"])
    ) else row,axis=1)
# print(culturalMetrics.shape)
# print(culturalMetrics.dropna().shape)

# def init(x= culturalMetrics):
#     return x

# if __name__ == "__main__":
#     init(culturalMetrics)