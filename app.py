from flask import Flask, render_template, request, jsonify, Markup, Response
import json
import os
import sqlite3 #Database management library we used
import jinja2
import pandas as pd

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
    
    c.close()
    conn.close()

    return render_template('pivot_table.html',table = Markup(table))


def html_table(c):
    # Generates table
    conn = sqlite3.connect('USIODB.db')
    df = pd.read_sql_query("SELECT * FROM USIODB", conn)
    
    return df.to_html(classes="table table-striped").replace('border="1"','border="0"')






@app.route("/pivot_table_builder.html", methods = ['POST','GET'])
def pivot_table_builder():
    if request.method == 'POST':
                
        # e.g. ImmutableMultiDict([('colLabel', u'Export Inc/Dec'), ('filterName', u'Service Balance'), ('aggregationOf', u'Minimum of'), ('aggregationCol', u'Service Balance'), ('filterQuery', u'<')])
        dic = request.form

        # Check Validation
        if len(dic)!=6:
            raise ValueError
        else:
            table_block = build_table(request.form)
            return table_block.replace('border="1"','border="0"')
        
        
        # Everything seems right, start process data
        return dic['filterValue']
        
            
    return render_template('pivot_table_builder.html')

def build_table(dic):
    colLabel = dic['colLabel']
    filterName = dic['filterName']
    filterQuery = dic['filterQuery']
    filterValue = dic['filterValue']
    aggregationOf = dic['aggregationOf']
    aggregationCol = dic['aggregationCol']
    
    conn = sqlite3.connect('USIODB.db')
    
    sql = "SELECT Period,{} FROM USIODB WHERE {} {} {}".format(to_valid_query(colLabel),to_valid_query(filterName),filterQuery,filterValue)
    
    df = pd.read_sql_query(sql, conn)
    
    print(sql)
    
    conn.close()
    return df.to_html()
    

def to_valid_query(x):
    return {
        'Period' : 'Period',
        'Total Balance' : 'TotalBalance',
        'Goods Balance' : 'GoodsBalance',
        'Service Balance' : 'Services_Balance',
        'Total Exports' : 'Total_Exports',
        'Export Inc/Dec' : 'Export_Inc_Dec',
        'Goods Exports' : 'Goods_Exports',
        'Services Exports' : 'Services_Exports',
        'Total Imports' : 'Total_Imports',
        'Import Inc/Dec' : 'Import_Inc_Dec',
        'Goods Imports' : 'Goods_Imports',
        'Services Imports' : 'Services_Imports'
    }[x]

@app.route("/interesting_sights.html")
def interesting_sights():
    return render_template('interesting_sights.html')
	
def table_selector():
    return false

if __name__ == "__main__":
    app.run(debug=True, host='127.0.0.1', port=8765)
