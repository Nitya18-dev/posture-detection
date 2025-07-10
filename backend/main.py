# from fastapi import FastAPI, UploadFile, File, Form
# from fastapi.middleware.cors import CORSMiddleware
# from fastapi.responses import JSONResponse
# import cv2
# import numpy as np
# import mediapipe as mp
# from io import BytesIO
# from PIL import Image
# import tempfile

# app = FastAPI()

# # CORS middleware for frontend communication
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],  # Replace with specific domain in production
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# mp_pose = mp.solutions.pose

# def get_angle(a, b, c):
#     a = np.array(a)
#     b = np.array(b)
#     c = np.array(c)
#     radians = np.arccos(
#         np.clip(np.dot(a - b, c - b) / (np.linalg.norm(a - b) * np.linalg.norm(c - b)), -1.0, 1.0)
#     )
#     return np.degrees(radians)

# @app.post("/analyze")
# async def analyze_posture(file: UploadFile = File(...), posture_type: str = Form(...)):
#     print(f"🎥 Received video: {file.filename}, Posture: {posture_type}")
#     temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".mp4")
#     temp_file.write(await file.read())
#     temp_file.close()

#     cap = cv2.VideoCapture(temp_file.name)
#     pose = mp_pose.Pose(static_image_mode=False)

#     frame_index = 0
#     results = []
#     bad_frames = 0

#     while cap.isOpened():
#         ret, frame = cap.read()
#         if not ret:
#             break

#         frame_index += 1
#         frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
#         result = pose.process(frame_rgb)

#         issues = []
#         if result.pose_landmarks:
#             lm = result.pose_landmarks.landmark

#             def get_point(name):
#                 p = lm[mp_pose.PoseLandmark[name].value]
#                 return [p.x, p.y]

#             try:
#                 if posture_type == "squat":
#                     shoulder = get_point("LEFT_SHOULDER")
#                     hip = get_point("LEFT_HIP")
#                     knee = get_point("LEFT_KNEE")
#                     back_angle = get_angle(shoulder, hip, knee)
#                     if back_angle < 150:
#                         issues.append(f"Back angle too small: {int(back_angle)}°")

#                     knee_x = get_point("LEFT_KNEE")[0]
#                     toe_x = get_point("LEFT_FOOT_INDEX")[0]
#                     if knee_x > toe_x:
#                         issues.append("Knee over toe")

#                 elif posture_type == "sitting":
#                     shoulder = get_point("LEFT_SHOULDER")
#                     ear = get_point("LEFT_EAR")
#                     hip = get_point("LEFT_HIP")
#                     neck_angle = get_angle(ear, shoulder, hip)
#                     if neck_angle < 150:
#                         issues.append(f"Neck bend too much: {int(neck_angle)}°")
#                     if abs(shoulder[0] - hip[0]) > 0.1:
#                         issues.append("Back not straight")

#             except:
#                 issues.append("Incomplete landmarks")

#         if len(issues) > 0:
#             bad_frames += 1

#         results.append({
#             "frame": frame_index,
#             "bad_posture": len(issues) > 0,
#             "issues": issues
#         })

#     cap.release()

#     return JSONResponse(content={
#         "summary": {
#             "bad_frames": bad_frames,
#             "total_frames": frame_index
#         },
#         "details": results
#     })

# @app.post("/analyze-frame")
# async def analyze_frame(file: UploadFile = File(...), posture_type: str = Form(...)):
#     print(f"📸 Received live frame for: {posture_type}")
#     contents = await file.read()
#     img = Image.open(BytesIO(contents)).convert("RGB")
#     frame = np.array(img)

#     pose = mp_pose.Pose(static_image_mode=True)
#     result = pose.process(cv2.cvtColor(frame, cv2.COLOR_RGB2BGR))

#     issues = []
#     pose_landmarks = []

#     if result.pose_landmarks:
#         lm = result.pose_landmarks.landmark

#         for point in lm:
#             pose_landmarks.append({"x": point.x, "y": point.y})

#         def get_point(name):
#             p = lm[mp_pose.PoseLandmark[name].value]
#             return [p.x, p.y]

#         try:
#             if posture_type == "squat":
#                 shoulder = get_point("LEFT_SHOULDER")
#                 hip = get_point("LEFT_HIP")
#                 knee = get_point("LEFT_KNEE")
#                 back_angle = get_angle(shoulder, hip, knee)
#                 if back_angle < 150:
#                     issues.append(f"Back angle too small: {int(back_angle)}°")

#                 knee_x = get_point("LEFT_KNEE")[0]
#                 toe_x = get_point("LEFT_FOOT_INDEX")[0]
#                 if knee_x > toe_x:
#                     issues.append("Knee over toe")

#             elif posture_type == "sitting":
#                 shoulder = get_point("LEFT_SHOULDER")
#                 ear = get_point("LEFT_EAR")
#                 hip = get_point("LEFT_HIP")
#                 neck_angle = get_angle(ear, shoulder, hip)
#                 if neck_angle < 150:
#                     issues.append(f"Neck bend too much: {int(neck_angle)}°")
#                 if abs(shoulder[0] - hip[0]) > 0.1:
#                     issues.append("Back not straight")

