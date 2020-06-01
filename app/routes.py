from flask import render_template
from app import app
import check_last_version

brand1nok = []
brand2nok = []
brand3nok = []
mixednok = []
#check_last_version.download()
#check_last_version.untar_version_file()
ref = check_last_version.checkversion_ref()
data = check_last_version.read_DB()

print(data)

for row in data :
	if row[4] == ('brand1' or 'Brand1') and row[2] == "NOK":
		brand1nok.append(row)
	elif row[4] == ('brand2' or 'Brand2') and row[2] == "NOK":
		brand2nok.append(row)
	elif row[4] == ('brand3' or 'Brand3') and row[2] == "NOK":
		brand3nok.append(row)
	elif row[2] == "NOK":
		brandmixednok.append(row)

for row in data :
	if row[4] == ('brand1' or 'Brand1'):
		brand1all.append(row)
	elif row[4] == ('brand2' or 'Brand2'):
		brand2all.append(row)
	elif row[4] == ('brand3' or 'Brand3'):
		brand3ll.append(row)
	else :
		brandmixedall.append(row)



@app.route('/')
def dynamic_pagenok():
	return render_template('index.html', brand1=brand1nok, brand2=brand2nok, brand3=brand3nok mixed=mixednok, ref=ref)