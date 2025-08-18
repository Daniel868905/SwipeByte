import { apiUrl } from '../config';

function getToken() {
  try {
    const ls = localStorage.getItem('auth_token')
    if (ls) return ls
  } catch {
    // Ignore if localStorage is unavailable
  }
  const m = (document.cookie || '').match(/(?:^|;\s*)auth_token=([^;]+)/)
  return m ? decodeURIComponent(m[1]) : null
}

const origFetch = window.fetch.bind(window);

window.fetch = (input, init = {}) => {
  let url = input;

  // Normalize /api/... to absolute URL
  if (typeof input === 'string' && input.startsWith('/api/')) {
    url = apiUrl(input);
  } else if (input instanceof URL && input.pathname.startsWith('/api/')) {
    url = apiUrl(input.pathname + input.search);
  }

  // Normalize headers and add Authorization if missing
  const headers = new Headers(init && init.headers ? init.headers : undefined);
  const token = getToken();
  if (token && !headers.has('Authorization')) {
    headers.set('Authorization', `Token ${token}`);
  }

  return origFetch(url, { ...init, headers });
};
