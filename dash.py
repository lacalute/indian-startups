import csv
from flask import Flask, render_template, request
from scrapping import *
import matplotlib.pyplot as plt

app = Flask(__name__)

with open('startup.csv') as f:
  reader = csv.reader(f)
  x = list(reader)
  titles = x[0]
  x.pop(0)

class Collect:
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
  
class Statistics:
  def years(self):
    years_list = []
    years_data = []
    for i in x:
      if i[3] not in years_list:
        years_list.append(i[3])
        years_data.append(dict({'year': i[3], 'number': 0}))
      else:
        ind = years_list.index(i[3])
        years_data[ind]['number'] += 1

    years_data_sorted = sorted(years_data, key=lambda s: s['number'])
    number = []
    years = []
    for w in years_data_sorted[-5:]:
      number.append(w['number'])
      years.append(w['year'])
    
    return number, years      


collect = Collect()
# data for main page
id = collect.collect(0)
companies = collect.collect(1)
city = collect.collect(2)
indust = collect.collect(5)
companies_name = collect.companies_name()
# data for dashboard

def years_data():
  stat = Statistics()
  info = stat.years()
  plt.style.use('ggplot')
  fig, ax = plt.subplots()
  plt.suptitle('By year')
  plt.title('In what years were companies open')
  ax.bar(info[1], info[0])
  fig.savefig("./static/foo.png")
  plt.close(fig)
  return ""

@app.route("/", methods=['GET'])
def main():
  return render_template("pagef.html", zip=zip, id_t=id, companies_t=companies, city_t=city, indust_t=indust)


def get():
  pay = request.form.get('company')
  pay2 = request.form.get('comp-detect')
  pay3 = request.form.get('type-detect')
  return pay, pay2, pay3


@app.route("/dashboard", methods=['POST'])
def show():
  g = get()
  result_company = collect.indentify(g[0])
  if g[0] in companies_name:
    return render_template('dash.html', data=result_company)
  else:
    return "The company not in list"

@app.route('/about')
def about():
  return render_template('about.html')

@app.route('/statistics', methods=['POST', 'GET'])
def stats():
  g = get()
  return render_template('statistics.html', names=companies_name,  comp_name=g[1], type_name=g[2], img=years_data())