# Contenido de models.py
from pydantic import BaseModel, Field, EmailStr
from typing import Optional, List
from datetime import datetime

# Estructura base
class MedicalHistoryBase(BaseModel):
    patient_email: EmailStr = Field(..., description="Correo del paciente (para buscar su historial).")
    doctor_id: str = Field(..., description="ID del doctor que crea/edita la entrada.")
    date: datetime = Field(default_factory=datetime.now, description="Fecha de la consulta.")
    diagnosis: str = Field(..., description="Diagnóstico o motivo.")
    treatment: Optional[str] = Field(None, description="Tratamiento recetado.")
    notes: Optional[str] = Field(None, description="Notas adicionales.")

# Modelo para crear
class MedicalHistoryCreate(MedicalHistoryBase):
    pass

# Modelo para actualizar
class MedicalHistoryUpdate(BaseModel):
    diagnosis: Optional[str] = Field(None, description="Nuevo diagnóstico.")
    treatment: Optional[str] = Field(None, description="Nuevo tratamiento.")
    notes: Optional[str] = Field(None, description="Nuevas notas.")

# Modelo para devolver desde MongoDB
class MedicalHistoryInDB(MedicalHistoryBase):
    id: str = Field(..., alias="_id", description="ID único del historial.") 

    class Config:
        populate_by_name = True
        json_encoders = {
            datetime: lambda dt: dt.isoformat()
        }