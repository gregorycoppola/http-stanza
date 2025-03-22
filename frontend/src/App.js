// frontend/displacy-client/src/App.js
import React, { useState } from 'react';

function App() {
  const [input, setInput] = useState("The quick brown fox jumps over the lazy dog.");
  const [svg, setSvg] = useState(null);

  const handleSubmit = async () => {
    const res = await fetch("http://localhost:8000/parse", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ text: input })
    });
    const data = await res.json();
    setSvg(data.svg);
  };

  return (
    <div style={{ padding: '2rem' }}>
      <h2>Dependency Parse Viewer</h2>
      <textarea
        value={input}
        onChange={e => setInput(e.target.value)}
        rows={4}
        cols={60}
      />
      <br />
      <button onClick={handleSubmit}>Parse</button>
      <div
        style={{ marginTop: '2rem' }}
        dangerouslySetInnerHTML={{ __html: svg }}
      />
    </div>
  );
}

export default App;
