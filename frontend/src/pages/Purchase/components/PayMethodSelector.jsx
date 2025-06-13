import { useDispatch, useSelector } from "react-redux";
import { setPaymentMethod } from "../../../reducers/cartSlice";

export const PayMethodSelector = ({ paymentOngoing }) => {
  const { payment_method: userPayMethod } = useSelector((store) => store.cart);
  const dispatch = useDispatch();

  const checkedColor = (val) => {
    return {
      backgroundColor: val === userPayMethod ? "#ef5e78" : "",
      border: val === userPayMethod ? "2px solid transparent" : "",
    };
  };

  return (
    <div>
      <form>
        <div className="form-item-heading">Selecciona un Método de Pago</div>
        <div className="form-pay-options">
          <div
            className="pay-input-container"
            key="Credit Card"
            style={checkedColor("Credit Card")}
          >
            <input
              disabled={paymentOngoing}
              type="radio"
              id={1}
              name="Select Payment"
              value="Credit Card"
              onChange={(e) => dispatch(setPaymentMethod(e.target.value))}
              checked={"Credit Card" === userPayMethod}
            />

            <label className="form-pay-detail" htmlFor={1}>
              Tarjeta de Crédito
            </label>
          </div>

          <div
            className="pay-input-container"
            key="Debit Card"
            style={checkedColor("Debit Card")}
          >
            <input
              disabled={paymentOngoing}
              type="radio"
              id={2}
              name="Select Payment"
              value="Debit Card"
              onChange={(e) => dispatch(setPaymentMethod(e.target.value))}
              checked={"Debit Card" === userPayMethod}
            />

            <label className="form-pay-detail" htmlFor={2}>
              Tarjeta de Débito
            </label>
          </div>
        </div>
      </form>
    </div>
  );
};