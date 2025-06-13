import axios from "axios";
import { useState } from "react";
import { useSelector } from "react-redux";
import { adminErrorToast, adminMovieToast } from "../../../toasts/toast";

export const AdminMovieAddSection = () => {
  const { signedPerson } = useSelector((store) => store.authentication);

  const [movieInfo, setMovieInfo] = useState({
    movieName: "",
    imagePath: "",
    language: "",
    description: "",
    rating: "",
    duration: "",
    cast: "",
    relDate: "",
    genres: "",
    directors: "",
  });
  const [adminMovieDropDown, setAdminMovieDropDown] = useState(false);
  const [loading, setLoading] = useState(false);

  const toggleAdminSection = () => {
    setAdminMovieDropDown((prevState) => !prevState);
  };

  const handleMovieInfo = (e) => {
    const name = e.target.name;
    const value =
      name === "genres" || name === "directors"
        ? e.target.value.split(",")
        : e.target.value;

    setMovieInfo((prevInfo) => {
      return {
        ...prevInfo,
        [name]: name === "rating" ? parseFloat(value) : value,
      };
    });
  };

  const movieAdd = async (e) => {
    e.preventDefault();

    // Validaciones básicas
    const {
      movieName, imagePath, language, description, rating,
      duration, cast, relDate, genres, directors,
    } = movieInfo;

    // Validaciones personalizadas
    if (!movieName || !imagePath || !language || !description || !cast) {
      adminErrorToast("Por favor, complete todos los campos de texto.");
      return;
    }

    if (!rating || isNaN(rating) || rating < 0 || rating > 10) {
      adminErrorToast("El rating debe ser un número entre 0 y 10.");
      return;
    }

    const dateRegex = /^\d{4}-\d{2}-\d{2}$/;
    if (!relDate.match(dateRegex)) {
      adminErrorToast("La fecha debe estar en el formato aaaa-mm-dd.");
      return;
    }

    const durationRegex = /^(\d+h)?\s?(\d+m)?$/;
    if (!duration.match(durationRegex)) {
      adminErrorToast("Duración inválida. Ejemplo válido: '1h 30m'");
      return;
    }

    if (!Array.isArray(genres) || genres.length === 0) {
      adminErrorToast("Debe ingresar al menos un género.");
      return;
    }

    if (!Array.isArray(directors) || directors.length === 0) {
      adminErrorToast("Debe ingresar al menos un director.");
      return;
    }

    try {
      setLoading(true);
      const movieResponse = await axios.post(
        `${import.meta.env.VITE_API_URL}/adminMovieAdd`,
        {
          email: signedPerson.email,
          password: signedPerson.password,
          name: movieName,
          image_path: imagePath,
          language,
          synopsis: description,
          rating,
          duration,
          top_cast: cast,
          release_date: relDate,
        }
      );

      const movieId = movieResponse.data?.[0]?.last_id;

      if (!movieId) {
        console.error("last_id no recibido:", movieResponse.data);
        adminErrorToast("Error al registrar la película.");
        return;
      }

      for (const genre of genres) {
        await axios.post(`${import.meta.env.VITE_API_URL}/genreInsert`, {
          email: signedPerson.email,
          password: signedPerson.password,
          movieId,
          genre,
        });
      }

      for (let idx = 0; idx < directors.length; idx++) {
        const director = directors[idx];
        await axios.post(`${import.meta.env.VITE_API_URL}/directorInsert`, {
          email: signedPerson.email,
          password: signedPerson.password,
          movieId,
          director,
        });

        if (idx === directors.length - 1) {
          adminMovieToast();
        }
      }

      toggleAdminSection();
    } catch (err) {
      console.error(err);
      adminErrorToast(err.response?.data?.message || "Error inesperado.");
    } finally {
      setMovieInfo({
        movieName: "",
        imagePath: "",
        language: "",
        description: "",
        rating: "",
        duration: "",
        cast: "",
        relDate: "",
        genres: "",
        directors: "",
      });
      setLoading(false);
    }
  };

  return (
    <section className="section-admin-movie-add container">
      <div className="form-heading-container">
        <h2 className="form-admin-heading">Añadir una Pelicula</h2>
        <button className="btn-admin-arrow" onClick={toggleAdminSection}>
          {!adminMovieDropDown ? (
            <svg
              xmlns="http://www.w3.org/2000/svg"
              className="admin-icon"
              viewBox="0 0 512 512"
            >
              <path
                fill="none"
                stroke="currentColor"
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth="48"
                d="M112 184l144 144 144-144"
              />
            </svg>
          ) : (
            <svg
              xmlns="http://www.w3.org/2000/svg"
              className="admin-icon"
              viewBox="0 0 512 512"
            >
              <path
                fill="none"
                stroke="currentColor"
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth="48"
                d="M112 328l144-144 144 144"
              />
            </svg>
          )}
        </button>
      </div>

      {adminMovieDropDown && (
        <form className="form-movie-add" onSubmit={movieAdd}>
          <div>
            <p>Nombre de la Pelicula:</p>
            <input
              name="movieName"
              onChange={(e) => handleMovieInfo(e)}
              type="text"
              placeholder="Ingrese el nombre..."
            />
          </div>

          <div>
            <p>Ruta - Foto de Cartelera:</p>
            <input
              name="imagePath"
              onChange={(e) => handleMovieInfo(e)}
              type="text"
              placeholder="Ingresar ruta de la imagen"
            />
          </div>

          <div>
            <p>Idioma:</p>
            <input
              name="language"
              onChange={(e) => handleMovieInfo(e)}
              type="text"
              placeholder="Ingrese idioma..."
            />
          </div>

          <div>
            <p>Sinopsis:</p>
            <input
              name="description"
              onChange={(e) => handleMovieInfo(e)}
              placeholder="Breve descripción..."
            />
          </div>

          <div>
            <p>Rating:</p>
            <input
              name="rating"
              onChange={(e) => handleMovieInfo(e)}
              type="text"
              placeholder="Ingrese la clasificacion"
            />
          </div>

          <div>
            <p>Duración:</p>
            <input
              name="duration"
              onChange={(e) => handleMovieInfo(e)}
              type="text"
              placeholder="Ingrese la duración..."
            />
          </div>

          <div>
            <p>Casting:</p>
            <input
              name="cast"
              onChange={(e) => handleMovieInfo(e)}
              type="text"
              placeholder="Nombre del actor/actriz principal"
            />
          </div>

          <div>
            <p>Fecha de Lanzamiento:</p>
            <input
              name="relDate"
              onChange={(e) => handleMovieInfo(e)}
              type="text"
              placeholder="(aaaa-mm-dd)"
            />
          </div>

          <div>
            <p>Géneros de la Pelicula:</p>
            <input
              name="genres"
              onChange={(e) => handleMovieInfo(e)}
              type="text"
              placeholder="Ingreselos separados por una coma"
            />
          </div>

          <div>
            <p>Directores de la pelicula:</p>
            <input
              name="directors"
              onChange={(e) => handleMovieInfo(e)}
              type="text"
              placeholder="Ingreselos separados por una coma"
            />
          </div>

          <button type="submit" className="btn-admin" disabled={loading}>
            {loading ? "Loading..." : "CONFIRM"}
          </button>
        </form>
      )}
    </section>
  );
};
