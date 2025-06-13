import axios from "axios";
import { useEffect, useState } from "react";
import { HiCalendar, HiOutlineClock, HiOutlineCurrencyDollar, HiOutlineMapPin, HiOutlineTicket, HiOutlineTv } from "react-icons/hi2";
import { RiSofaLine } from "react-icons/ri";
import { useSelector } from "react-redux";
import { Link } from "react-router-dom";
import HashLoader from "react-spinners/HashLoader";

export const CustomerInfoSection = () => {
  const [cusProData, setCusProData] = useState({});
  const [cusTicketData, setCusTicketData] = useState([]);
  const [loading1, setLoading1] = useState(true);
  const [loading2, setLoading2] = useState(true);
  const [error, setError] = useState(null);

  const { signedPerson } = useSelector((store) => store.authentication);

  useEffect(() => {
    const fetchData = async () => {
      // Datos del perfil del cliente
      try {
        const profileResponse = await axios.post(
          `${import.meta.env.VITE_API_URL}/customerProfile`,
          {
            email: signedPerson.email,
            password: signedPerson.password,
          }
        );
        setCusProData(profileResponse.data[0] || {});
      } catch (err) {
        console.error("Error fetching profile:", err);
      } finally {
        setLoading1(false);
      }

      // Historial de compras
      try {
        const purchasesResponse = await axios.post(
          `${import.meta.env.VITE_API_URL}/customerPurchases`,
          {
            email: signedPerson.email,
          }
        );

        const formattedData = purchasesResponse.data.map((purchase) => ({
          ...purchase,
          showtime_date: new Date(purchase.showtime_date).toLocaleDateString("es-ES"),
          purchase_date: new Date(purchase.purchase_date).toLocaleDateString("es-ES"),
          ticket_ids: purchase.ticket_ids || "N/A",
          seat_numbers: purchase.seat_names || "Asiento no especificado"
        }));

        setCusTicketData(formattedData);
        setError(null);
      } catch (err) {
        console.error("Error fetching purchases:", err);
        setError("Error al cargar el historial de compras");
        setCusTicketData([]);
      } finally {
        setLoading2(false);
      }
    };

    fetchData();
  }, [signedPerson]);

  const purchaseHtml = cusTicketData.map((purchase, index) => (
    <Link
      key={`${purchase.payment_id}-${index}`}
      to={`/movieDetails/${purchase.movie_id}`}
      className="purchase-history-item"
    >
      <div className="purchase-item-details">
        <div className="purchase-item-header">
          <h2>{purchase.movie_name}</h2>
          <div className="purchase-show-quality">
            <HiOutlineTv size={18} />
            <p>{purchase.show_type}</p>
          </div>
        </div>

        <div className="purchase-ticket-id">
          <HiOutlineTicket size={16} />
          <p className="ticket-id">ID de Pago: {purchase.payment_id}</p>
        </div>

        <div className="purchase-hall-info">
          <HiOutlineMapPin size={18} />
          <p>
            {purchase.theatre_name} - {purchase.hall_name}
          </p>
        </div>

        <div className="purchase-seat">
          <RiSofaLine size={20} />
          <p>Asientos: {purchase.seat_numbers}</p>
        </div>

        <div className="purchase-date-time">
          <div className="purchase-tags">
            <HiCalendar size={20} />
            <strong>{purchase.showtime_date}</strong>
          </div>
          <div className="purchase-tags">
            <HiOutlineClock size={18} />
            <strong>{purchase.movie_start_time}</strong>
          </div>
        </div>

        <div className="purchase-price-create">
          <div className="purchase-tags">

            <strong>${purchase.ticket_price} Bs</strong>
          </div>
          <div className="purchase-tags">
            <p>
              Comprado el <strong>{purchase.purchase_date}</strong>
            </p>
          </div>
        </div>
      </div>

      <div className="purchase-item-img-box">
        <img
          className="purchase-item-img"
          src={purchase.movie_image}
          alt={`Poster de ${purchase.movie_name}`}
          onError={(e) => {
            e.target.src = '/ruta/a/imagen/por/defecto.jpg';
          }}
        />
      </div>
    </Link>
  ));

  return (
    <div className="section-customer-info">
      <div className="container">
        <h3 className="customer-info-heading">Información del Cliente</h3>
        {loading1 ? (
          <HashLoader color="#eb3656" cssOverride={{ display: 'block', margin: '2.4rem auto' }} />
        ) : (
          <div className="customer-info-details">
            <div>
              <p>Nombre</p>
              <p>:</p>
              <p>{`${cusProData.first_name || ''} ${cusProData.last_name || ''}`}</p>
            </div>
            <div>
              <p>Correo electrónico</p>
              <p>:</p>
              <p>{cusProData.email || 'No disponible'}</p>
            </div>
            <div>
              <p>Teléfono</p>
              <p>:</p>
              <p>{cusProData.phone_number || 'No disponible'}</p>
            </div>
          </div>
        )}

        <h3 className="customer-info-heading">Historial de Compras</h3>
        {loading2 ? (
          <HashLoader color="#eb3656" cssOverride={{ display: 'block', margin: '2.4rem auto' }} />
        ) : error ? (
          <p className="error-message">{error}</p>
        ) : cusTicketData.length === 0 ? (
          <p className="customer-empty-status">No has realizado ninguna compra todavía.</p>
        ) : (
          <div className="purchase-history-section">
            <div className="purchase-history-list">{purchaseHtml}</div>
          </div>
        )}
      </div>
    </div>
  );
};