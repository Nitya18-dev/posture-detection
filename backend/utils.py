import cv2
import mediapipe as mp
import math

mp_pose = mp.solutions.pose

def calculate_angle(a, b, c):
    angle = math.degrees(
        math.atan2(c[1] - b[1], c[0] - b[0]) -
        math.atan2(a[1] - b[1], a[0] - b[0])
    )
    return abs(angle if angle <= 180 else 360 - angle)

def analyze_posture(video_path, posture_type):
    cap = cv2.VideoCapture(video_path)
    pose = mp_pose.Pose(static_image_mode=False)
    feedback = []
    total_frames = 0
    bad_frames = 0

    while cap.isOpened():
        success, frame = cap.read()
        if not success:
            break
        total_frames += 1
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        result = pose.process(frame_rgb)

        if result.pose_landmarks:
            landmarks = result.pose_landmarks.landmark
            h, w, _ = frame.shape

            def get_point(idx):
                pt = landmarks[idx]
                return (int(pt.x * w), int(pt.y * h))

            issues = []

            if posture_type == "squat":
                hip = get_point(mp_pose.PoseLandmark.RIGHT_HIP)
                knee = get_point(mp_pose.PoseLandmark.RIGHT_KNEE)
                ankle = get_point(mp_pose.PoseLandmark.RIGHT_ANKLE)
                shoulder = get_point(mp_pose.PoseLandmark.RIGHT_SHOULDER)
                ear = get_point(mp_pose.PoseLandmark.RIGHT_EAR)

                if knee[0] > ankle[0]:
                    issues.append("Knee over toe")

                back_angle = calculate_angle(hip, shoulder, ear)
                if back_angle < 150:
                    issues.append(f"Back angle too low: {int(back_angle)}°")

            elif posture_type == "sitting":
                hip = get_point(mp_pose.PoseLandmark.RIGHT_HIP)
                shoulder = get_point(mp_pose.PoseLandmark.RIGHT_SHOULDER)
                ear = get_point(mp_pose.PoseLandmark.RIGHT_EAR)
                nose = get_point(mp_pose.PoseLandmark.NOSE)

                back_angle = calculate_angle(hip, shoulder, ear)
                neck_angle = calculate_angle(shoulder, ear, nose)

                if back_angle < 160:
                    issues.append(f"Back not straight: {int(back_angle)}°")
                if neck_angle > 30:
                    issues.append(f"Neck bend too much: {int(neck_angle)}°")

            bad = len(issues) > 0
            if bad:
                bad_frames += 1

            feedback.append({
                "frame": total_frames,
                "bad_posture": bad,
                "issues": issues
            })

    cap.release()

    return {
        "summary": {
            "total_frames": total_frames,
            "bad_frames": bad_frames
        },
        "details": feedback
    }
