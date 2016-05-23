from flask import Flask, render_template, request, jsonify, Markup, Response
import json
import os
import sqlite3 #Database management library we used
import jinja2


#for row in c.execute('SELECT * FROM USIODB'):
#    print row

app = Flask(__name__, static_folder='.', static_url_path='')

# Handler
@app.route("/home.html")
def index():
    return render_template('home.html')

@app.route("/pivot_table.html")
def pivot_table():

    # Process the Database
    conn = sqlite3.connect('USIODB.db')
    c = conn.cursor()

    table = html_table(c)

#    for sublist in c.execute('SELECT * FROM USIODB'):
#        print sublist
    c.close()
    conn.close()

    return render_template('pivot_table.html',table = Markup(table))

def html_table(c):
    # Generates table
    table = '<table class="table table-striped table-hover">'

    header = 1

    for row in c.execute('SELECT * FROM USIODB'):

        table += '<tr>'
        if header:
            table+='<thead>'
            for data in row:
                table+='<th>{}</th>'.format(data)
            table+='</thead></tr>'
            header = 0

        else:

            for data in row:
                table+='<td>{}</td>'.format(data)
            table+='</tr>'

    table+='</table>'
    return table

@app.route("/pivot_table_builder.html", methods = ['POST','GET'])
def pivot_table_builder():
    if request.method == 'POST':
                
        # e.g. ImmutableMultiDict([('colLabel', u'Export Inc/Dec'), ('filterName', u'Service Balance'), ('aggregationOf', u'Minimum of'), ('aggregationCol', u'Service Balance'), ('filterQuery', u'<')])

        # Check Validation
        try:
            dic = request.form
            print(dic)
            
            colLabel = dic['colLabel']
            filterName = dic['filterName']
            filterQuery = dic['filterQuery']
            aggregationOf = dic['aggregationOf']
            aggregationCol = dic['aggregationCol']
            
        except KeyError:
            return '400'
            
        return dic['filterValue']
        
            
    return render_template('pivot_table_builder.html')

@app.route("/interesting_sights.html")
def interesting_sights():
    return render_template('interesting_sights.html')
	
def table_selector():
    return false

if __name__ == "__main__":
    app.run(debug=True, host='127.0.0.1', port=8765)
