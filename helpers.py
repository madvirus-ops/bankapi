from fastapi import status,HTTPException





def get_object_or_404(model,id,db):
    object = db.query(model).filter(model.id == id).first()
    if object:
        return object
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"object with id {id} is not foumd")

