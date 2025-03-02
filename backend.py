from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import google.generativeai as genai
from PIL import Image
import os
import shutil

app = FastAPI()

# 🔑 Configure Google Gemini AI API Key
genai.configure(api_key="AIzaSyDG477OzK1pn0LPou9-4eaVihRV75w_QjI")  # Replace with your actual key

CATEGORY_LIST = ["Nature", "Landscape", "People", "Animals", "Food",
                 "Buildings", "Technology", "Vehicles", "Art", "Documents"]

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Enable CORS for desktop app communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def categorize_image(image_path):
    """Uses Google Gemini AI to categorize an image"""
    try:
        model = genai.GenerativeModel("gemini-2.0-flash")
        image = Image.open(image_path)
        response = model.generate_content([
            f"Categorize this image based on {CATEGORY_LIST}. Only reply with one word from the list.", image
        ])
        category = response.text.strip().replace("\n", "")
        return category if category in CATEGORY_LIST else "Uncategorized"
    except:
        return "Uncategorized"

@app.post("/upload/")
async def upload_image(image: UploadFile = File(...)):
    """Handles image upload and categorization"""
    file_path = os.path.join(UPLOAD_FOLDER, image.filename)
    
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(image.file, buffer)

    category = categorize_image(file_path)
    return {"filename": image.filename, "category": category}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
