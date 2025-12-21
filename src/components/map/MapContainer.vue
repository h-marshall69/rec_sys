<template>
  <div id="mapContainer"></div>
  <button class="fab-location" @click="$emit('trigger-gps')">
    📍
  </button>
</template>

<script setup>
import { onMounted, ref, watch, toRaw } from 'vue';
import L from 'leaflet';
import 'leaflet/dist/leaflet.css';
import { PUNO_COORDS, COLORES_TIPO } from '@/constants';

const props = defineProps({
  restaurants: {
    type: Array,
    default: () => []
  },
  userLocation: {
    type: Array,
    default: null
  }
});

const emit = defineEmits(['update-location', 'trigger-gps']);

const mapa = ref(null);
const userMarker = ref(null);
const markersGroup = ref(null);

onMounted(() => {
  initMap();
});

watch(() => props.restaurants, (newRestaurantes) => {
  if (mapa.value) {
    renderMarkers(newRestaurantes);
  }
}, { deep: true });

watch(() => props.userLocation, (newCoords) => {
  if (newCoords && mapa.value) {
    updateUserMarker(newCoords);
  }
});

const initMap = () => {
  // Check if map already initialized
  if (mapa.value) return;

  const startCoords = props.userLocation || PUNO_COORDS;
  mapa.value = L.map('mapContainer', { zoomControl: false }).setView(startCoords, 15);

  L.tileLayer('https://{s}.basemaps.cartocdn.com/rastertiles/voyager/{z}/{x}/{y}{r}.png', {
    attribution: '© OpenStreetMap, © CartoDB',
    maxZoom: 20
  }).addTo(mapa.value);

  markersGroup.value = L.layerGroup().addTo(mapa.value);

  createUserMarker(startCoords);

  if (props.restaurants.length > 0) {
    renderMarkers(props.restaurants);
  }

  // Evento para click en el mapa
  mapa.value.on('click', (e) => {
    emit('update-location', [e.latlng.lat, e.latlng.lng]);
  });
};

const createUserMarker = (coords) => {
  if (userMarker.value) {
    userMarker.value.setLatLng(coords);
  } else {
    userMarker.value = L.circleMarker(coords, {
      radius: 10, color: '#fff', fillColor: '#2196F3', fillOpacity: 1, weight: 3, pane: 'markerPane'
    }).addTo(mapa.value).bindPopup("Tu ubicación");
  }
};

const updateUserMarker = (coords) => {
  createUserMarker(coords);
  mapa.value.flyTo(coords, 16);
};

const renderMarkers = (restaurantes) => {
  if (!markersGroup.value) return;
  markersGroup.value.clearLayers();

  restaurantes.forEach(est => {
    const lat = est.ubicacion.latitud;
    const lng = est.ubicacion.longitud;
    const tipo = est.tipo;

    const color = COLORES_TIPO[tipo] || COLORES_TIPO.default;

    const pin = L.circleMarker([lat, lng], {
      color: 'white', fillColor: color, fillOpacity: 0.9, radius: 10, weight: 2
    });

    const imgUrl = `https://placehold.co/300x150/${color.replace('#', '')}/white?text=${encodeURIComponent(est.nombre)}`;
    const direccion = est.ubicacion.direccion || "Puno, Centro";
    const cocina = est.cocina ? `• Cocina: ${est.cocina}` : '';
    const sitioWeb = est.sitio_web ? `<a href="${est.sitio_web}" target="_blank" style="color:${color}">🌐 Web</a>` : '';

     const popupHtml = `
        <div style="width: 200px; text-align: center; overflow: hidden; font-family: sans-serif;">
          <div style="width:100%; height:80px; background: url('${imgUrl}') center/cover; border-radius: 8px 8px 0 0;"></div>
          <div style="padding: 8px;">
            <h3 style="margin:0; font-size: 15px; color: #333;">${est.nombre}</h3>
            <p style="margin:4px 0; font-size: 11px; color: #666;">
               ${direccion} <br>
               ${cocina}
            </p>
            <div style="display:flex; justify-content:space-between; align-items:center; margin-top:5px;">
                <span style="background:${color}; color:white; padding:2px 6px; border-radius:4px; font-size:10px; text-transform:uppercase;">${tipo}</span>
                <span style="font-size:11px;">${sitioWeb}</span>
            </div>
          </div>
        </div>
      `;

    pin.bindPopup(popupHtml);
    markersGroup.value.addLayer(pin);
  });
};
</script>

<style scoped>
#mapContainer {
  height: 100%;
  width: 100%;
  z-index: 1;
  background: #eee;
}

.fab-location {
  position: absolute;
  bottom: 30px;
  right: 20px;
  width: 50px;
  height: 50px;
  border-radius: 50%;
  background: white;
  border: none;
  font-size: 24px;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
  z-index: 999;
  cursor: pointer;
}
</style>
