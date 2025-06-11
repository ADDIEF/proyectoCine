import { useState } from 'react';
import axios from '../utils/axios'; // Asegúrate de que este archivo esté configurado correctamente

const Register = () => {
  const [nombre, setNombre] = useState('');
  const [email, setEmail] = useState('');
  const [contraseña, setContraseña] = useState('');
  const [rol, setRol] = useState('registrado'); // Por defecto el rol es "registrado"
  const [error, setError] = useState('');
  const [successMessage, setSuccessMessage] = useState('');

  const handleRegister = async (e) => {
    e.preventDefault();
    try {
      const response = await axios.post('/usuarios/register', {
        nombre,
        email,
        contraseña,
        rol,
      });
      setSuccessMessage(response.data.mensaje);
      setError('');
    // eslint-disable-next-line no-unused-vars
    } catch (err) {
      setError('Hubo un problema al registrar el usuario');
      setSuccessMessage('');
    }
  };

  return (
    <div>
      <h1>Registro de Usuario</h1>
      <form onSubmit={handleRegister}>
        <div>
          <label>Nombre:</label>
          <input
            type="text"
            value={nombre}
            onChange={(e) => setNombre(e.target.value)}
            placeholder="Ingresa tu nombre"
            required
          />
        </div>
        <div>
          <label>Email:</label>
          <input
            type="email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            placeholder="Ingresa tu correo"
            required
          />
        </div>
        <div>
          <label>Contraseña:</label>
          <input
            type="password"
            value={contraseña}
            onChange={(e) => setContraseña(e.target.value)}
            placeholder="Ingresa tu contraseña"
            required
          />
        </div>
        <div>
          <label>Rol:</label>
          <select
            value={rol}
            onChange={(e) => setRol(e.target.value)}
          >
            <option value="registrado">Registrado</option>
            <option value="admin">Admin</option>
            <option value="visitante">Visitante</option>
          </select>
        </div>
        <button type="submit">Registrar</button>
      </form>

      {error && <p style={{ color: 'red' }}>{error}</p>}
      {successMessage && <p style={{ color: 'green' }}>{successMessage}</p>}
    </div>
  );
};

export default Register;
