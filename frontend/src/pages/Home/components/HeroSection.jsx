import { useDispatch, useSelector } from "react-redux";
import { useNavigate } from "react-router-dom";
import { HashLink } from "react-router-hash-link";
import { showLoginModal } from "../../../reducers/authSlice";
import { resetCart } from "../../../reducers/cartSlice";
import { TextEffect } from "../../../components/TextEffect";

export const HeroSection = () => {
  const navigate = useNavigate();
  const { isAuthenticated, signedPerson } = useSelector(
    (store) => store.authentication
  );
  const dispatch = useDispatch();

  return (
    <section className="section-hero">
      <div className="container hero">
        <div className="hero-text">
          <h1 className="heading-primary">
            <TextEffect preset="slide">
              ¡Déjate llevar por el cine, al estilo boliviano!
            </TextEffect>
          </h1>

          <p className="hero-description">
            Vive la magia del séptimo arte entre paisajes andinos y la calidez de nuestra tierra. 
            Películas que emocionan, en un lugar que te hace sentir como en casa.
          </p>
          <div className="hero-btn-container">
            <button
              onClick={() => {
                dispatch(resetCart());
                isAuthenticated && signedPerson.person_type === "Customer"
                  ? navigate("/purchase")
                  : dispatch(showLoginModal());
              }}
              className="btn btn-full"
            >
              Compra una Entrada!
            </button>
            <HashLink to="#nowShowing" className="btn btn-outline">
              Mira más &darr;
            </HashLink>
          </div>

          <div className="hero-review-section">
            <div className="customers-img">
              <img
                src="/Images/customers/customer-1.jpg"
                className="customer-img"
                alt="Customer Photo"
              />
              <img
                src="/Images/customers/customer-2.jpg"
                className="customer-img"
                alt="Customer Photo"
              />
              <img
                src="/Images/customers/customer-3.jpg"
                className="customer-img"
                alt="Customer Photo"
              />
              <img
                src="/Images/customers/customer-4.jpg"
                className="customer-img"
                alt="Customer Photo"
              />
              <img
                src="/Images/customers/customer-5.jpg"
                className="customer-img"
                alt="Customer Photo"
              />
              <img
                src="/Images/customers/customer-6.jpg"
                className="customer-img"
                alt="Customer Photo"
              />
            </div>

            <p className="hero-review-text">
              <span>10,370+</span> Entradas vendidas el último año
            </p>
          </div>
        </div>

        <div className="hero-img-box">
          <img
            className="hero-img"
            src="/Images/hero-img.webp"
            alt="Hero Image"
          />
        </div>
      </div>
    </section>
  );
};
