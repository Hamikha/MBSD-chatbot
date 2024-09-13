from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from store_index import MBSD_rag
import uvicorn
from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()

# CORS settings
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow any domain to make requests
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files for serving CSS/JS
app.mount("/static", StaticFiles(directory="static"), name="static")

# Specify the directory for templates
templates = Jinja2Templates(directory="templates")

# Endpoint to render the index.html page
@app.get("/")
async def get_home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# Endpoint to handle the query
@app.post("/query")
async def handle_query(request: Request):
    # Extract the question from the incoming request
    req_data = await request.json()
    user_query = req_data.get('question')

    if not user_query:
        return JSONResponse(content={"answer": "Please provide a valid query."})

    # Pass the user's query to MBSD_rag function in store_index.py
    try:
        response = MBSD_rag(user_query)
        return JSONResponse(content={"answer": response})
    except Exception as e:
        return JSONResponse(content={"answer": f"An error occurred: {str(e)}"})

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
