import React, { useState } from 'react';
import UploadForm from './components/UploadForm';
import WebcamRecorder from './components/WebcamRecorder';
import FeedbackGrid from './components/FeedbackGrid';
import './App.css';

function App() {
  const [mode, setMode] = useState('upload');
  const [feedback, setFeedback] = useState(null);

  return (
    <div className="App dark">
      <h1>🧠 Posture Detection App</h1>

      <div className="toggle">
        <button onClick={() => setMode('upload')}>Upload Video</button>
        <button onClick={() => setMode('webcam')}>Use Webcam</button>
      </div>

      {mode === 'upload' ? (
        <UploadForm setFeedback={setFeedback} />
      ) : (
        <WebcamRecorder setFeedback={setFeedback} />
      )}

      {feedback && <FeedbackGrid feedback={feedback} />}
    </div>
  );
}

export default App;
