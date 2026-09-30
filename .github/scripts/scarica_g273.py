"""Scarica SOLO G273_PALERMO.zip da SICILIA.zip (range request) ed estrae il GML delle particelle."""
import io, sys, zipfile
from remotezip import RemoteZip

URL = "https://wfs-download.cartografia.agenziaentrate.eu/wfsdownload/SICILIA.zip"
HDR = {"User-Agent": "Mozilla/5.0"}  # senza UA l'Agenzia risponde 403
out = sys.argv[1] if len(sys.argv) > 1 else "."

# 1) dal zip regionale (1,3 GB) si legge via HTTP Range solo PA.zip (~220 MB)
with RemoteZip(URL, headers=HDR) as regione:
    pa = regione.read("PA.zip")
# 2) da PA.zip solo il comune G273_PALERMO.zip
with zipfile.ZipFile(io.BytesIO(pa)) as prov:
    nome = next(n for n in prov.namelist() if n.split("/")[-1].startswith("G273_"))
    comune = prov.read(nome)
del pa
# 3) dal comune il GML PLE (particelle)
with zipfile.ZipFile(io.BytesIO(comune)) as com:
    gml = next(n for n in com.namelist() if n.lower().endswith(".gml") and "_ple" in n.lower())
    with com.open(gml) as s, open(f"{out}/G273_ple.gml", "wb") as d:
        d.write(s.read())
print("ok", nome, gml)
