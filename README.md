# 🧠 Rule-Based Posture Detection App

A full-stack web application that detects **bad posture** using **MediaPipe + OpenCV**, powered by **FastAPI (backend)** and **React + Vite (frontend)**. Users can **upload a video** or use their **webcam** to receive real-time feedback on posture during **squats** or **desk sitting**.

---

## 📸 Demo

> 🔗 Live Frontend: [https://posture-detection-delta.vercel.app](https://posture-detection-delta.vercel.app)  
> 🔗 Live Backend (Render): [https://posture-backend-70l3.onrender.com](https://posture-backend-70l3.onrender.com)

---

## 🧩 Features

- ✅ Upload video for analysis (`.mp4`)
- ✅ Use webcam for live detection
- ✅ Detect bad posture using rule-based logic
- ✅ Supports two posture types:
  - **Squat**: flags `knee over toe` and `back angle < 150°`
  - **Desk Sitting**: flags `neck bend > 30°` and `non-straight back`
- ✅ Displays frame-by-frame feedback
- ✅ Clean UI with dark theme
- ✅ Deploy-ready on **Vercel** and **Render**

---

## 🧪 Technologies Used

### 🔹 Frontend (`frontend/`)
- React + Vite
- react-webcam
- Tailwind / CSS (your styling choice)
- Deployed on **Vercel**

### 🔹 Backend (`backend/`)
- FastAPI
- OpenCV
- MediaPipe
- Pillow, NumPy
- Deployed on **Render**

---

## 🚀 Project Structure

```
posture-detection/
├── backend/           ← FastAPI backend
│   ├── main.py
│   ├── requirements.txt
│   └── ...
├── frontend/          ← React + Vite frontend
│   ├── src/
│   ├── public/
│   └── vite.config.js
└── README.md
```

---

## ⚙️ Setup Instructions

### 🔧 Backend (FastAPI)

```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload
```

> ✅ Make sure Python 3.13 is used (Render default)

---

### 🔧 Frontend (React + Vite)

```bash
cd frontend
npm install
npm run dev
```

> 🔗 Update `UploadForm.jsx` and `WebcamRecorder.jsx` to use:
```js
fetch("https://posture-backend-70l3.onrender.com/analyze")
```

---

## 💻 How It Works

- Video or live frame is sent to the backend
- MediaPipe extracts pose landmarks
- Rule-based logic evaluates:
  - Squat posture: back angle, knee position
  - Sitting posture: neck angle, back alignment
- Sends structured feedback per frame

---

## 📦 Backend Deployment (Render)
- Runtime: Python 3.13.4
- Start Command: `uvicorn main:app --host=0.0.0.0 --port=10000`

---

## 🌐 Frontend Deployment (Vercel)
| Field           | Value              |
|----------------|---------------------|
| Build Command  | `npm run build`     |
| Install Command| `npm install`       |
| Output Dir     | `dist`              |
| Root Dir       | `frontend/`         |

---

## 👨‍💻 Author

**Nitya**  
BCA Student, Rajasthan University  
👨‍💻 Passionate about Coding, AI, and Full-Stack Projects  
📫 GitHub: [@Nitya18-dev](https://github.com/Nitya18-dev)

---

## 📄 License

This project is open-source and available under the [MIT License](LICENSE).
