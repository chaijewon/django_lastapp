from django.db import models
import cx_Oracle
# Create your models here.

def getConnection():
    try:
         conn=cx_Oracle.connect("hr/happy@localhost:1521/xe")
    except Exception as e:
         print(e)
    return conn

def recipeListData(page):
    conn=getConnection()
    cursor=conn.cursor()
    rowSize=12
    start=(rowSize*page)-(rowSize-1)
    end=rowSize*page

    sql=f"""
           SELECT no,title,poster,num
           FROM (SELECT no,title,poster,rownum as num
           FROM (SELECT /*+ INDEX_ASC(recipe recipe_no_pk) */ no,title,poster 
           FROM recipe))
           WHERE num BETWEEN {start} AND {end}
          """
    cursor.execute(sql)
    recipe_data=cursor.fetchall()
    cursor.close()
    conn.close()
    return recipe_data

def recipeTotPage():
    conn=getConnection()
    cursor=conn.cursor()
    sql="""
            SELECT CEIL(COUNT(*)/12.0) FROM recipe
         """
    cursor.execute(sql)
    total=cursor.fetchone()
    cursor.close()
    conn.close()
    return total[0]

def login(id,pwd):
    conn=getConnection()
    cursor=conn.cursor()
    sql=f"""
            SELECT COUNT(*) FROM project_member
            WHERE id='{id}'
          """
    cursor.execute(sql)
    count=cursor.fetchone()
    cursor.close()
    result=''
    if count[0]==0 :
        result='NOID'
    else :
        sql=f"""
               SELECT pwd,name FROM project_member
               WHERE id='{id}'
              """
        cursor=conn.cursor()
        cursor.execute(sql)
        db_data=cursor.fetchone()
        cursor.close()
        db_pwd=db_data[0]
        name=db_data[1]
        if db_pwd == pwd:
            result=name
        else:
            result='NOPWD'
    conn.close()
    return result
'''
RNO                  NUMBER         
POSTER      NOT NULL VARCHAR2(260)  
CHEF        NOT NULL VARCHAR2(200)  
CHEF_POSTER NOT NULL VARCHAR2(260)  
TITLE       NOT NULL VARCHAR2(2000) 
CONTENT     NOT NULL VARCHAR2(4000) 
INFO1       NOT NULL VARCHAR2(20)   
INFO2       NOT NULL VARCHAR2(20)   
INFO3       NOT NULL VARCHAR2(20)   
FOOD_MAKE   NOT NULL CLOB           
CHEF_INFO   NOT NULL VARCHAR2(1000) 
'''
def recipeDetail(rno):
    conn=getConnection()
    cursor=conn.cursor()
    sql=f"""
           SELECT poster,chef,chef_poster,title,content,info1,info2,info3,food_make,chef_info
           FROM recipe_make
           WHERE rno={rno}
          """
    cursor.execute(sql)
    rd=cursor.fetchone()
    recipe_detail=(rd[0],rd[1],rd[2],rd[3],rd[4],rd[5],rd[6],rd[7],rd[8].read(),rd[9])
    cursor.close()
    conn.close()
    return recipe_detail

def recipeInfoData(rno):
    conn=getConnection()
    cursor=conn.cursor()
    sql=f"""
           SELECT no,poster FROM recipe
           WHERE no={rno}
          """
    cursor.execute(sql)
    info_data=cursor.fetchone()
    cursor.close()
    conn.close()
    return info_data











