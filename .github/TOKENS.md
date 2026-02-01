# Gestión de Tokens GitHub - MoltyCollab

## ⚠️ IMPORTANTE
**Este archivo NO debe versionarse en git.**
Ver: .github/workflows/token-rotation.yml para recordatorios.

## Política de Rotación
- Crear nuevo token cada 25-28 días
- Revocar token anterior después de confirmar nuevo funciona
- Nunca más de 2 tokens activos simultáneamente

## Proceso de Rotación
1. Generar nuevo token en: https://github.com/settings/tokens
2. Nombre: `MoltyCollab Auto-{fecha}`
3. Permisos: repo, workflow
4. Expiración: 30 días
5. Probar: `gh auth login --with-token`
6. Revocar token anterior

## Variables de Entorno
```bash
export MOLTYCOLLAB_GITHUB_TOKEN="[TOKEN_AQUI]"
export MOLTYCOLLAB_GITHUB_USER="moltycollab"
```
