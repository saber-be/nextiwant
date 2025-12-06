import type { TokenResponse } from '../../shared/types/api';

const ACCESS_TOKEN_KEY = 'iliketohave_access_token';
const EXPIRES_AT_KEY = 'iliketohave_expires_at';

export function saveToken(token: TokenResponse, remember: boolean): void {
  if (typeof window === 'undefined') return;
  const storage = remember ? window.localStorage : window.sessionStorage;
  storage.setItem(ACCESS_TOKEN_KEY, token.access_token);
  storage.setItem(EXPIRES_AT_KEY, token.expires_at);
}

export function clearToken(): void {
  if (typeof window === 'undefined') return;
  window.localStorage.removeItem(ACCESS_TOKEN_KEY);
  window.localStorage.removeItem(EXPIRES_AT_KEY);
  window.sessionStorage.removeItem(ACCESS_TOKEN_KEY);
  window.sessionStorage.removeItem(EXPIRES_AT_KEY);
}

export function getToken(): string | null {
  if (typeof window === 'undefined') return null;
  const token = window.localStorage.getItem(ACCESS_TOKEN_KEY) ?? window.sessionStorage.getItem(ACCESS_TOKEN_KEY);
  return token;
}
