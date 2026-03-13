export function getApiBaseUrl(): string {
  if (process.env.NEXT_PUBLIC_API_BASE_URL) {
    return process.env.NEXT_PUBLIC_API_BASE_URL;
  }

  if (typeof window === "undefined") {
    return "http://localhost:8000";
  }

  const { protocol, hostname } = window.location;
  if (hostname === "localhost" || hostname === "127.0.0.1") {
    return `${protocol}//${hostname}:8000`;
  }

  throw new Error("NEXT_PUBLIC_API_BASE_URL must be set outside local development.");
}

export async function parseJsonSafely(response: Response): Promise<unknown | null> {
  const responseText = await response.text();
  if (!responseText) {
    return null;
  }

  try {
    return JSON.parse(responseText) as unknown;
  } catch {
    return null;
  }
}

export function isRecord(value: unknown): value is Record<string, unknown> {
  return typeof value === "object" && value !== null;
}

export function getApiErrorMessage(value: unknown): string | null {
  if (!isRecord(value)) {
    return null;
  }

  const error = value.error;
  if (!isRecord(error) || typeof error.message !== "string") {
    return null;
  }

  return error.message;
}
