import Chatbot from './components/Chatbot'
import ChartPanel from './components/ChartPanel'
import './App.css'

function App() {
  return (
    <div className="app-container">
      <header className="app-header">
        <h1>📊 CSV Charts & Chat Assistant</h1>
        <p>Upload CSV files, visualize data, and chat with AI</p>
      </header>
      <div className="app-content">
        <aside className="sidebar">
          <Chatbot />
        </aside>
        <main className="main-content">
          <ChartPanel />
        </main>
      </div>
    </div>
  )
}

export default App
