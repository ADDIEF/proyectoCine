import axios from "axios";
import { useState } from "react";
import BarLoader from "react-spinners/BarLoader";
import { signupFailedToast, signupSuccessToast } from "../toasts/toast";
import { useDispatch } from "react-redux";
import { hideSignModal } from "../reducers/authSlice";

export const SignupModal = () => {
  const [loading, setLoading] = useState(false);
  const [passViewState, setPassViewState] = useState(false);
  const [signupDetails, setSignupDetails] = useState({
    firstName: "",
    lastName: "",
    phoneNumber: "",
    email: "",
    password: "",
  });
  const [errors, setErrors] = useState({});
  const dispatch = useDispatch();

  const handleSignupDetails = (e) => {
    const { name, value } = e.target;
    setSignupDetails((prev) => ({ ...prev, [name]: value }));
    setErrors((prev) => ({ ...prev, [name]: "" }));
  };

  const togglePassState = (e) => {
    e.preventDefault();
    setPassViewState((prev) => !prev);
  };

  const validateInputs = () => {
    const newErrors = {};

    if (!signupDetails.firstName.trim()) newErrors.firstName = "Nombre requerido.";
    if (!signupDetails.lastName.trim()) newErrors.lastName = "Apellido requerido.";
    if (!signupDetails.phoneNumber.trim()) {
      newErrors.phoneNumber = "Número requerido.";
    } else if (signupDetails.phoneNumber.length !== 8) {
      newErrors.phoneNumber = "Debe tener 8 dígitos.";
    }
    if (!signupDetails.email.trim()) newErrors.email = "Email requerido.";
    if (!signupDetails.password.trim()) {
      newErrors.password = "Contraseña requerida.";
    } else if (signupDetails.password.length < 8) {
      newErrors.password = "Debe tener al menos 8 caracteres.";
    }

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleDataInsert = async (e) => {
    e.preventDefault();
    if (!validateInputs()) return;

    try {
      setLoading(true);
      const res = await axios.post(`${import.meta.env.VITE_API_URL}/registration`, signupDetails);

      if (res.status === 200) {
        dispatch(hideSignModal());
        signupSuccessToast(res.data.message);
      }
    } catch (err) {
      console.error("Error during registration:", err);
      signupFailedToast(err.response?.data?.message || "Error desconocido.");
    } finally {
      setLoading(false);
      setSignupDetails({
        firstName: "",
        lastName: "",
        phoneNumber: "",
        email: "",
        password: "",
      });
    }
  };

  return (
    <div className="signup-form">
      <form onSubmit={handleDataInsert}>
        <div className="signup-form-heading">
          <h2 className="signup-form-heading-text">Crea tu cuenta</h2>
          <button type="button" className="btn-form-exit" onClick={() => dispatch(hideSignModal())}>
            <svg
              xmlns="http://www.w3.org/2000/svg"
              className="form-icon"
              viewBox="0 0 512 512"
            >
              <path
                fill="none"
                stroke="currentColor"
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth="32"
                d="M368 368L144 144M368 144L144 368"
              />
            </svg>
          </button>
        </div>

        <div className="signup-form-body">
          {/* Nombres */}
          <div className="signup-form-category-sp">
            <div className="signup-form-category">
              <label>Nombre: <span>*</span></label>
              <input
                disabled={loading}
                name="firstName"
                type="text"
                placeholder="Ingrese su nombre..."
                onChange={handleSignupDetails}
                value={signupDetails.firstName}
              />
              {errors.firstName && <small className="error-text">{errors.firstName}</small>}
            </div>

            <div className="signup-form-category">
              <label>Apellido: <span>*</span></label>
              <input
                disabled={loading}
                name="lastName"
                type="text"
                placeholder="Ingrese su apellido..."
                onChange={handleSignupDetails}
                value={signupDetails.lastName}
              />
              {errors.lastName && <small className="error-text">{errors.lastName}</small>}
            </div>
          </div>

          {/* Celular */}
          <div className="signup-form-category">
            <label>Número Celular: <span>*</span></label>
            <input
              disabled={loading}
              name="phoneNumber"
              type="number"
              placeholder="Ingrese su número..."
              onChange={handleSignupDetails}
              value={signupDetails.phoneNumber}
            />
            {errors.phoneNumber && <small className="error-text">{errors.phoneNumber}</small>}
          </div>

          {/* Email */}
          <div className="signup-form-category">
            <label>Email: <span>*</span></label>
            <input
              disabled={loading}
              name="email"
              type="email"
              placeholder="Ingrese su correo..."
              onChange={handleSignupDetails}
              value={signupDetails.email}
            />
            {errors.email && <small className="error-text">{errors.email}</small>}
          </div>

          {/* Password */}
          <div className="signup-form-category">
            <label>Contraseña (mínimo 8): <span>*</span></label>
            <div className="input-password">
              <input
                disabled={loading}
                name="password"
                type={passViewState ? "text" : "password"}
                placeholder="Ingrese su contraseña..."
                onChange={handleSignupDetails}
                value={signupDetails.password}
              />
              <button type="button" className="pass-icon-btn" onClick={togglePassState}>
                {/* Íconos SVG igual que antes */}
              </button>
            </div>
            {errors.password && <small className="error-text">{errors.password}</small>}
          </div>

          <button type="submit" className="btn-reg" disabled={loading}>
            {loading ? <BarLoader color="#e6e6e8" /> : "Ingrese"}
          </button>
        </div>
      </form>
    </div>
  );
};