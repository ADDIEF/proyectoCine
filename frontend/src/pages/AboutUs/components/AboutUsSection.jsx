export const AboutUsSection = () => {
  return (
    <section className="section-about-us">
      <div className="container">
        <div className="about-us-heading">
          Descubre la magia de
          <div className="aboutus-logo-container">
            {/* Reemplazado: SVG por tu imagen */}
            <img 
              src="/public/logo.svg"  // Ajusta la ruta según tu estructura
              alt="Logo CINECRISP"
              className="aboutus-logo-icon"
            />
            <h1 className="aboutus-logo-text">CINECRISP</h1>
          </div>
        </div>
        <div className="about-us-body">
          <p>¡Bienvenidos a CINECRISP!</p>
          <p>
            En el corazón de La Paz, CINECRISP es más que un cine: es un refugio
            donde el séptimo arte se fusiona con la calidez paceña. Nuestras
            salas, equipadas con tecnología de punta y sonido envolvente, te
            transportan desde la altura de nuestra ciudad hasta el centro de
            cada historia.
          </p>
          <p>
            Ofrecemos una experiencia única con pantallas cristalinas y butacas
            de primera, mientras disfrutas de sabores locales como api con
            buñuelos o snacks gourmet inspirados en la gastronomía boliviana.
            ¡Hasta el popcorn tiene nuestro toque altiplánico!
          </p>
          <p>
            Programamos desde estrenos internacionales hasta cine boliviano de
            autor, porque creemos en el poder de las historias que nos reflejan.
            Cada proyección es un viaje, ya sea por los paisajes del Salar en un
            documental o en aventuras de Hollywood con subtítulos en quechua o
            aymara para eventos especiales.
          </p>
          <p>
            Nos enorgullece ser un espacio donde las familias paceñas, jóvenes
            cinéfilos y visitantes crean recuerdos. ¿Nuestro secreto? Combinar
            la modernidad del cine global con el alma festiva de Bolivia.
          </p>
          <p>
            Ven a CINECRISP: donde la pantalla grande brilla a 3,600 metros de
            altura. ¡La mejor vista del cine está aquí!
          </p>
        </div>
      </div>
    </section>
  );
};