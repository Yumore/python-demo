import pymysql.cursors
from flask import Flask, render_template, request, redirect, url_for

from database import configs, mysqli

# Connect to the database
connection = pymysql.connect(host=configs.mysqlHost, user=configs.mysqlUser, password=configs.mysqlPwd, port=configs.mysqlPort, db=configs.mysqlDb, charset=configs.mysqlCharset, cursorclass=pymysql.cursors.DictCursor)

app = Flask(__name__)


# 保持数据库连接
def connectionSql():
    connection.ping(reconnect=True)
    return connection


# 首页
@app.route('/')
def index():
    cols = ['id', 'name', 'gender', 'age', 'phone']
    tpl_html = 'home.html'
    result, reason, code = mysqli.query_all('tb_user')
    if code == -1:
        reason = f"Can\'t view index: {reason}"
    return render_template(tpl_html, items=result, cols=cols, success=reason)


# 搜索
@app.route('/search')
def search():
    cols = ['id', 'name', 'gender', 'age', 'phone']
    keyword = request.args.get('keyword').strip()
    tpl_html = 'home.html'
    result, reason, code = mysqli.query_by_args('tb_user', 'name', keyword)
    if code == -1:
        reason = f"search error: {reason}"
    return render_template(tpl_html, items=result, keyword=keyword, cols=cols, success=reason)


@app.route('/toAddPage')
def toAddPage():
    tpl_html = 'add.html'
    return render_template(tpl_html)


@app.route('/toEditPage/<int:id>')
def toEditPage(id):
    try:
        with connectionSql().cursor() as cursor:
            sql = "select * from `tb_user` where id=%s"
            cursor.execute(sql, (id))
            result = cursor.fetchone()
            cursor.close()
            return render_template("edit.html", item=result, success='')
    except Exception as e:
        cursor.close()
        return render_template("edit.html", success='Can\'t edit User: ' + str(e))


@app.route('/add', methods=['POST'])
def add():
    name = request.form['name'].strip()
    age = request.form['age'].strip()
    gender = request.form['gender'].strip()
    phone = request.form['phone'].strip()
    try:
        with connectionSql().cursor() as cursor:
            sql = "INSERT INTO `tb_user` (`name`, `age`,`gender`,`phone`) VALUES (%s, %s,%s,%s)"
            cursor.execute(sql, (name, age, gender, phone))
            cursor.close()
            return redirect(url_for("index"))
    except Exception as e:
        cursor.close()
        return render_template("add.html", success='Can\'t add User: ' + str(e))


@app.route('/edit', methods=['POST'])
def edit():
    id = request.form['id'].strip()
    name = request.form['name'].strip()
    age = request.form['age'].strip()
    phone = request.form['phone'].strip()
    gender = request.form['gender'].strip()
    try:
        with connectionSql().cursor() as cursor:
            sql = "update `tb_user` set name=%s,age=%s,gender=%s,phone=%s where id=%s"
            cursor.execute(sql, (name, age, gender, phone, id))
            cursor.close()
            return redirect(url_for("index"))
    except Exception as e:
        cursor.close()
        return render_template("edit.html", success='Can\'t edit User: ' + str(e))


@app.route('/remove/<int:id>/')
def remove(id):
    try:
        with connectionSql().cursor() as cursor:
            sql = "delete from `tb_user` where id=%s"
            cursor.execute(sql, (id))
            cursor.close()
            return redirect(url_for("home"))
    except Exception as e:
        cursor.close()
        return render_template("home.html", success='Can\'t remove User: ' + str(e))


@app.errorhandler(404)
def page_not_found(error):
    return render_template('page_not_found.html'), 404


@app.errorhandler(500)
def system_error(error):
    return render_template('500.html'), 500


if __name__ == '__main__':
    # 静态文件缓存自动刷新
    app.jinja_env.auto_reload = True
    app.run(host='127.0.0.1', port=8001, debug=True)
