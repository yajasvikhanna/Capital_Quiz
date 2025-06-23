// const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000'

// export const API_ENDPOINTS = {
//   QUESTION: `${API_BASE_URL}question/`,
//   CHECK_ANSWER: `${API_BASE_URL}check-answer/`,
//   REFRESH_COUNTRIES: `${API_BASE_URL}refresh-countries/`
// }


// export default API_BASE_URL


let API_BASE_URL = '';

if (window.location.hostname.includes('localhost') || window.location.hostname === '127.0.0.1') {
  // Local environment
  API_BASE_URL = 'http://localhost:8000/api/';
} else {
  // Production environment use value from .env
  API_BASE_URL = import.meta.env.VITE_API_BASE_URL;
}

export const API_ENDPOINTS = {
  QUESTION: `${API_BASE_URL}question/`,
  CHECK_ANSWER: `${API_BASE_URL}check-answer/`,
  REFRESH_COUNTRIES: `${API_BASE_URL}refresh-countries/`,
};

export default API_BASE_URL;
