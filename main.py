from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, EmailStr, validator
from typing import Optional
from datetime import date
import json
import re

app = FastAPI()

class Abonent(BaseModel):
    last_name: str
    first_name: str
    birth_date: date
    phone: str
    email: EmailStr

    @validator('last_name', 'first_name')
    def validate_name(cls, v):
        if not re.fullmatch(r'[А-ЯЁ][а-яё]+', v):
            raise ValueError('Имя и фамилия должны быть с заглавной буквы и только на кириллице')
        return v

    @validator('phone')
    def validate_phone(cls, v):
        if not re.fullmatch(r'\+7\d{10}', v):
            raise ValueError('Телефон должен быть в формате +7XXXXXXXXXX')
        return v

@app.post("/abonent")
def collect_abonent(data: Abonent):
    try:
        with open("abonent_data.json", "w", encoding="utf-8") as f:
            json.dump(data.dict(), f, ensure_ascii=False, indent=4)
        return {"message": "Данные успешно сохранены"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
