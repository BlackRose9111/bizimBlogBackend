from fastapi import APIRouter, HTTPException
from fastapi.params import Header
from starlette.requests import Request

from Models.DTO import CreateBlogDTO, EditBlogDTO
from Models.Models import User, Category

router = APIRouter()

@router.get("/")
async def get_all_blogs():
    from Models.Models import Blog
    blogs = await Blog.get_all()
    return {"message":"Blogs found","blogs":[blog for blog in blogs]}



@router.get("/{start}/{limit}")
async def get_blogs(start:int,limit:int):
    from Models.Models import Blog
    blogs = await Blog.get_all()
    end = start + limit
    if end > len(blogs):
        end = len(blogs)
    return {"message":"Blogs found","blogs":[blog for blog in blogs[start:end]]}


@router.get("/search")
async def get_from_search(search:str,start:int = None,limit:int = None):
    from Models.Models import Blog
    blogs = await Blog.search(search,start,limit)
    for blog in blogs:
        blog.category = await Category.find_where(id=blog.category)
        blog.author = await User.find_where(id=blog.author)
        blog.author.password = None
    if blogs == None:
        raise HTTPException(status_code=404, detail="Blog not found")
    return {"message":f"Blogs found","blogs":[blog for blog in blogs]}



@router.get("/{id}")
async def get_blog(id:int):
    from Models.Models import Blog
    from Models.DTO import DTO
    blog = Blog.get(id)
    if blog == None:
        raise HTTPException(status_code=404, detail="Blog not found")

    return {"message":"Blog found","blog":blog}

@router.get("/author/{id}")
async def get_blogs_by_author(id:int):
    from Models.Models import Blog
    blogs = await Blog.find_where(user_id=id)
    for blog in blogs:
        blog.category = await Category.find_where(id=blog.category_id)
        blog.user = await User.find_where(id=blog.user_id)
        blog.user.password = None
    if blogs == None:
        raise HTTPException(status_code=404, detail="Blog not found")
    return {"message":f"Blogs found","blogs":[blog for blog in blogs]}
@router.get("/category/{id}")
async def get_blogs_by_category(id:int):
    from Models.Models import Blog
    blogs = await Blog.find_where(category_id=id)
    for blog in blogs:
        blog.category = await Category.find_where(id=blog.category_id)
        blog.user = await User.find_where(id=blog.user_id)
        blog.user.password = None
    if blogs == None:
        raise HTTPException(status_code=404, detail="Blog not found")
    return {"message":f"Blogs found","blogs":[blog for blog in blogs]}

@router.post("/")
async def create_blog(blogdto : CreateBlogDTO,request : Request):
    from Models.Models import Blog
    from Authorization.Authorization import Authorization
    token = request.headers["Authorization"]
    user = Authorization.get_instance().get_user(token)
    if user == None:
        raise HTTPException(status_code=401, detail="Unauthorized")
    author = user
    author.password = None

    category = Category.get(blogdto.category)

    blog = Blog(title=blogdto.title,content=blogdto.content,author=author,category=category,description=blogdto.description)
    try:
        blog.create()
    except:
        raise HTTPException(status_code=400, detail="Blog could not be created")
    print(f"{blog.title} created")

    return {"message":"Blog created","blog":blog}

@router.put("/")
async def update_blog(request : Request,blogdto : EditBlogDTO):
    AuthorizationToken = request.headers.get("Authorization")
    from Models.Models import Blog
    from Models.DTO import DTO
    from Authorization.Authorization import Authorization
    user = Authorization.get_instance().get_user(AuthorizationToken)
    if user == None:
        raise HTTPException(status_code=401, detail="Unauthorized")

    blog = await Blog.find_where(author=user.id,id=blogdto.id)
    if blog == None:
        raise HTTPException(status_code=404, detail="Blog not found")
    blog.title = blogdto.title
    blog.content = blogdto.content
    blog.author = User.get(blogdto.author)
    blog.category = Category.get(blogdto.category)
    try:
        blog.update()
    except:
        raise HTTPException(status_code=400, detail="Blog could not be updated")
    blogdto = DTO(id=blog.id,title=blog.title,content=blog.content,author=blog.author)
    return {"message":"Blog updated","blog":blogdto}
@router.delete("/")
async def delete_blog(id : int,token):
    from Models.Models import Blog
    from Authorization.Authorization import Authorization
    user = Authorization.get_instance().get_user(token)
    if user == None:
        raise HTTPException(status_code=401, detail="Unauthorized")
    blog = await Blog.find_where(author=user.id,id=id)
    if blog == None:
        raise HTTPException(status_code=404, detail="Blog not found")
    blog.delete()
    return {"message":"Blog deleted"}


