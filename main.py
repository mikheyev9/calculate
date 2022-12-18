import sqlite3 as sq
import datetime as dt
date_format = '%d.%m.%Y'
class Calculator:
    def __init__(self,limit):
        self.limit = limit
        self.records = {}
    def today_limit(self):
        a = dt.date.today()
        a = a.strftime('%d.%b.%Y')
        if a in self.records.keys():
            all_cash = sum([i.amount for i in self.records[a]])
            return self.limit - all_cash
        else:
            return self.limit
    def today_limit_database(self):
        try:
            name = dt.date.today()
            name = name.strftime('%d.%b.%Y')
            with sq.connect("calc.db") as con:
                cur = con.cursor()
                cur.execute(f"SELECT amount from records_money WHERE name LIKE '{name}'")
                resault = cur.fetchall()
                all_cash = sum([i[0] for i in resault])
                return self.limit - all_cash
        except:
            return 'Sorry'


class CaloriesCalculator(Calculator):
    def __init__(self):
        super().__init__()
    
    def add_record():
    #Save food intake record.
        pass

    def get_today_stats():
    #How many calories have you eaten tooday.

        pass

    def get_calories_remained():
    #How many calories you can eat today.
        pass

    def get_week_stats():
    #Show how many calories you have got this week
    
        pass

class CashCalculator(Calculator):
    def __init__(self,limit):
       super().__init__(limit)
    
    def add_record(self,amount,comment='Null'):
        '''Save new expence record.'''
        time = dt.datetime.now()
        if self.today_limit() - amount >= 0:
            a = dt.date.today()
            a = a.strftime('%d.%b.%Y')
            comment = Record(amount,time,comment)
            if a not in self.records.keys():
                self.records.setdefault(a ,[])
                self.records.setdefault(a ,[]).append(comment)
            elif a in self.records.keys():
                self.records.setdefault(a,comment).append(comment)
        else:
            print('you cannt use tis sum of money,\
                you can use {} only today {}'.format(self.today_limit(),time.date()))
            return 'You cannt use tis sum of money, \
                you can use {} only today {}'.format(self.today_limit(),time.date())
    
    def add_record_database(self,amount):
        time = dt.datetime.now()
        if self.today_limit_database() - amount >= 0:
            name = dt.date.today()
            name_str = name.strftime('%d.%b.%Y')
            with sq.connect("calc.db") as con:
                cur = con.cursor()
                text = """INSERT INTO records_money(name,amount,date,week,year)
                        VALUES(?,?,?,?,?)"""
                text_tuple = (name_str,amount,time,name.isocalendar().week,name.isocalendar().year)
                cur.execute(text, text_tuple)
                con.commit()
        else:
            print('you cannt use this sum of money,',
                'you can use {} only today {}'.format(self.today_limit_dataase(),time.date()),sep = ' ')
            return 'You cannt use tis sum of money, \
                you can use {} only today {}'.format(self.today_limit_dataase(),time.date())
                
    def add_database(self,date,amount,comment='Null'):
        year,mounth,day = map(int,date.split('/'))
        date = dt.date(year, mounth, day)
        date_str = date.strftime('%d.%b.%Y')
        comment = Record(amount,date,comment)
        with sq.connect("calc.db") as con:
            cur = con.cursor()
            acc = """INSERT INTO records_money (name, amount,date,week,year)
            VALUES (?,?,?,?,?)"""
            acc_tuple =(date_str, comment.amount,date,comment.week,comment.year)
            con.commit()
            cur.execute(acc,acc_tuple)
        
    def add_new(self,date,amount,comment='Null'):
        year,mounth,day = map(int,date.split('/'))
        date = dt.date(year, mounth, day)
        date_str = date.strftime('%d.%b.%Y')
        work = Record(amount,date,comment)
        if date_str not in self.records.keys():
                self.records.setdefault(date_str ,[])
                self.records.setdefault(date_str,[]).append(work)
        elif date_str in self.records.keys():
            self.records.setdefault(date_str ,work).append(work)

    def get_today_stats(self):
        '''Show how much money have you spend today.'''
        return f"you spent today {self.limit - self.today_limit()} rub"
    def get_today_stats_database(self):
        return f'you spend today {self.limit - self.today_limit_database()} rub'

    def get_today_cash_remained(currency):
    #Show how much money you will be able to spent tooday.
    #currency -> usd, rub, eur
        pass
    
    def get_week_stats(self):
    #Show how much money have you spend this week.
        now_week = dt.date.today().isocalendar().week
        box = []
        for i in self.records:
            for j in self.records[i]:
                if j.week == now_week:
                    box.append(j.amount)
        return f"this week you get out {sum(box)} rub"

    def get_week_status_database(self):
        now_week = dt.date.today().isocalendar().week
        with sq.connect('calc.db') as con:
            cur = con.cursor()
            cur.execute(f'SELECT SUM(amount) FROM records_money GROUP BY week HAVING week IN({now_week})')
            res = cur.fetchone()[0]
            return  f"this week you get out {res} rub"  
class Record():
    def __init__(self,amount,date,comment):
        self.amount = amount
        self.comment = comment
        self.date = date
        self.week = self.date.isocalendar().week
        self.year = self.date.isocalendar().year
    def __repr__(self):
        return str((self.week ,self.amount, self.comment, self.date.strftime('%d.%b.%Y.#%H:%M.')))
a = CashCalculator(500)
a.add_record(200)
a.add_record(100)
#a.add_record_database(100)
print(a.get_week_status_database())
#a.add_new('2022/09/21', 300, 'comment')
#a.add_database('2022/09/21', 300, 'comment')
#print(a.records)
#print(a.today_limit())
#print(a.get_today_stats())
""" now_week = dt.date.today().isocalendar().week
box = []
for i in a.records:
    for j in a.records[i]:
        if j.week == now_week:
                box.append(j.amount) """
            
#print(a.records)
#print(a.records['14.Dec.2022'][0].year)
    #print(a.records[i][0].week)
#print(dt.date.today().isocalendar().week)