#         except:
#             issues.append("Landmark error")
#     else:
#         issues.append("No landmarks detected")

#     return JSONResponse(content={
#         "bad_posture": len(issues) > 0,
#         "issues": issues,
#         "landmarks": pose_landmarks
#     })


from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import cv2
import numpy as np
import mediapipe as mp

from io import BytesIO
from PIL import Image
import tempfile

app = FastAPI()

# CORS middleware for frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Replace with specific domain in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

mp_pose = mp.solutions.pose

def get_angle(a, b, c):
    a = np.array(a)
    b = np.array(b)
    c = np.array(c)
    radians = np.arccos(
        np.clip(np.dot(a - b, c - b) / (np.linalg.norm(a - b) * np.linalg.norm(c - b)), -1.0, 1.0)
    )
    return np.degrees(radians)

@app.post("/analyze")
async def analyze_posture(file: UploadFile = File(...), posture_type: str = Form(...)):
    print(f"🎥 Received video: {file.filename}, Posture: {posture_type}")
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".mp4")
    temp_file.write(await file.read())
    temp_file.close()

    cap = cv2.VideoCapture(temp_file.name)
    pose = mp_pose.Pose(static_image_mode=False)

    frame_index = 0
    results = []
    bad_frames = 0

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        frame_index += 1
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        result = pose.process(frame_rgb)

        issues = []
        if result.pose_landmarks:
            lm = result.pose_landmarks.landmark

            def get_point(name):
                p = lm[mp_pose.PoseLandmark[name].value]
                return [p.x, p.y]

            try:
                if posture_type == "squat":
                    shoulder = get_point("LEFT_SHOULDER")
                    hip = get_point("LEFT_HIP")
                    knee = get_point("LEFT_KNEE")
                    back_angle = get_angle(shoulder, hip, knee)
                    if back_angle < 150:
                        issues.append(f"Back angle too small: {int(back_angle)}°")

                    knee_x = get_point("LEFT_KNEE")[0]
                    toe_x = get_point("LEFT_FOOT_INDEX")[0]
                    if knee_x > toe_x:
                        issues.append("Knee over toe")

                elif posture_type == "sitting":
                    shoulder = get_point("LEFT_SHOULDER")
                    ear = get_point("LEFT_EAR")
                    hip = get_point("LEFT_HIP")
                    neck_angle = get_angle(ear, shoulder, hip)
                    if neck_angle < 150:
                        issues.append(f"Neck bend too much: {int(neck_angle)}°")
                    if abs(shoulder[0] - hip[0]) > 0.1:
                        issues.append("Back not straight")

            except:
                issues.append("Incomplete landmarks")

        if len(issues) > 0:
            bad_frames += 1

        results.append({
            "frame": frame_index,
            "bad_posture": len(issues) > 0,
            "issues": issues
        })

    cap.release()

    return JSONResponse(content={
        "summary": {
            "bad_frames": bad_frames,
            "total_frames": frame_index
        },
        "details": results
    })


@app.post("/analyze-frame")
async def analyze_frame(file: UploadFile = File(...), posture_type: str = Form(...)):
    print(f"📸 Received live frame for: {posture_type}")
    contents = await file.read()
    img = Image.open(BytesIO(contents)).convert("RGB")
    frame = np.array(img)

    pose = mp_pose.Pose(static_image_mode=True)
    result = pose.process(cv2.cvtColor(frame, cv2.COLOR_RGB2BGR))

    issues = []
    pose_landmarks = []

    if result.pose_landmarks:
        lm = result.pose_landmarks.landmark

        for point in lm:
            pose_landmarks.append({"x": point.x, "y": point.y})

        def get_point(name):
            p = lm[mp_pose.PoseLandmark[name].value]
            return [p.x, p.y]

        try:
            if posture_type == "squat":
                shoulder = get_point("LEFT_SHOULDER")
                hip = get_point("LEFT_HIP")
                knee = get_point("LEFT_KNEE")
                back_angle = get_angle(shoulder, hip, knee)
                if back_angle < 150:
                    issues.append(f"Back angle too small: {int(back_angle)}°")

                knee_x = get_point("LEFT_KNEE")[0]
                toe_x = get_point("LEFT_FOOT_INDEX")[0]
                if knee_x > toe_x:
                    issues.append("Knee over toe")

            elif posture_type == "sitting":
                shoulder = get_point("LEFT_SHOULDER")
                ear = get_point("LEFT_EAR")
                hip = get_point("LEFT_HIP")
                neck_angle = get_angle(ear, shoulder, hip)
                if neck_angle < 150:
                    issues.append(f"Neck bend too much: {int(neck_angle)}°")
                if abs(shoulder[0] - hip[0]) > 0.1:
                    issues.append("Back not straight")

        except:
            issues.append("Landmark error")
    else:
        issues.append("No landmarks detected")

    return JSONResponse(content={
        "bad_posture": len(issues) > 0,
        "issues": issues,
        "landmarks": pose_landmarks
    })
