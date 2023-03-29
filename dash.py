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
  def t1(self, index):
    years_list = []
    years_data = []
    for i in x:
      if i[index] not in years_list:
        years_list.append(i[index])
        years_data.append(dict({'year': i[index], 'number': 1}))
      else:
        ind = years_list.index(i[index])
        years_data[ind]['number'] += 1

    years_data_sorted = sorted(years_data, key=lambda s: s['number'])
    number = []
    years = []
    for w in years_data_sorted[-5:]:
      number.append(w['number'])
      years.append(w['year'])
    
    return number, years  
  def t2(self, index):
    amount_data = []
    for i in x:
      amount_data.append(dict({'company': i[1], 'amount': float(i[index])}))
    amound_data_sorted = sorted(amount_data, key=lambda s: s['amount'])

    companies = []
    amount = []
    for w in amound_data_sorted[-5:]:
      companies.append(w['company'])
      amount.append(w['amount'])
    return companies, amount

collect = Collect()
# data for main page
id = collect.collect(0)
companies = collect.collect(1)
city = collect.collect(2)
indust = collect.collect(5)
companies_name = collect.companies_name()
# data for dashboard


stat = Statistics()
years = stat.t1(3)
investing_amount = stat.t2(8)
#employees = stat.t2(7)
found_rounds = stat.t2(9)
industries = stat.t1(5)

for i in industries:
  print(i)

def plot_graph():
  plt.style.use('ggplot')
  fig, ax = plt.subplots()
  ax.bar(found_rounds[0], found_rounds[1])
  fig.savefig("./static/found_rounds.png")
  plt.close(fig)

plot_graph()



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
  return render_template('statistics.html', names=companies_name,  comp_name=g[1], type_name=g[2])
  
