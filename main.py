# Contenido de main.py
from fastapi import FastAPI, HTTPException, status
from bson.objectid import ObjectId
from pymongo.errors import PyMongoError
from typing import List

from database import medical_histories_collection
from models import MedicalHistoryCreate, MedicalHistoryUpdate, MedicalHistoryInDB, EmailStr

app = FastAPI(
    title="Microservicio de Historial Médico",
    description="API para gestionar historiales médicos.",
)

def serialize_history(history) -> MedicalHistoryInDB:
    if history:
        history['_id'] = str(history['_id'])
    return MedicalHistoryInDB(**history) if history else None


## --- Endpoints del Doctor (CRUD) ---

@app.post("/histories", response_model=MedicalHistoryInDB, status_code=status.HTTP_201_CREATED)
async def create_history(history: MedicalHistoryCreate):
    """Crea una nueva entrada en el historial médico (Doctor)."""
    if medical_histories_collection is None:
        raise HTTPException(status_code=503, detail="Base de datos no disponible.")
        
    try:
        result = medical_histories_collection.insert_one(history.model_dump(by_alias=True))
        new_history = medical_histories_collection.find_one({"_id": result.inserted_id})
        return serialize_history(new_history)
    except PyMongoError as e:
        raise HTTPException(status_code=500, detail=f"Error DB al crear: {e}")

@app.get("/histories/{history_id}", response_model=MedicalHistoryInDB)
async def read_history_by_id(history_id: str):
    """Obtiene una entrada específica del historial por su ID (Doctor)."""
    if medical_histories_collection is None:
        raise HTTPException(status_code=503, detail="Base de datos no disponible.")

    try:
        if not ObjectId.is_valid(history_id):
            raise HTTPException(status_code=400, detail="ID no válido.")
            
        history = medical_histories_collection.find_one({"_id": ObjectId(history_id)})
        
        if history is None:
            raise HTTPException(status_code=404, detail="Historial no encontrado.")
            
        return serialize_history(history)
    except PyMongoError as e:
        raise HTTPException(status_code=500, detail=f"Error DB al leer: {e}")

@app.put("/histories/{history_id}", response_model=MedicalHistoryInDB)
async def update_history(history_id: str, history_update: MedicalHistoryUpdate):
    """Actualiza una entrada del historial médico por su ID (Doctor)."""
    if medical_histories_collection is None:
        raise HTTPException(status_code=503, detail="Base de datos no disponible.")

    try:
        if not ObjectId.is_valid(history_id):
            raise HTTPException(status_code=400, detail="ID no válido.")

        update_data = history_update.model_dump(exclude_none=True)
        
        if not update_data:
            raise HTTPException(status_code=400, detail="No se proporcionaron datos para actualizar.")

        result = medical_histories_collection.update_one(
            {"_id": ObjectId(history_id)},
            {"$set": update_data}
        )

        if result.matched_count == 0:
            raise HTTPException(status_code=404, detail="Historial no encontrado.")

        updated_history = medical_histories_collection.find_one({"_id": ObjectId(history_id)})
        return serialize_history(updated_history)
    except PyMongoError as e:
        raise HTTPException(status_code=500, detail=f"Error DB al actualizar: {e}")

@app.delete("/histories/{history_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_history(history_id: str):
    """Elimina una entrada específica del historial por su ID (Doctor)."""
    if medical_histories_collection is None:
        raise HTTPException(status_code=503, detail="Base de datos no disponible.")

    try:
        if not ObjectId.is_valid(history_id):
            raise HTTPException(status_code=400, detail="ID no válido.")
            
        result = medical_histories_collection.delete_one({"_id": ObjectId(history_id)})
        
        if result.deleted_count == 0:
            raise HTTPException(status_code=404, detail="Historial no encontrado.")
            
        return
    except PyMongoError as e:
        raise HTTPException(status_code=500, detail=f"Error DB al borrar: {e}")


## --- Endpoints del Paciente (Lectura) ---

@app.get("/histories/patient/{patient_email}", response_model=List[MedicalHistoryInDB])
async def read_patient_history(patient_email: EmailStr):
    """Obtiene todo el historial médico de un paciente por su correo electrónico (Paciente)."""
    if medical_histories_collection is None:
        raise HTTPException(status_code=503, detail="Base de datos no disponible.")
        
    try:
        histories = list(medical_histories_collection.find({"patient_email": patient_email}).sort("date", -1))
        
        return [serialize_history(h) for h in histories]
    except PyMongoError as e:
        raise HTTPException(status_code=500, detail=f"Error DB al consultar historial: {e}")