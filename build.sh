npm run linux-build
sed -i 's/<div id="overlays">/<div id="overlays"><span id="error">{{ slug }}<\/span>/g' build/index.html
