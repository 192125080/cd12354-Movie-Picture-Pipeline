import React, { useEffect, useState } from 'react';
import axios from 'axios';
import PropTypes from 'prop-types';

function MovieDetail({ movie }) {
  const [details, setDetails] = useState(null);
  const [error, setError] = useState(false);
  useEffect(() => {
    setDetails(null);
    setError(false);
    axios
      .get(`${process.env.REACT_APP_MOVIE_API_URL}/movies/${movie.id}`)
      .then((response) => setDetails(response.data))
      .catch(() => setError(true));
  }, [movie]);

  if (error) {
    return <p role="alert">Unable to load movie details.</p>;
  }

  return (
    <div>
      <h2>{details?.movie.title}</h2>
      <p>{details?.movie.description}</p>
    </div>
  );
}

MovieDetail.propTypes = {
  movie: PropTypes.shape({
    id: PropTypes.oneOfType([PropTypes.number, PropTypes.string]).isRequired,
  }).isRequired,
};

export default MovieDetail;
