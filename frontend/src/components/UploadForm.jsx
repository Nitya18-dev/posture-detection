import React, { useState } from 'react';

function UploadForm({ setFeedback }) {
  const [file, setFile] = useState(null);
  const [postureType, setPostureType] = useState('squat');

  const handleSubmit = async (e) => {
    e.preventDefault();

    if (!file) {
      alert("Please select a video file.");
      return;
    }

    try {
      const formData = new FormData();
      formData.append('file', file);
      formData.append('posture_type', postureType);

      console.log("📡 Sending request to backend...");
      const res = await fetch('http://127.0.0.1:8000/analyze', {
        method: 'POST',
        body: formData,
      });

      console.log("✅ Got response:", res.status);
      if (!res.ok) {
        const errorText = await res.text();
        throw new Error(`Server error: ${errorText}`);
      }

      const data = await res.json();
      console.log("📊 Parsed data:", data);
      setFeedback(data);
    } catch (err) {
      console.error("❌ Upload failed:", err.message);
      alert("Error uploading video or receiving response.");
    }
  };

  return (
    <form onSubmit={handleSubmit} className="upload-form">
      <label>Select Posture Type:</label>
      <select onChange={(e) => setPostureType(e.target.value)} value={postureType}>
        <option value="squat">Squat</option>
        <option value="sitting">Desk Sitting</option>
      </select>

      <input type="file" accept="video/*" onChange={(e) => setFile(e.target.files[0])} />
      <button type="submit">Analyze</button>
    </form>
  );
}

export default UploadForm;
