import os
import requests

API_KEY = os.getenv("PARSE_BOT_API_KEY", "pmx_580102e639490ef96149eee8f588d1bd")
BASE_URL = "https://api.parse.bot/scraper/73fcfdc9-d8df-488d-b5fa-66bb10075e9c"

HEADERS = {
    "X-API-Key": API_KEY.strip()
}

def search_products(query: str, limit: int = 5) -> dict:
    """
    Busca productos en el catálogo de Classic Football Shirts usando palabras clave
    (equipo, marca, temporada, estilo, etc.).
    """
    url = f"{BASE_URL}/search_products"
    params = {"query": query, "limit": limit}
    
    try:
        response = requests.get(url, headers=HEADERS, params=params, timeout=15)
        response.raise_for_status()
        data = response.json()
        
        if data.get("status") == "success":
            return {
                "success": True,
                "query": query,
                "total": data.get("data", {}).get("total", 0),
                "products": data.get("data", {}).get("products", [])
            }
        return {"success": False, "error": "Respuesta no exitosa de Parse"}
    except Exception as e:
        return {"success": False, "error": str(e)}


def get_products_by_team(team: str, limit: int = 5) -> dict:
    """
    Busca camisetas y productos específicos filtrados exclusivamente por el nombre de un club.
    """
    url = f"{BASE_URL}/get_products_by_team"
    params = {"team": team, "limit": limit}
    
    try:
        response = requests.get(url, headers=HEADERS, params=params, timeout=15)
        response.raise_for_status()
        data = response.json()
        
        if data.get("status") == "success":
            return {
                "success": True,
                "team": team,
                "total": data.get("data", {}).get("total", 0),
                "products": data.get("data", {}).get("products", [])
            }
        return {"success": False, "error": "Respuesta no exitosa de Parse"}
    except Exception as e:
        return {"success": False, "error": str(e)}