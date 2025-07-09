function FeedbackGrid({ feedback }) {
  return (
    <div className="feedback">
      <h3>Feedback Summary</h3>
      <p>Bad Frames: {feedback.summary.bad_frames}</p>
      <p>Total Frames: {feedback.summary.total_frames}</p>

      <h4>Frame-by-Frame Issues</h4>
      <ul>
        {feedback.details.map((f) => (
          <li key={f.frame}>
            Frame {f.frame}: {f.bad_posture ? f.issues.join(', ') : 'Good posture ✅'}
          </li>
        ))}
      </ul>
    </div>
  );
}

export default FeedbackGrid;
