#!/bin/bash
# Script seguro para configurar las variables de entorno para MoltyCollab

# Este script ayuda a configurar las credenciales de forma segura
# Las credenciales reales deben ser ingresadas por el usuario

echo "=== Configuración Segura de Credenciales para MoltyCollab ==="
echo ""
echo "NOTA: Este script no almacena credenciales en texto plano"
echo "Las credenciales se deben ingresar manualmente cada vez que se desee desplegar"
echo ""

# Solicitar credenciales al usuario (no se guardan)
read -p "Ingresa GITHUB_APP_ID: " GITHUB_APP_ID
read -p "Ingresa GITHUB_CLIENT_ID: " GITHUB_CLIENT_ID
read -s -p "Ingresa GITHUB_CLIENT_SECRET: " GITHUB_CLIENT_SECRET
echo ""
read -p "Ingresa GITHUB_WEBHOOK_SECRET: " GITHUB_WEBHOOK_SECRET

# Exportar temporalmente para el despliegue
export GITHUB_APP_ID="$GITHUB_APP_ID"
export GITHUB_CLIENT_ID="$GITHUB_CLIENT_ID"
export GITHUB_CLIENT_SECRET="$GITHUB_CLIENT_SECRET"
export GITHUB_WEBHOOK_SECRET="$GITHUB_WEBHOOK_SECRET"

echo ""
echo "Credenciales cargadas temporalmente para esta sesión"
echo "Iniciando despliegue..."

# Aquí iría el proceso de despliegue real
# ./deploy-real.sh