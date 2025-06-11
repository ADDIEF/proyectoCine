// src/components/UserProfile.jsx
import { useState, useEffect } from 'react';
import axios from '../utils/axios';

const UserProfile = () => {
  const [perfil, setPerfil] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchPerfil = async () => {
      const token = localStorage.getItem('access_token');
      if (!token) {
        setError('No estás autenticado');
        setLoading(false);
        return;
      }

      try {
        const response = await axios.get('/usuarios/perfil', {
          headers: { Authorization: `Bearer ${token}` },
        });
        setPerfil(response.data);
      // eslint-disable-next-line no-unused-vars
      } catch (err) {
        setError('Error al obtener el perfil');
      } finally {
        setLoading(false);
      }
    };

    fetchPerfil();
  }, []);

  if (loading) return <p>Cargando perfil...</p>;
  if (error) return <p>{error}</p>;

  return (
    <div>
      <h1>Perfil del Usuario</h1>
      <p><strong>Nombre:</strong> {perfil.nombre}</p>
      <p><strong>Email:</strong> {perfil.email}</p>
      <p><strong>Rol:</strong> {perfil.rol}</p>
    </div>
  );
};

export default UserProfile;
