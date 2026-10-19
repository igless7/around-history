from flask import Flask, render_template, request, jsonify
from src.database import get_engine, init_db, get_session_factory
from src.validator import validate_coordinates, validate_radius
from src.geocoding import address_to_coordinates
from src.wiki_service import fetch_nearby_history
from src.models import HistorySearchModel

app = Flask(__name__)

# Configurar Base de Datos SQLite
engine = get_engine()
init_db(engine)
SessionFactory = get_session_factory(engine)

@app.route('/')
def home():
    """Renders de la página principal."""
    return render_template('index.html')

@app.route('/api/search', methods=['POST'])
def search_history():
    """
    Endpoint API que procesa la búsqueda por GPS o Dirección
    y persiste el historial en la BD.
    """
    data = request.get_json() or {}
    
    try:
        radius_km = validate_radius(data.get("radius_km", 5.0))
        address = data.get("address")
        
        # Determinar coordenadas
        if address:
            lat, lon, display_name = address_to_coordinates(address)
        else:
            raw_lat = data.get("latitude")
            raw_lon = data.get("longitude")
            coords = validate_coordinates(raw_lat, raw_lon)
            lat, lon = coords.latitude, coords.longitude
            display_name = None

        # Consultar la API externa de Wikipedia
        results = fetch_nearby_history(lat, lon, radius_km)

        # Persistir resultados en la Base de Datos usando SQLAlchemy Session
        session = SessionFactory()
        for item in results:
            record = HistorySearchModel(
                address_query=display_name or address,
                latitude=lat,
                longitude=lon,
                radius_km=radius_km,
                place_title=item["title"],
                distance_km=item["distance_km"],
                page_url=item["url"]
            )
            session.add(record)
        session.commit()
        session.close()

        return jsonify({
            "status": "success",
            "search_location": {"lat": lat, "lon": lon, "display_name": display_name},
            "results": results
        }), 200

    except ValueError as ve:
        return jsonify({"error": str(ve)}), 400
    except Exception as e:
        return jsonify({"error": f"Error interno: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)