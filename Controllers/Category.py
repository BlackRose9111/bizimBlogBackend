from fastapi import APIRouter, HTTPException
from fastapi.params import Header
from Models.DTO import CreateCategoryDTO

router = APIRouter()

@router.get("/")
async def get_all_categories():
    from Models.Models import Category
    categories = await Category.get_all()
    return {"message":"Categories found","categories":[category for category in categories]}
@router.get("/{id}")
async def get_category(id:int):
    from Models.Models import Category
    _category = Category.get(id)
    if _category == None:
        raise HTTPException(status_code=404, detail="Category not found")

    return {"message":"Category found","category":_category}

@router.post("/")
async def create_category(categorydto : CreateCategoryDTO,token : str = Header(default=None,description="Authorization token")):
    from Models.Models import Category
    from Models.DTO import DTO
    from Authorization.Authorization import Authorization
    user = Authorization.get_instance().get_user(token)
    if user == None:
        raise HTTPException(status_code=401, detail="Unauthorized")
    category = Category(name=categorydto.name)
    try:
        category.create()
    except:
        raise HTTPException(status_code=400, detail="Category could not be created")
    categorydto = DTO(id=category.id,name=category.name)
    return {"message":"Category created","category":categorydto}

@router.put("/{id}")
async def update_category(categorydto : CreateCategoryDTO,token,id):
    from Models.Models import Category
    from Models.DTO import DTO
    from Authorization.Authorization import Authorization
    user = Authorization.get_instance().get_user(token)
    if user == None:
        raise HTTPException(status_code=401, detail="Unauthorized")

    category = await Category.find_where(id=id)
    if category == None:
        raise HTTPException(status_code=404, detail="Category not found")
    category.name = categorydto.name
    try:
        category.update()
    except:
        raise HTTPException(status_code=400, detail="Category could not be updated")
    categorydto = category
    return {"message":"Category updated","category":categorydto}