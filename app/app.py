from typing import List, Dict
import simplejson as json
from flask import Flask, request, Response, redirect
from flask import render_template
from flaskext.mysql import MySQL
from pymysql.cursors import DictCursor

app = Flask(__name__)
mysql = MySQL(cursorclass=DictCursor)

app.config['MYSQL_DATABASE_HOST'] = 'db'
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'root'
app.config['MYSQL_DATABASE_PORT'] = 3306
app.config['MYSQL_DATABASE_DB'] = 'homesData'
mysql.init_app(app)


@app.route('/', methods=['GET'])
def index():
    user = {'username': 'Homes Project'}
    cursor = mysql.get_db().cursor()
    cursor.execute('SELECT * FROM tblHomesImport')
    result = cursor.fetchall()
    return render_template('index.html', title='Home', user=user, homes=result)


@app.route('/view/<int:home_id>', methods=['GET'])
def record_view(home_id):
    cursor = mysql.get_db().cursor()
    cursor.execute('SELECT * FROM tblHomesImport WHERE id=%s', home_id)
    result = cursor.fetchall()
    return render_template('view.html', title='View Form', home=result[0])


@app.route('/edit/<int:home_id>', methods=['GET'])
def form_edit_get(home_id):
    cursor = mysql.get_db().cursor()
    cursor.execute('SELECT * FROM tblHomesImport WHERE id=%s', home_id)
    result = cursor.fetchall()
    return render_template('edit.html', title='Edit Form', home=result[0])


@app.route('/edit/<int:home_id>', methods=['POST'])
def form_update_post(home_id):
    cursor = mysql.get_db().cursor()
    inputData = (request.form.get('fldSell'), request.form.get('fldList'), request.form.get('fldLiving'),
                 request.form.get('fldRooms'), request.form.get('fldBeds'),
                 request.form.get('fldBaths'), request.form.get('fldAge'),
                 request.form.get('fldAcres'), request.form.get('fldTaxes'), home_id)
    sql_update_query = """UPDATE tblHomesImport t SET t.fldSell = %s, t.fldList = %s, t.fldLiving = %s, t.fldRooms = 
    %s, t.fldBeds = %s, t.fldBaths = %s, t.fldAge = %s, t.fldAcres = %s, t.fldTaxes = %s WHERE t.id = %s """
    cursor.execute(sql_update_query, inputData)
    mysql.get_db().commit()
    return redirect("/", code=302)

@app.route('/homes/new', methods=['GET'])
def form_insert_get():
    return render_template('new.html', title='New Home Form')


@app.route('/homes/new', methods=['POST'])
def form_insert_post():
    cursor = mysql.get_db().cursor()
    inputData = (request.form.get('fldSell'), request.form.get('fldList'), request.form.get('fldLiving'),
                 request.form.get('fldRooms'), request.form.get('fldBeds'),
                 request.form.get('fldBaths'), request.form.get('fldAge'),
                 request.form.get('fldAcres'), request.form.get('fldTaxes'))
    sql_insert_query = """INSERT INTO tblHomesImport (fldSell,fldList,fldLiving,fldRooms,fldBeds,fldBaths,fldAge,fldAcres,fldTaxes) VALUES (%s, %s,%s, %s,%s, %s,%s,%s,%s) """
    cursor.execute(sql_insert_query, inputData)
    mysql.get_db().commit()
    return redirect("/", code=302)

@app.route('/delete/<int:home_id>', methods=['POST'])
def form_delete_post(home_id):
    cursor = mysql.get_db().cursor()
    sql_delete_query = """DELETE FROM tblHomesImport WHERE id = %s """
    cursor.execute(sql_delete_query, home_id)
    mysql.get_db().commit()
    return redirect("/", code=302)


@app.route('/api/v1/homes', methods=['GET'])
def api_browse() -> str:
    cursor = mysql.get_db().cursor()
    cursor.execute('SELECT * FROM tblHomesImport')
    result = cursor.fetchall()
    json_result = json.dumps(result);
    resp = Response(json_result, status=200, mimetype='application/json')
    return resp


@app.route('/api/v1/homes/<int:home_id>', methods=['GET'])
def api_retrieve(home_id) -> str:
    cursor = mysql.get_db().cursor()
    cursor.execute('SELECT * FROM tblHomesImport WHERE id=%s', home_id)
    result = cursor.fetchall()
    json_result = json.dumps(result);
    resp = Response(json_result, status=200, mimetype='application/json')
    return resp


@app.route('/api/v1/homes/', methods=['POST'])
def api_add() -> str:
    resp = Response(status=201, mimetype='application/json')
    return resp


@app.route('/api/v1/homes/<int:home_id>', methods=['PUT'])
def api_edit(home_id) -> str:
    resp = Response(status=201, mimetype='application/json')
    return resp


@app.route('/api/homes/<int:home_id>', methods=['DELETE'])
def api_delete(home_id) -> str:
    resp = Response(status=210, mimetype='application/json')
    return resp


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
