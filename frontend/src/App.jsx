// src/App.jsx
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import Login from './components/Login';
import UserProfile from './components/UserProfile';
import Register from './components/Register'; 

const App = () => {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Login />} /> {/* Ruta raíz */}
        <Route path="/perfil" element={<UserProfile />} />
        <Route path="/register" element={<Register />} /> {/* Ruta de registro */}
      </Routes>
    </Router>
  );
};

export default App;
