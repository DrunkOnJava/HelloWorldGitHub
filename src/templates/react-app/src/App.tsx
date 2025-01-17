import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'
import './App.css'

function App() {
  return (
    <Router>
      <div className='app'>
        <header className='app-header'>
          <h1>Welcome to Your React App</h1>
        </header>
        <main className='app-content'>
          <Routes>
            <Route path='/' element={<div>Home Page</div>} />
            {/* Add more routes here */}
          </Routes>
        </main>
        <footer className='app-footer'>
          <p>Built with React + TypeScript + Vite</p>
        </footer>
      </div>
    </Router>
  )
}

export default App
