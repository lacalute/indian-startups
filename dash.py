import csv
from flask import Flask, render_template, request

app = Flask(__name__)

with open('startup.csv') as f:
  reader = csv.reader(f)
  x = list(reader)
  titles = x[0]
  x.pop(0)


class Analysis:
  def collect(self, index):
    l = []
    for i in x:
      l.append(i[index])
    return l

  def companies_name(self):
    names = []
    for i in x:
      names.append(i[1])
    return names
  
  def indentify(self, city):
    data = {}
    for i in x:
      if i[1] == city:
        data['name'] = i[1]
        data['city'] = i[2]
        data['year'] = i[3]
        data['founders'] = i[4]
        data['industry'] = i[5]
        data['descript'] = i[6]
        data['emp'] = i[7]
        data['amount'] = i[8]
        data['rounds'] = i[9]
    return data    

analysis = Analysis()
# data for main page
id = analysis.collect(0)
companies = analysis.collect(1)
city = analysis.collect(2)
indust = analysis.collect(5)
companies_name = analysis.companies_name()
# data for dashboard



@app.route("/", methods=['GET'])
def main():
  return render_template("pagef.html", zip=zip, id_t=id, companies_t=companies, city_t=city, indust_t=indust)


def get():
  global pay
  pay = request.form['pay']
  return pay


@app.route("/dashboard", methods=['POST'])
def show():
  result_company = analysis.indentify(get())
  if get() in companies_name:
    return render_template('dash.html', data=result_company)
  else:
    return "The company not in list"

