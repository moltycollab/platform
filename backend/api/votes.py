from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from database.session import get_db
from schemas.base import Vote, VoteCreate
from models import Vote as VoteModel, User as UserModel


router = APIRouter(prefix="/votes", tags=["votes"])


@router.get("/", response_model=List[Vote])
def get_votes(
    skip: int = 0, 
    limit: int = 100,
    voter_id: int = None,
    recipient_id: int = None,
    vote_type: str = None,
    db: Session = Depends(get_db)
):
    """Obtener lista de votos"""
    query = db.query(VoteModel)
    
    # Filtrar por votante si se especifica
    if voter_id:
        query = query.filter(VoteModel.voter_id == voter_id)
    
    # Filtrar por destinatario si se especifica
    if recipient_id:
        query = query.filter(VoteModel.recipient_id == recipient_id)
    
    # Filtrar por tipo de voto si se especifica
    if vote_type:
        query = query.filter(VoteModel.vote_type == vote_type)
    
    votes = query.offset(skip).limit(limit).all()
    return votes


@router.get("/{vote_id}", response_model=Vote)
def get_vote(vote_id: int, db: Session = Depends(get_db)):
    """Obtener un voto por ID"""
    vote = db.query(VoteModel).filter(VoteModel.id == vote_id).first()
    if not vote:
        raise HTTPException(status_code=404, detail="Vote not found")
    return vote


@router.post("/", response_model=Vote)
def create_vote(vote: VoteCreate, db: Session = Depends(get_db)):
    """Crear un nuevo voto"""
    # Verificar que el votante exista
    voter = db.query(UserModel).filter(UserModel.id == vote.voter_id).first()
    if not voter:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Voter does not exist"
        )
    
    # Verificar que el destinatario exista
    recipient = db.query(UserModel).filter(UserModel.id == vote.recipient_id).first()
    if not recipient:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Recipient does not exist"
        )
    
    # Verificar que no sea el mismo usuario votándose a sí mismo
    if vote.voter_id == vote.recipient_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot vote for yourself"
        )
    
    # Crear el voto
    db_vote = VoteModel(**vote.dict())
    
    db.add(db_vote)
    db.commit()
    db.refresh(db_vote)
    return db_vote


@router.delete("/{vote_id}")
def delete_vote(vote_id: int, db: Session = Depends(get_db)):
    """Eliminar un voto"""
    db_vote = db.query(VoteModel).filter(VoteModel.id == vote_id).first()
    if not db_vote:
        raise HTTPException(status_code=404, detail="Vote not found")
    
    db.delete(db_vote)
    db.commit()
    return {"message": "Vote deleted successfully"}


@router.get("/user/{user_id}/received", response_model=List[Vote])
def get_votes_received(user_id: int, db: Session = Depends(get_db)):
    """Obtener votos recibidos por un usuario"""
    votes = db.query(VoteModel).filter(VoteModel.recipient_id == user_id).all()
    return votes


@router.get("/user/{user_id}/given", response_model=List[Vote])
def get_votes_given(user_id: int, db: Session = Depends(get_db)):
    """Obtener votos dados por un usuario"""
    votes = db.query(VoteModel).filter(VoteModel.voter_id == user_id).all()
    return votes


@router.get("/user/{user_id}/reputation")
def get_user_reputation(user_id: int, db: Session = Depends(get_db)):
    """Calcular reputación de un usuario basado en votos recibidos"""
    # Obtener todos los votos recibidos por el usuario
    votes_received = db.query(VoteModel).filter(VoteModel.recipient_id == user_id).all()
    
    if not votes_received:
        return {"user_id": user_id, "reputation_score": 0, "total_votes": 0}
    
    # Calcular reputación (simple suma de valores de voto)
    total_reputation = sum(vote.value for voto in votes_received)
    total_votes = len(votes_received)
    
    # Actualizar la reputación en el modelo de usuario
    user = db.query(UserModel).filter(UserModel.id == user_id).first()
    if user:
        user.reputation_score = total_reputation
        db.commit()
    
    return {
        "user_id": user_id,
        "reputation_score": total_reputation,
        "total_votes": total_votes,
        "breakdown": {
            "positive": len([v for v in votes_received if v.value > 0]),
            "negative": len([v for v in votes_received if v.value < 0])
        }
    }