# 重新统计用户分值
user_score_detail = '''
DELETE FROM tprj_user_score_detail;
INSERT INTO tprj_user_score_detail 
SELECT a.mixin_id, sum(s.value),
u.team,
'成员',
a.date 
FROM
    tprj_activity a
    LEFT JOIN tprj_user u ON a.mixin_id = u.mixin_id
    LEFT JOIN tbas_score s ON a.type = s.type 
WHERE
    cal_done IS NULL 
    AND s.title = '成员' 
GROUP BY
    a.mixin_id,
    u.team,
    u.title,
    a.date 
UNION ALL
SELECT
    a.mixin_id,
    sum( s.value ),
    u.team,
    '组长',
    a.date 
FROM
    tprj_activity a
    LEFT JOIN tprj_user u ON a.mixin_id = u.mixin_id
    LEFT JOIN tbas_score s ON a.type = s.type 
WHERE
    cal_done IS NULL 
    AND s.title = '组长' 
GROUP BY
    a.mixin_id,
    u.team,
    u.title,
    a.date
'''

user_score = '''
DELETE 
FROM
	tprj_user_score;
INSERT INTO tprj_user_score SELECT
mixin_id,
sum( score ),
team,
title 
FROM
	tprj_user_score_detail 
GROUP BY
	mixin_id,
	team,
	title

'''

team_score_detail = '''
DELETE 
FROM
	tprj_team_score_detail;
INSERT INTO tprj_team_score_detail SELECT
team,
sum( CASE WHEN title = '成员' THEN score * 0.6 WHEN title = '组长' THEN score * 0.4 END ),
date 
FROM
	tprj_user_score_detail 
GROUP BY
	team,
	date
'''

team_score = '''
DELETE 
FROM
	tprj_team_score;
INSERT INTO tprj_team_score SELECT
team,
sum( score ) 
FROM
	tprj_team_score_detail 
GROUP BY
	team
'''

team_check_count = '''
select u.team, a.date, count(u.mixin_id) checkcount 
from tprj_user u inner join tprj_activity a on u.mixin_id = a.mixin_id where type='打卡' 
GROUP BY team, a.date
'''

team_member_count = 'select team, count(1) mcount from tprj_user GROUP BY team'

clear_team_check_count = 'delete from tprj_team_check_rate'

check_rate_show ='''
SELECT 
date,
max(case when team ='1组' then rate else 0 end) as '1组',
max(case when team ='2组' then rate else 0 end) as '2组',
max(case when team ='3组' then rate else 0 end) as '3组',
max(case when team ='4组' then rate else 0 end) as '4组',
max(case when team ='5组' then rate else 0 end) as '5组'
FROM tprj_team_check_rate
GROUP BY date
'''

member_top10 = "select u.name,u.team, s.score from tprj_user_score s inner join tprj_user u on s.mixin_id=u.mixin_id where s.title ='成员' ORDER BY score DESC limit 0, 10"

leader_top = "select u.name,u.team, s.score from tprj_user_score s inner join tprj_user u on s.mixin_id=u.mixin_id where s.title ='组长' ORDER BY score DESC limit 0, 5"

score_type_temp = "max(case when type ='{atype}' then num else 0 end) as '{atype}'"

member_score = """select b.team '组', b.name '昵称', 
{0},
ifnull(b.score,0) '积分'
from (
select u.team, u.name, a.type,  a.num,us.score from tprj_user u 
left join tprj_user_score us on u.mixin_id = us.mixin_id and us.title='成员'
left join (
select mixin_id, type, count(1) as num from tprj_activity GROUP BY mixin_id, type) a on u.mixin_id=a.mixin_id 
left join tbas_score s on a.type=s.type and s.title='成员') b
group by b.team, b.name,b.score
ORDER BY b.score desc"""

leader_score = """select b.team '组', b.name '昵称', 
{0},
ifnull(b.score,0) '积分'
from (
select u.team, u.name, a.type,  a.num,us.score from (select * from tprj_user where title like '%组长') u 
left join tprj_user_score us on u.mixin_id = us.mixin_id  and us.title='组长'
left join (
select mixin_id, type, count(1) as num from tprj_activity GROUP BY mixin_id, type) a on u.mixin_id=a.mixin_id
left join tbas_score s on a.type=s.type and s.title='组长') b
group by b.team, b.name,b.score
ORDER BY b.score desc"""

check_date_temp = "max(case when date = '{date}' then count else 0 end) as '{date2}'"
check_detail = """
select u.team '组', u.name '昵称', 
{0}
from tprj_user u left join tprj_activity a on u.mixin_id = a.mixin_id and
 a.type='打卡'
group by u.mixin_id
ORDER BY u.team
"""

team_score_show = "select * from tprj_team_score ORDER BY score"