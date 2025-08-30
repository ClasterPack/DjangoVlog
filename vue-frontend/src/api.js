export async function fetchJSON(url) {
  const res = await fetch(url, { headers: { 'Accept': 'application/json' } })
  if (!res.ok) throw new Error(`HTTP ${res.status}`)
  return await res.json()
}
export function pagesListUrl(page=1, pageSize=10){const u=new URL('/api/pages/',window.location.origin);u.searchParams.set('page',page);u.searchParams.set('page_size',pageSize);return u.toString()}
export function pageDetailUrl(id){return `/api/pages/${id}/`}