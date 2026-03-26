#!/bin/bash
# 🚀 Script de despliegue automático para MoltyCollab MVP

set -e  # Exit on any error

echo "🚀 Iniciando despliegue de MoltyCollab MVP..."

# Check if we're in the right directory
if [ ! -f "projects/moltycollab/backend/main.py" ]; then
    echo "❌ Error: No se encontró el directorio de MoltyCollab"
    echo "Navegue al directorio raíz del proyecto antes de ejecutar este script"
    exit 1
fi

# Check if docker is installed
if ! command -v docker &> /dev/null; then
    echo "❌ Error: Docker no está instalado"
    echo "Instale Docker antes de ejecutar este script"
    exit 1
fi

# Check if docker-compose is installed
if ! command -v docker-compose &> /dev/null; then
    echo "❌ Error: Docker Compose no está instalado"
    echo "Instale Docker Compose antes de ejecutar este script"
    exit 1
fi

echo "✅ Prerrequisitos verificados"

# Create .env file if it doesn't exist
ENV_FILE="projects/moltycollab/.env"
if [ ! -f "$ENV_FILE" ]; then
    echo "📝 Creando archivo .env con valores por defecto..."
    cat > "$ENV_FILE" << EOF
# GitHub OAuth Configuration
GITHUB_CLIENT_ID=Iv23li2P6I0qQ48VYNoE
GITHUB_CLIENT_SECRET=00bb9c128a9ce25d55909f6ddd7c98138c735d9f
GITHUB_REDIRECT_URI=http://localhost:8000/auth/github/callback

# GitHub App Configuration
GITHUB_APP_ID=2792036
GITHUB_APP_PRIVATE_KEY_PATH=../../../nautilus/private-key.pem
GITHUB_WEBHOOK_SECRET=moltycollab-webhook-secret-202666-583976

# Security
SECRET_KEY=0000000000000000000000000000000000000000000000000000000000000000

# Database
DATABASE_URL=postgresql://moltycollab:password@db:5432/moltycollab

# Redis
REDIS_URL=redis://redis:6379
EOF
    echo "✅ Archivo .env creado"
fi

echo "📂 Cambiando al directorio de MoltyCollab..."
cd projects/moltycollab

echo "🐳 Construyendo imágenes de Docker..."
docker-compose build

echo "🚀 Iniciando servicios..."
docker-compose up -d

echo "⏳ Esperando a que los servicios estén listos..."
sleep 30

# Check if backend is running
echo "🔍 Verificando estado del backend..."
if curl -f http://localhost:8000/health >/dev/null 2>&1; then
    echo "✅ Backend está corriendo correctamente"
else
    echo "⚠️  Backend puede tardar unos segundos más en iniciar"
    sleep 30
    if curl -f http://localhost:8000/health >/dev/null 2>&1; then
        echo "✅ Backend está corriendo correctamente"
    else
        echo "❌ Error: Backend no está respondiendo"
        echo "Revise los logs con: docker-compose logs backend"
        exit 1
    fi
fi

echo "🌐 Aplicación disponible en:"
echo "  Backend: http://localhost:8000"
echo "  Frontend: http://localhost:3000"
echo "  Health Check: http://localhost:8000/health"
echo "  API Docs: http://localhost:8000/api/v1/docs"

echo ""
echo "📋 Pasos siguientes:"
echo "1. Abra http://localhost:3000 para acceder a la interfaz"
echo "2. Para ver logs: docker-compose logs -f"
echo "3. Para detener: docker-compose down"
echo "4. Para reiniciar: docker-compose restart"

echo ""
echo "🎉 ¡Despliegue de MoltyCollab MVP completado exitosamente!"
echo "🔧 Para configurar en producción, actualice las variables en .env con valores seguros"