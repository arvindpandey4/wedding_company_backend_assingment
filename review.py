import requests
import uvicorn
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI()

class Student(BaseModel):
    name: str
    country: str
    id: Optional[str] = None
    
    model_config = {"extra": "ignore"}

URL = 'https://69465581ed253f51719dd78e.mockapi.io/get-students/students_data'

@app.get('/students')
def get_students():
    response = requests.get(URL)
    
    if response.status_code == 200:
        students = response.json()
        return {"students": students, "status code": response.status_code}
    else:
        raise HTTPException(status_code=500, detail="Failed to fetch student data")

@app.get('/students/ascii-check')
def get_students_with_ascii_gap(target_diff: int = 20):
    response = requests.get(URL)
    
    if response.status_code != 200:
        raise HTTPException(status_code=500, detail="Failed to fetch student data")
        
    students_data = response.json()
    matching_students = []
    
    for student in students_data:
        try:
            student_obj = Student(**student)
            name = student_obj.name
            country = student_obj.country
            
            if name and country:
                first_char_name = name[0]
                last_char_country = country[-1]
                
                diff = abs(ord(first_char_name) - ord(last_char_country))
                
                if diff == target_diff:
                    student_dict = student_obj.model_dump()
                    student_dict['ascii_diff'] = diff
                    matching_students.append(student_dict)
        except Exception:
            continue
            
    return {"matches": matching_students, "count": len(matching_students), "target_diff": target_diff}

if __name__ == '__main__':
    uvicorn.run(app, host="127.0.0.1", port=8000)
