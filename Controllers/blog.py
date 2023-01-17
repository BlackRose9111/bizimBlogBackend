from fastapi import APIRouter

from Models.DTO import CreateBlogDTO

router = APIRouter()

@router.get("/{id}")
async def get_blog(id:int):
    from Models.Models import Blog
    from Models.DTO import DTO
    blog = Blog.get(id)
    if blog == None:
        return {"message":"Blog not found"}
    blogdto = DTO(id=blog.id,title=blog.title,content=blog.content,author=blog.author)
    return {"message":"Blog found","blog":blogdto}

@router.post("/")
async def create_blog(blogdto : CreateBlogDTO,token):
    from Models.Models import Blog
    from Models.DTO import DTO
    from Authorization.Authorization import Authorization
    user = Authorization.get_instance().get_user(token)
    if user == None:
        return {"message":"Unauthorized" }
    blog = Blog(title=blogdto.title,content=blogdto.content,author=blogdto.author)
    blog.create()
    blogdto = DTO(id=blog.id,title=blog.title,content=blog.content,author=blog.author)
    return {"message":"Blog created","blog":blogdto}

@router.put("/")
async def update_blog(blogdto : CreateBlogDTO,token):
    from Models.Models import Blog
    from Models.DTO import DTO
    from Authorization.Authorization import Authorization
    user = Authorization.get_instance().get_user(token)
    if user == None:
        return {"message":"Unauthorized" }

    blog = await Blog.find_where(author=user.id,id=blogdto.id)
    if blog == None:
        return {"message":"Blog not found"}
    blog.title = blogdto.title
    blog.content = blogdto.content
    blog.author = blogdto.author
    blog.update()
    blogdto = DTO(id=blog.id,title=blog.title,content=blog.content,author=blog.author)
    return {"message":"Blog updated","blog":blogdto}
@router.delete("/")
async def delete_blog(id : int,token):
    from Models.Models import Blog
    from Authorization.Authorization import Authorization
    user = Authorization.get_instance().get_user(token)
    if user == None:
        return {"message":"Unauthorized" }
    blog = await Blog.find_where(author=user.id,id=id)
    if blog == None:
        return {"message":"Blog not found"}
    blog.delete()
    return {"message":"Blog deleted"}


