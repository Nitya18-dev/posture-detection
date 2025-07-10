import React, { useEffect, useRef, useState } from "react";
import Webcam from "react-webcam";

const WebcamRecorder = ({ setFeedback }) => {
  const webcamRef = useRef(null);
  const canvasRef = useRef(null);
  const [postureType, setPostureType] = useState("squat");
  const [liveIssues, setLiveIssues] = useState([]);

  useEffect(() => {
    const interval = setInterval(async () => {
      if (!webcamRef.current || !canvasRef.current) return;
      const screenshot = webcamRef.current.getScreenshot();
      if (!screenshot) return;

      const blob = await (await fetch(screenshot)).blob();
      const formData = new FormData();
      formData.append("file", blob, "frame.jpg");
      formData.append("posture_type", postureType);

      try {
        const res = await fetch("https://posture-backend-70l3.onrender.com/analyze-frame", {
          method: "POST",
          body: formData,
        });

        const data = await res.json();
        setLiveIssues(data.issues);

        // Clear canvas
        const canvas = canvasRef.current;
        const ctx = canvas.getContext("2d");
        ctx.clearRect(0, 0, canvas.width, canvas.height);

        // Draw landmarks
        const landmarks = data.landmarks;
        if (landmarks) {
          ctx.strokeStyle = "cyan";
          ctx.lineWidth = 2;
          ctx.fillStyle = "red";

          // Draw dots
          for (let i = 0; i < landmarks.length; i++) {
            const x = landmarks[i].x * canvas.width;
            const y = landmarks[i].y * canvas.height;
            ctx.beginPath();
            ctx.arc(x, y, 3, 0, 2 * Math.PI);
            ctx.fill();
          }

          // Optionally draw connections (manually pick landmark pairs)
          const connect = (a, b) => {
            const p1 = landmarks[a];
            const p2 = landmarks[b];
            ctx.beginPath();
            ctx.moveTo(p1.x * canvas.width, p1.y * canvas.height);
            ctx.lineTo(p2.x * canvas.width, p2.y * canvas.height);
            ctx.stroke();
          };

          // Key landmark connections (shoulders, arms, back, legs)
          connect(11, 13); connect(13, 15); // Left arm
          connect(12, 14); connect(14, 16); // Right arm
          connect(11, 12); // shoulders
          connect(23, 24); // hips
          connect(11, 23); connect(12, 24); // back
          connect(23, 25); connect(25, 27); // left leg
          connect(24, 26); connect(26, 28); // right leg
        }

      } catch (err) {
        console.error("Live analysis failed", err);
      }
    }, 1000);

    return () => clearInterval(interval);
  }, [postureType]);

  return (
    <div>
      <h3>Live Posture Detection (with Skeleton)</h3>
      <label>Posture Type: </label>
      <select onChange={(e) => setPostureType(e.target.value)} value={postureType}>
        <option value="squat">Squat</option>
        <option value="sitting">Desk Sitting</option>
      </select>

      <div style={{ position: "relative", width: 400, height: 300 }}>
        <Webcam
          audio={false}
          ref={webcamRef}
          screenshotFormat="image/jpeg"
          width={400}
          height={300}
          mirrored
          videoConstraints={{ width: 400, height: 300 }}
        />
        <canvas
          ref={canvasRef}
          width={400}
          height={300}
          style={{
            position: "absolute",
            top: 0,
            left: 0,
          }}
        />
      </div>

      <div style={{ marginTop: "1rem" }}>
        {liveIssues.length > 0 ? (
          <div style={{ color: "orange" }}>
            <strong>⚠️ Issues:</strong>
            <ul>
              {liveIssues.map((issue, idx) => (
                <li key={idx}>{issue}</li>
              ))}
            </ul>
          </div>
        ) : (
          <p style={{ color: "lightgreen" }}>✅ Good posture detected</p>
        )}
      </div>
    </div>
  );
};

export default WebcamRecorder;
