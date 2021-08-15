import sqlite3
from . import sql
from . import crawljingdata as cj
import time
from datetime import timedelta, datetime

class DBSqlite:
    def __init__(self, db):
        super().__init__()
        self.db = db
        self._conn = None

    def __del__(self):
        if self._conn:
            self._conn.close()
        
    def _get_conn(self):
        if not self._conn:
            self._conn = sqlite3.connect(self.db)
            self._conn.row_factory = sqlite3.Row
        return self._conn
    def _close_conn(self):
        if self._conn:
            self._conn.close()
            self._conn = None

    def _query(self, sql):
        conn = self._get_conn()
        cur = conn.cursor()
        rows = []
        for row in cur.execute(sql):
            rows.append(row)
        cur.close()
        self._close_conn()
        return rows

    def de(self, sql):
        conn = self._get_conn()
        cur = conn.cursor()
        for s in sql.split(";"):
            cur.execute(s)
        conn.commit()
        cur.close()
        self._close_conn()
        return True

    def insert(self, table, rows):
        conn = self._get_conn()
        cur = conn.cursor()
        cur.executemany("insert into %s values (%s)" % (table, ("?,"*len(rows[0]))[:-1]), rows)
        conn.commit()
        cur.close()
        self._close_conn()
        return True

    def qj(self, sql):
        conn = self._get_conn()
        cur = conn.cursor()
        cur.execute(sql)
        rows = cur.fetchall()
        cur.close()
        self._close_conn()
        return rows
    
    def qv(self, sql):
        conn = self._get_conn()
        cur = conn.cursor()
        cur.execute(sql)
        rows = cur.fetchall()
        cur.close()
        self._close_conn()
        if len(rows) > 0:
            return rows[0][0]
        else:
            return None

