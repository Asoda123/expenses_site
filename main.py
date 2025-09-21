# from http.client import responses
# from locale import currency
#
# import json
#
# # import flask
from flask import Flask
from flask import url_for, redirect
from flask import render_template, request
# import requests
# import json
from sqlalchemy import Table, Column ,create_engine , String, ForeignKey
# from typing import List, Optional
from sqlalchemy.orm import DeclarativeBase , sessionmaker, Mapped, mapped_column, relationship

app = Flask(__name__)

engine = create_engine("sqlite:///expenses.db",echo=True)
Session = sessionmaker(bind=engine)

class Base(DeclarativeBase):
    def create_db(self):
        Base.metadata.create_all(engine)
    def drop_db(self):
        Base.metadata.drop_all(engine)

class Expenses(Base):
    __tablename__ = "expenses"
    id : Mapped[int] = mapped_column(primary_key=True)
    value: Mapped[float] = mapped_column()
    currency: Mapped[str] = mapped_column(String(3))
    purpose: Mapped[str] = mapped_column(String(50))
    date : Mapped[str] = mapped_column(String(50))

class Users(Base):
    __tablename__ = 'users'
    id : Mapped[int] = mapped_column(primary_key=True)
    login : Mapped[str] = mapped_column(String(20))
    password : Mapped[str] = mapped_column(String(20))

# base = Base()
# base.create_db()


@app.route('/exp', methods=['GET','POST'])
def get_info():
    if request.method == 'GET':
        return render_template('index.html')
    else:
        value = int(request.form['value'])
        currency = request.form['currency']
        purpose = request.form['purpose']
        date = request.form['date']

        with Session() as session:
            new_expense = Expenses(value=value, currency=currency, purpose=purpose, date=date)
            session.add(new_expense)
            session.commit()

        return redirect(url_for("all_exps"))

@app.route('/all_expenses')
def all_exps():
    with Session() as view:
        data = view.query(Expenses).all()
        return render_template('all_expenses.html', data=data)

@app.route('/reg', methods=['GET','POST'])
def reg():
    if request.method == "GET":
        return render_template("reg.html")
    else:
        login = request.form['login']
        password = request.form['password']
        with Session() as sess:
            find_user = sess.query(Users).filter_by(login=login).first()
            if find_user is None:
                with Session() as sess1:
                    new_us = Users(login=login, password=password)
                    sess1.add(new_us)
                    sess1.commit()
                    return redirect(url_for('get_info'))
            else:
                return render_template('reg.html', message='This login is used.')



@app.route('/sign_in', methods=['GET','POST'])
def sign_in():
    if request.method == "GET":
        return render_template("sign_in.html")
    else:
        login = request.form['login']
        password = request.form['password']

        with Session() as sess:
            new_us = Users(login=login, password=password)
            sess.add(new_us)
            sess.commit()

        return redirect(url_for('get_info'))


if __name__ == '__main__':
    app.run(debug=True, port=8000)