from django.shortcuts import render,redirect
from recipe import models
# Create your views here.
# 레시피 목록
def recipe_list(request):
    try:
         page=request.GET['page']
    except Exception as e:
         page="1"
    curpage=int(page)
    recipe_data=models.recipeListData(curpage)
    totalpage=models.recipeTotPage()

    block=10
    startPage=((curpage-1)//block*block)+1
    endPage=((curpage-1)//block*block)+block
    if endPage>totalpage:
        endPage=totalpage

    rd=[]
    for recipe in recipe_data:
        r={"no":recipe[0],"title":recipe[1],"poster":recipe[2]}
        rd.append(r)
    #쿠기 읽기
    cd=[]
    recipe_cookie=request.COOKIES
    if recipe_cookie:
        for key in recipe_cookie:
            if key.startswith('recipe'):
                data=request.COOKIES.get(key)
                db_data=models.recipeInfoData(int(data))
                cookie_data={"no":db_data[0],"poster":db_data[1]}
                cd.append(cookie_data)

    return render(request,"recipe/list.html",{"rd":rd,"cd":cd,"startPage":startPage,
                    "endPage":endPage,"curpage":curpage,"totalpage":totalpage,"range":range(startPage,endPage+1)})

# 레시피 상세보기
def recipe_detail(request):
    no=request.GET['no']
    rd=models.recipeDetail(int(no))
   #poster,chef,chef_poster,title,content,info1,info2,info3,food_make,chef_info
    recipe_data={
          "poster":rd[0],
          "chef":rd[1],
          "chef_poster":rd[2],
          "title":rd[3],
          "content":rd[4],
          "info1":rd[5],
          "info2":rd[6],
          "info3":rd[7],
           "chef_info":rd[9]
        }
    fm=rd[8].split('\n')
    return render(request,'recipe/detail.html',{"rd":recipe_data,"fm":fm})


def login(request):
    id=request.POST['id']
    pwd=request.POST['pwd']
    result=models.login(id,pwd)
    if not (result=='NOID' and result=='NOPWD'):
        request.session['id']=id
        request.session['name']=result
    return render(request,'recipe/login.html',{"result":result})

def logout(request):
    request.session.clear()
    return redirect('/recipe/')

# 쿠키저장
'''
response = render()
response = redirect()
'''
def detail_before(request):
    no=request.GET['no']
    response=redirect(f"/recipe/detail/?no={no}")
    response.set_cookie(f"recipe{no}",str(no))
    return response
