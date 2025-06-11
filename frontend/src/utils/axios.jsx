// src/utils/axios.jsx
import axios from 'axios';

const axiosInstance = axios.create({
  baseURL: 'http://localhost:8000/', // Cambia a tu URL base del backend
  headers: {
    'Content-Type': 'application/json',
  },
});

export default axiosInstance;
