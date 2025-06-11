import { useState } from 'react';
import axios from '../utils/axios';
import { Link } from 'react-router-dom';

const Login = () => {
  const [email, setEmail] = useState('');
  const [contraseña, setContraseña] = useState('');
  const [error, setError] = useState('');

  const handleLogin = async (e) => {
    e.preventDefault();
    try {
      const response = await axios.post('/usuarios/login', { email, contraseña });
      localStorage.setItem('access_token', response.data.access_token);
      // Redirigir a la página de perfil o a donde necesites
      window.location.href = '/perfil';
    // eslint-disable-next-line no-unused-vars
    } catch (err) {
      setError('Credenciales inválidas');
    }
  };

  return (
    <div>
      <h1>Login</h1>
      <form onSubmit={handleLogin}>
        <input 
          type="email" 
          value={email} 
          onChange={(e) => setEmail(e.target.value)} 
          placeholder="Correo electrónico" 
        />
        <input 
          type="password" 
          value={contraseña} 
          onChange={(e) => setContraseña(e.target.value)} 
          placeholder="Contraseña" 
        />
        <button type="submit">Iniciar sesión</button>
        {error && <p>{error}</p>}
      </form>

      <Link to="/register">¿No tienes cuenta? Regístrate aquí</Link> {/* Enlace al formulario de registro */}
    </div>
  );
};

export default Login;
