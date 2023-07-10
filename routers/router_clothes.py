
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import func
from sqlalchemy.orm import Session
from classes.database import get_cursor
from classes import models_orm, schemas_dto

router = APIRouter(
    prefix='/clothes',
    tags=['Clothes']
)

# Read
@router.get('')
async def get_clothe(
    cursor: Session= Depends(get_cursor), 
    limit:int=10, offset:int=0):
    all_clothe = cursor.query(models_orm.Clothes).limit(limit).offset(offset).all() # Lancement de la requête
    clothe_count= cursor.query(func.count(models_orm.Clothe.id)).scalar()
    return {
        "clothes": all_clothe,
        "limit": limit,
        "total": clothe_count,
        "skip":offset
    }


# Read by id
@router.get('/{clothe_id}', response_model=schemas_dto.Clothe_GETID_Response)
async def get_clothe(clothe_id:int, cursor:Session= Depends(get_cursor)):
    corresponding_clothe = cursor.query(models_orm.Clothe).filter(models_orm.Clothe.id == clothe_id).first()
    if(corresponding_clothe):  
        return corresponding_clothe
    else:
        raise HTTPException (
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No corresponding clothes found with id : {clothe_id}"
        )

# CREATE / POST 
@router.post('', status_code=status.HTTP_201_CREATED)
async def create_clothe(payload: schemas_dto.Clothe_POST_Body, cursor:Session= Depends(get_cursor)):
    new_clothe = models_orm.clothe(name=payload.clotheName, price=payload.clothePrice) # build the insert
    cursor.add(new_clothe) # Send the query
    cursor.commit() #Save the staged change
    cursor.refresh(new_clothe)
    return {"message" : f"New watch {new_clothe.name} added sucessfully with id: {new_clothe.id}"} 

# DELETE ? 
@router.delete('/{clothe_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_clothe(clothe_id:int, cursor:Session=Depends(get_cursor)):
    # Recherche sur le produit existe ? 
    corresponding_clothe = cursor.query(models_orm.Clothe).filter(models_orm.Clothe.id == clothe_id)
    if(corresponding_clothe.first()):
        # Continue to delete
        corresponding_clothe.delete() # supprime
        cursor.commit() # commit the stated changes (changement latent)
        return
    else: 
        raise HTTPException (
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Ne corresponding clothes with id: {clothe_id}'
        )

# Update
@router.patch('/{clothe_id}')
async def update_clothe(clothe_id: int, payload:schemas_dto.Clothe_PATCH_Body, cursor:Session=Depends(get_cursor)):
    # trouver le produit correspodant
    corresponding_clothe = cursor.query(models_orm.Clothe).filter(models_orm.Clothe.id == clothe_id)
    if(corresponding_clothe.first()):
        # mise à jour (quoi avec quelle valeur ?) Body -> DTO
        corresponding_clothe.update({'featured':payload.newFeatured})
        cursor.commit()
        return corresponding_clothe.first()
    else: 
        raise HTTPException (
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Ne corresponding clothes with id: {clothe_id}'
        )