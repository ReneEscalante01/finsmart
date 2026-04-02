from pydantic import BaseModel, EmailStr, field_validator

class UsuarioLogin(BaseModel):
    email: EmailStr
    contrasena: str
    
    @field_validator("contrasena")
    @classmethod
    def vacio(cls, v):
        if v is not None and v.strip() == "":
            raise ValueError("La contrasena no puede estar vacia")
        if len(v) > 72:
            raise ValueError("La contrasena no puede tener mas de 72 caracteres")
        return v
    
class LoginResponse(BaseModel):
    message: str
    access_token: str
    token_type: str