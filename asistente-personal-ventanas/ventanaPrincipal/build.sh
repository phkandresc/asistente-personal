#!/bin/bash

# Configuración
UI_FILE="sidebar.ui"
UI_PY="sidebar.py"
QRC_FILE="resource.qrc"
QRC_PY="resource_rc.py"

echo "🎯 Generando archivo Python desde UI..."
python -m PyQt6.uic.pyuic "$UI_FILE" -o "$UI_PY"

if [ $? -ne 0 ]; then
    echo "❌ Error al compilar el archivo UI."
    exit 1
fi

echo "✅ Archivo UI convertido correctamente: $UI_PY"

echo "🎯 Generando archivo Python desde QRC..."
python -m PyQt6.pyrcc_main "$QRC_FILE" -o "$QRC_PY"

if [ $? -ne 0 ]; then
    echo "❌ Error al compilar el archivo QRC."
    exit 1
fi

echo "✅ Archivo QRC convertido correctamente: $QRC_PY"

echo "🚀 Proceso finalizado correctamente."
