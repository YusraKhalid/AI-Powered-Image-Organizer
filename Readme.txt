# AI-Powered Image Organizer

## 📌 Overview
AI-Powered Image Organizer is a smart **desktop application** that helps users **automatically categorize, manage, and clean up their image collection** using **Google Gemini AI**. The application allows users to **view, keep, or delete images**, ensuring a clutter-free storage experience. Deleted images are sent to the **Recycle Bin** for safety, and users receive notifications when all images have been processed.

---

## 🎯 Features

✅ **AI-Powered Categorization** – Uses Google Gemini AI to classify images into relevant categories like "Screenshots," "People," "Documents," etc.  
✅ **Drag & Drop Support** – Easily add images for processing.  
✅ **Keep or Delete Images** – Decide what to retain or remove. Deleted images move to the **Recycle Bin**.  
✅ **Category-Based Viewing** – Navigate images by category.  
✅ **Completion Notifications** – Alerts when all images are processed, with an option to check again.  
✅ **Modern UI & Theming** – Beautiful, responsive interface with customizable styles.  
✅ **App Reset Functionality** – After viewing all images, users can restart processing.  

---

## 🛠️ Tech Stack
- **Python** – Core backend logic
- **PyQt6** – Graphical User Interface (GUI)
- **Google Gemini AI** – AI-powered image classification
- **Pillow (PIL)** – Image handling & processing
- **Send2Trash** – Moves deleted images to the Recycle Bin
- **FastAPI** – Optional backend for AI processing
- **GitHub & Git** – Version control and repository management

---

## 🚀 Installation & Setup

### **1️⃣ Clone the Repository**
```sh
git clone https://github.com/YusraKhalid/AI-Powered-Image-Organizer.git
cd AI-Powered-Image-Organizer
```

### **2️⃣ Create & Activate Virtual Environment**
```sh
# For Windows
python -m venv venv
venv\Scripts\activate

# For macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### **3️⃣ Install Dependencies**
```sh
pip install -r requirements.txt
```

### **4️⃣ Run the Application**
```sh
python app.py
```

---

## 🔄 How to Use

1️⃣ **Drag & Drop** images into the application.  
2️⃣ **Select View Mode** – Browse all images or filter by category.  
3️⃣ **Use Action Buttons** – "✅ Keep", "❌ Delete", "➡ Next".  
4️⃣ **Receive Notifications** – When all images are processed.  
5️⃣ **Restart** – If needed, reset the app to process new images.  

---

## 🎯 Future Improvements
🔹 **Cloud Storage Integration** (AWS S3, Firebase)  
🔹 **Duplicate Image Detection**  
🔹 **Enhanced AI Categorization**  
🔹 **Support for More File Types (GIFs, PDFs, etc.)**  

---

## 🤝 Contributing
Contributions are welcome! Feel free to fork the repository, open issues, and submit pull requests.

---

## 📝 License
This project is licensed under the **MIT License**.

---

## 📬 Contact
For questions or contributions, reach out via [GitHub Issues](https://github.com/YusraKhalid/AI-Powered-Image-Organizer/issues).