class SaleRecord:
    def __init__(self, db):
        super().__init__()
        self.db = db
        self._users = self.db.qj("select * from tprj_user")
        self._scoring = self.init_scoring()

    def init_scoring(self):
        scoring = {}
        dbrows = self.db.qj("select * from tbas_score")
        for d in dbrows:
            scoring[d['type']] = d["value"]
        return scoring
        

    def merge_check(self, datafilename, dates):
        rows = []
        with open(datafilename, 'r', encoding='utf-8') as check_f:
            for line in check_f:
                linedata = line[:-1].split('\t')
                for i in range(len(dates)):
                    rows.append((linedata[0], dates[i], linedata[1+i]))
        result = self.record_check(rows)
        return result

    def merge_check_web(self, date):
        rows = cj.get_check_data(date, limit=100)
        newrows = []
        for r in rows:
            if 0 == self.db.qv("select count(1) from tprj_activity where std_id=%d and type='打卡' and date='%s'" % (r[0], date)):
                newrows.append(r)
        if len(newrows) > 0:
            result = self.record_check(newrows)
            return True
        else:
            print("没有发现需要新增的打卡数据")
            return False

    def record_check(self, rows):
        dbrows = []
        for row in rows:
            u = self.get_user(std_id=int(row[0]))
            if u:
                if row[2] != "×":
                    dbrows.append((u['mixin_id'], u['std_id'], row[1], "打卡", 1, row[2], None))
            else:
                print("没有找到用户：", row)
        if len(dbrows) > 0:
            self.db.insert("tprj_activity", dbrows)
        return dbrows

    def merge_activity(self, datafilename):
        rows = []
        with open(datafilename, 'r', encoding='utf-8') as check_f:
            data = {}
            for line in check_f:
                linedata = line[:-1].split('\t')
                date = linedata[0].replace("/","-")
                userinfo = linedata[1].split("/")
                team = userinfo[0]
                name, mixin_id, std_id = userinfo[1].split('-')
                atype = linedata[2]
                rows.append((mixin_id, date, atype))
                if atype == '开单':
                    # 为组长记录
                    for tl in self._get_team_leaders(team):
                        rows.append((tl['mixin_id'], date, "组员开单"))
        # 有数据，且 是增多的 插入
        if len(rows) > 0: # and len(rows) > self.db.qv("select count(1) from tprj_activity where type<>'打卡'"):
            result = self.record_activity(rows)
            return True
        else:
            print("没有发现需要新增的活动数据")
            return False

    def record_activity(self, rows):
        dbrows = []
        for row in rows:
            u = self.get_user(mixin_id=int(row[0]))
            if u:
                dbrows.append((u['mixin_id'], u['std_id'], row[1], row[2], 1, None, None))
            else:
                print("没有找到用户：", row)

        if len(dbrows) > 0:
            self.db.de("delete from  tprj_activity where type<>'打卡'")
            self.db.insert("tprj_activity", dbrows)
        return dbrows

    def _get_team_leaders(self, team):
        return self.db.qj("select * from tprj_user  where team = '{team}' and title like '%组长'".format(team= team))

    def _get_user_by_id(self, uid, idtype):
        for u in self._users:
            if u[idtype] == uid:
                return u
        return None

    def get_user(self, **kwargs):
        for k, v in kwargs.items():
            return self._get_user_by_id(v, k)
        return None

    def cal_check_rate(self):
        ## 计算打卡率
        tmcrows = self.db.qj(sql.team_member_count)
        team_member = {}
        for r in self.db.qj(sql.team_member_count):
            team_member[r['team']] = r['mcount']
        dbrows = []
        for r in self.db.qj(sql.team_check_count):
            dbrows.append((r['team'], r['date'], round((r['checkcount']/team_member[r['team']])*100)))
        if len(dbrows) > 0:
            self.db.insert("tprj_team_check_rate", dbrows)
        return dbrows

    def recal_score(self):
        """积分计算，按日期统计，之后汇总成总分"""
        self.db.de(sql.user_score_detail)
        print("成员积分明细统计完毕")

        self.db.de(sql.user_score)
        print("成员积分合计统计完毕")

        self.db.de(sql.team_score_detail)
        print("分组积分明细统计完毕")
        
        self.db.de(sql.team_score)
        print("分组积分合计统计完毕")

        self.db.de(sql.clear_team_check_count)
        self.cal_check_rate()
        print("打卡率统计完毕")

    def show_check_rate(self, rtype='txt'):
        data = self.db.qj(sql.check_rate_show)
        if rtype == 'dict':
            return self.sqlRowsToDict(data)
        result = []
        line = '\t'.join(data[0].keys()) + "\n"
        result.append(line)
        # print(line)
        for d in data:
            row = []
            for k in d.keys():
                if k != 'date':
                    row.append(str(d[k]) + "%")
                else:
                    row.append(d[k])
            line = '\t'.join(row) + "\n"
            result.append(line)
            # print(line)
        result.append('\n')
        # print("\n"*2)
        return result

    def get_score_sql(self, title):
        types = self.db.qj("select type, value from tbas_score where title='%s'" % title)
        temps = []
        for t in types:
            temps.append(sql.score_type_temp.format(atype=t['type']))
        print(temps)
        if title == '成员':
            realsql = sql.member_score
        else:
            realsql = sql.leader_score

        realsql = realsql.format(",\n".join(temps))
        # print(realsql)
        return realsql
        pass

    def sqlRowsToDict(self, data):
        rows = []
        for d in data:
            row = {}
            for k in d.keys():
                row[k] = d[k]
            rows.append(row)
        return rows

    def show_member_score(self, rtype='txt'):
        data = self.db.qj(self.get_score_sql(title='成员'))
        if rtype == 'dict':
            return self.sqlRowsToDict(data)
            
        result = []
        line = '\t'.join(data[0].keys()) + "\n"
        result.append(line)
        # print(line)
        for d in data:
            row = []
            for k in d.keys():
                v = d[k]
                if type(d[k]) != str:
                    v = str(v)
                row.append(v)
            line = '\t'.join(row) + "\n"
            result.append(line)
            # print(line)
        result.append('\n')
        return result

    def show_leader_score(self, rtype='txt'):
        data = self.db.qj(self.get_score_sql(title='组长'))
        if rtype == 'dict':
            return self.sqlRowsToDict(data)
        result = []
        line = '\t'.join(data[0].keys()) + "\n"
        result.append(line)
        # print(line)
        for d in data:
            row = []
            for k in d.keys():
                v = d[k]
                if type(d[k]) != str:
                    v = str(v)
                row.append(v)
            line = '\t'.join(row) + "\n"
            result.append(line)
            # print(line)
        result.append('\n')
        # print("\n"*2)
        return result

    def get_check_detail_sql(self):
        beginday = datetime.strptime('2021-08-01', '%Y-%m-%d')
        today = datetime.today()
        date = beginday

        temps = []
        while date <= today:
            temps.append(sql.check_date_temp.format(date=date.strftime("%Y-%m-%d"), date2=date.strftime("%m月%d日")))
            date += timedelta(1)
        realsql = sql.check_detail.format(",\n".join(temps))
        
        return realsql
        pass

    def show_check_detail(self, rtype='txt'):
        data = self.db.qj(self.get_check_detail_sql())
        if rtype == 'dict':
            return self.sqlRowsToDict(data)
        result = []
        line = '\t'.join(data[0].keys()) + "\n"
        result.append(line)
        # print(line)
        for d in data:
            row = []
            for k in d.keys():
                v = d[k]
                if type(d[k]) != str:
                    v = str(v)
                row.append(v)
            line = '\t'.join(row) + "\n"
            result.append(line)
            # print(line)
        result.append('\n')
        # print("\n"*2)
        return result
    
    def get_team_check_detail(self, team, date):
        return self.sqlRowsToDict(self.db.qj(sql.team_check_detail.format(date=date, team=team)))
    
    def get_sale_data(self):
        return self.sqlRowsToDict(self.db.qj(sql.sale_data))

def main():
    sale = SaleRecord(DBSqlite("example.db"))
    beginday = datetime.strptime('2021-08-01', '%Y-%m-%d')
    today = datetime.today()

    date = beginday
    need_cal = False
    while date <= today:
        print("获取 %s 的打卡数据" % date.strftime("%Y-%m-%d"))
        result = sale.merge_check_web(date.strftime("%Y-%m-%d"))
        need_cal = need_cal if need_cal else result
        date += timedelta(1)
    print("获取 活动数据")
    aresult = sale.merge_activity("activity.txt")
    need_cal = need_cal if need_cal else aresult
    if need_cal:
        sale.recal_score()

    # 显示数据
    print("打卡率")
    filename = "result_%s.txt" % today.strftime("%Y-%m-%d %H_%M_%S")
    with open(filename, 'w', encoding='utf-8') as r:
        r.writelines(sale.show_check_rate())
        r.writelines(sale.show_member_score())
        r.writelines(sale.show_leader_score())

def test():
    sale = SaleRecord(DBSqlite("example.db"))
    # return sale.get_score_sql("组长")
    ret = sale.show_check_detail(rtype='dict')
    print(ret)
if __name__ == "__main__":
    test()
    exit()
    main()
    
