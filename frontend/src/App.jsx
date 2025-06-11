import { BrowserRouter as Router, Routes, Route, Navigate } from "react-router-dom";
import Upload from "./pages/Upload";


function App() {

  return (
    <Router>
        <Routes>
          <Route path="/" element={<Navigate to="/upload" />} />
          <Route path="/upload" element={<Upload />} />
        </Routes>
    </Router>
  )
}

export default App
