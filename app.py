from flask import Flask, render_template, request, redirect, jsonify
from sqlalchemy.orm import Session
from database import engine, PuntoInteres
from geoalchemy2.elements import WKTElement

app = Flask(__name__)

# Página principal con formulario para agregar puntos de interés
@app.route('/')
def index():
    return render_template('index.html')

# Endpoint para manejar la carga de datos desde el formulario
@app.route('/add', methods=['POST'])
def add_point():
    nombre = request.form['nombre']
    descripcion = request.form['descripcion']
    latitud = float(request.form['latitud'])
    longitud = float(request.form['longitud'])
    capa = request.form['capa']

    # Crear un nuevo punto en la base de datos
    with Session(engine) as session:
        punto = PuntoInteres(
            nombre=nombre,
            descripcion=descripcion,
            latitud=latitud,
            longitud=longitud,
            capa=capa,
            geom=WKTElement(f'POINT({longitud} {latitud})', srid=4326)  # SRID 4326 para WGS84
        )
        session.add(punto)
        session.commit()

    return redirect('/map')

# Página para visualizar el mapa con la capa GeoJSON
@app.route('/map')
def map_view():
    return render_template('map.html')

# Endpoint para generar GeoJSON desde la base de datos
@app.route('/geojson')
@app.route('/geojson', methods=['GET'])
def geojson():
    capa = request.args.get('capa')  # Obtener la capa desde los parámetros de la URL
    with Session(engine) as session:
        if capa:
            puntos = session.query(PuntoInteres).filter(PuntoInteres.capa == capa).all()
        else:
            puntos = session.query(PuntoInteres).all()  # Si no hay capa, se devuelven todos los puntos

        features = []
        for punto in puntos:
            features.append({
                "type": "Feature",
                "geometry": {
                    "type": "Point",
                    "coordinates": [punto.longitud, punto.latitud]
                },
                "properties": {
                    "nombre": punto.nombre,
                    "descripcion": punto.descripcion,
                    "capa": punto.capa
                }
            })

        geojson_data = {
            "type": "FeatureCollection",
            "features": features
        }

        return jsonify(geojson_data)

# def geojson():
#     with Session(engine) as session:
#         puntos = session.query(PuntoInteres).all()
#
#         # Construir GeoJSON manualmente
#         features = []
#         for punto in puntos:
#             features.append({
#                 "type": "Feature",
#                 "geometry": {
#                     "type": "Point",
#                     "coordinates": [punto.longitud, punto.latitud]
#                 },
#                 "properties": {
#                     "nombre": punto.nombre,
#                     "descripcion": punto.descripcion
#                 }
#             })
#
#         geojson_data = {
#             "type": "FeatureCollection",
#             "features": features
#         }
#
#         return jsonify(geojson_data)

if __name__ == '__main__':
    app.run(debug=True)
