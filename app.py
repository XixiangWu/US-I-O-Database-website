from flask import Flask, render_template, request, jsonify, Markup, Response
import numpy as np
import seaborn as sns
import json
import os
import sqlite3 #Database management library we used
import jinja2
import pandas as pd

#for row in c.execute('SELECT * FROM USIODB'):
#    print row

app = Flask(__name__, static_folder='.', static_url_path='')

# Handler
@app.route("/home")
def index():
    return render_template('home.html')

@app.route("/pivot_table")
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



@app.route("/pivot_table_builder", methods = ['POST','GET'])
def pivot_table_builder():
    if request.method == 'POST':
        
        dic = request.form
        
        # Check Validation
        if len(dic)!=6:
            raise ValueError
        else:
            table_block = build_table(request.form)
            return table_block
            
    return render_template('pivot_table_builder.html')

def build_table(dic):
    colLabel = dic['colLabel']
    filterName = dic['filterName']
    filterQuery = dic['filterQuery']
    filterValue = dic['filterValue']
    aggregationOf = dic['aggregationOf']
    aggregationCol = dic['aggregationCol']
    
    conn = sqlite3.connect('USIODB.db')
    if (filterQuery == 'contains'):
        sql = "SELECT Period,{},{} FROM USIODB WHERE {} LIKE '%{}%' ".format(to_valid_query(colLabel),to_valid_query(aggregationCol),to_valid_query(filterName),filterValue.strip())
    elif (filterQuery == 'does not contatain'):
        sql = "SELECT Period,{},{} FROM USIODB WHERE {} NOT LIKE '%{}%'".format(to_valid_query(colLabel),to_valid_query(aggregationCol),to_valid_query(filterName),filterValue.strip())
    else:    
        sql = "SELECT Period,{},{} FROM USIODB WHERE {} {} {}".format(to_valid_query(colLabel),to_valid_query(aggregationCol),to_valid_query(filterName),filterQuery,filterValue)

    sql+=" GROUP BY {}".format(to_valid_query(aggregationCol))
    
    cm = sns.light_palette("green", as_cmap=True)
    
    df = (pd.read_sql_query(sql, conn) 
            .loc[:4] 
            .style 
            .background_gradient(cmap='viridis', low=.5, high=0) 
            .highlight_null('red')
            .background_gradient(cmap=cm)
    )
    conn.close()

    print(df)

    return df.render()
    

def to_valid_query(x):
    return {
        'Period' : 'Period',
        'Total Balance' : 'Total_Balance',
        'Goods Balance' : 'Goods_Balance',
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

@app.route("/interesting_sights")
def interesting_sights():
    return render_template('interesting_sights.html')
	
def table_selector():
    return false

if __name__ == "__main__":
    app.run(debug=True, host='127.0.0.1', port=8765)
