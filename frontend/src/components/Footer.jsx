import { useEffect, useState } from "react";
import axios from "axios";
import { Link, useLocation } from "react-router-dom";
import { HashLink } from "react-router-hash-link";
import HashLoader from "react-spinners/HashLoader";
import { useDispatch } from "react-redux";
import { showLoginModal, showSignModal } from "../reducers/authSlice";

export const Footer = () => {
  const [locationData, setLocationData] = useState([]);
  const [loading, setLoading] = useState(true);
  const dispatch = useDispatch();
  let pageName;
  const location = useLocation();

  location.pathname === "/" ? (pageName = "home") : (pageName = "");

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await axios.get(
          `${import.meta.env.VITE_API_URL}/locationDetails`
        );
        setLocationData(response.data);
      } catch (err) {
        console.log(err);
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, []);

  const locations = locationData.map((location, idx) => {
    return (
      <p key={idx} className="address">
        {location.location_details}
      </p>
    );
  });

  return (
    <section className="section-footer container">
      {pageName === "home" ? (
        <HashLink className="footer-logo-container" to="#headerTop">
          <img 
            src="/logo.svg"  // IMPORTANTE: usa solo "/logo.svg" (no "/public/logo.svg")
            alt="CINE CRISP - Experiencia cinematográfica en La Paz"
            className="footer-logo-icon"
          />
          <h1 className="footer-logo-text">CINE CRISP</h1>
        </HashLink>
      ) : (
        <Link className="footer-logo-container" to="/">
          {/* Logo con la ruta que especificaste */}
          <img 
            src="/logo.svg"  // IMPORTANTE: usa solo "/logo.svg" (no "/public/logo.svg")
            alt="CINE CRISP - Experiencia cinematográfica en La Paz"
            className="footer-logo-icon"
          />
          <h1 className="footer-logo-text">CINE CRISP</h1>
        </Link>
      )}

      <div className="footer-link-container foot-reg">
        <button
          className="footer-btn"
          onClick={() => {
            dispatch(showSignModal());
          }}
        >
          Crea una Cuenta
        </button>
      </div>

      <div className="footer-link-container">
        <button
          className="footer-btn"
          onClick={() => {
            dispatch(showLoginModal());
          }}
        >
          Inicia Sesión
        </button>
      </div>

      <div className="footer-link-container">
        <Link className="footer-link" to="/aboutus">
          Nosotros...
        </Link>
      </div>

      <h3 className="footer-heading">Nuestras centrales</h3>

      <p className="copyright">
        Copyright &copy; 2025 Análisis y Diseño de Sistemas 2 GRUPO 1{" "}
      </p>

      <div className="footer-address-container">
        {loading ? <HashLoader color="#eb3656" /> : locations}
      </div>
    </section>
  );
};
