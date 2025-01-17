export function getPath(path: string): string {
  // Ensure base has leading slash but no trailing slash
  const base = import.meta.env.BASE_URL.endsWith("/")
    ? import.meta.env.BASE_URL.slice(0, -1)
    : import.meta.env.BASE_URL;
  const baseWithSlash = base.startsWith("/") ? base : `/${base}`;

  // Clean the path to have no leading or trailing slashes
  const cleanPath = path.replace(/^\/+|\/+$/g, "");

  // Handle root path specially
  if (cleanPath === "") {
    return `${baseWithSlash}/index.html`;
  }

  // Don't append index.html if path already ends with .html
  if (cleanPath.endsWith(".html")) {
    return `${baseWithSlash}/${cleanPath}`;
  }

  // Append index.html to the path
  return `${baseWithSlash}/${cleanPath}/index.html`;
}
