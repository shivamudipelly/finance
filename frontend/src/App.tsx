import React from 'react'

function App() {
  return (
    <div style={{ padding: '40px', fontFamily: 'Arial, sans-serif' }}>
      <h1>🚀 Market AI Platform</h1>
      <p>Your Personal Market Intelligence System</p>
      
      <div style={{ marginTop: '40px' }}>
        <h2>✅ System Status</h2>
        <ul>
          <li><strong>Frontend:</strong> Running on port 3000</li>
          <li><strong>Backend:</strong> Running on port 8000</li>
          <li><strong>Database:</strong> PostgreSQL ready</li>
          <li><strong>Cache:</strong> Redis ready</li>
          <li><strong>AI Engine:</strong> Ollama loading model...</li>
        </ul>
      </div>

      <div style={{ marginTop: '40px' }}>
        <h2>📋 Next Steps</h2>
        <ol>
          <li>Wait 2-5 minutes for AI model to download</li>
          <li>Visit <a href="http://localhost:8000/docs" target="_blank">API Documentation</a></li>
          <li>Register a user account</li>
          <li>Start asking market questions!</li>
        </ol>
      </div>

      <div style={{ marginTop: '40px', padding: '20px', background: '#f0f0f0', borderRadius: '8px' }}>
        <h2>💡 Example Questions to Ask</h2>
        <ul>
          <li>"Analyze RELIANCE for long-term investment"</li>
          <li>"Is TCS good for swing trading this week?"</li>
          <li>"What happened in the market today?"</li>
          <li>"Compare HDFC Bank and ICICI Bank"</li>
          <li>"Find fundamentally strong companies that fell recently"</li>
        </ul>
      </div>

      <div style={{ marginTop: '40px' }}>
        <h2>🔗 Quick Links</h2>
        <ul>
          <li><a href="http://localhost:8000/docs" target="_blank">API Documentation (Swagger)</a></li>
          <li><a href="http://localhost:8000/health" target="_blank">Health Check</a></li>
        </ul>
      </div>
    </div>
  )
}

export default App
