import axios from 'axios';

const API_BASE = import.meta.env.VITE_API_URL || '';

export const api = axios.create({
  baseURL: API_BASE,
  headers: { 'Content-Type': 'application/json' },
});

api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token');
  if (token) config.headers.Authorization = `Bearer ${token}`;
  return config;
});

export async function getOverview() {
  const { data } = await api.get('/api/overview');
  return data;
}

export async function getFilters() {
  const { data } = await api.get('/api/overview/filters');
  return data;
}

export async function getTrends(params = {}) {
  const { data } = await api.get('/api/trends', { params });
  return data;
}

export async function getCompanies() {
  const { data } = await api.get('/api/companies');
  return data;
}

export async function predictRisk(body) {
  const { data } = await api.post('/api/predict', body);
  return data;
}

export async function login(username, password) {
  const { data } = await api.post('/api/auth/login', { username, password });
  return data;
}

export function getPdfReportUrl() {
  const token = localStorage.getItem('token');
  const base = API_BASE || window.location.origin;
  return `${base}/api/reports/pdf${token ? `?token=${token}` : ''}`;
}

export async function getEdaSummary() {
  const { data } = await api.get('/api/reports/eda');
  return data;
}
