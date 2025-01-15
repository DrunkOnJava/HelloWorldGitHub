export function getPath(path: string): string {
  const base = import.meta.env.BASE_URL;
  // Remove leading slash if present since base already includes it
  const cleanPath = path.startsWith("/") ? path.slice(1) : path;
  return `${base}${cleanPath}`;
}
