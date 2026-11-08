# Workflow particelle catastali (PRG2004/particelle)

1. **GML → GPKG**: plugin QGIS `CatastoIT_GML_Merger_Pro` (cartella qui accanto), layer PLE del comune.
   Campi prodotti: `foglio`, `particella` (+ `comune`, `sez_censuaria` se richiesti).
2. **GPKG → PMTiles + superficie**:
   ```
   python build_particelle_tiles.py particelle.gpkg particelle.pmtiles
   ```
   Lo script (shapely, pyproj, tippecanoe via WSL su Windows):
   - calcola `sup_mq` (m², area geodetica WGS84 sulla geometria **intera**) e lo **scrive nel GPKG**
     (colonna `sup_mq`; `--no-writeback` per non toccarlo);
   - scrive `sup_mq` nelle properties del layer `particelle`;
   - genera il layer `particelle_label` (1 punto interno per particella, etichette uniche).
   Accetta anche `.geojson`/`.geojsonl` (una feature per riga).
3. **Pubblicazione**: copia il `.pmtiles` qui (tenendo il backup del precedente) e fai commit/push.

Note
- `sup_mq` è una superficie **calcolata**, non quella in visura: può differire. La scheda
  (`palermohub/pmtiles/js/card.js`) la etichetta "calcolata"; senza `sup_mq` nei tile ripiega su una stima "≈".
- L'AdE non fornisce una superficie ufficiale nel GML PLE usato: il GPKG ha solo foglio/particella.
- Rigenerare **sempre** con questo script: senza `particelle_label` le etichette risultano doppie.
