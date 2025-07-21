# 🚀 SuperClaude Pro - Guía de Despliegue

## 📦 Instalación para Usuarios

### Opción 1: Instalación Rápida (Recomendada)

```bash
# 1. Instalar SuperClaude Pro
pip install superclaude-pro

# 2. Ejecutar el instalador
superclaude-pro install

# 3. Reiniciar Claude Code
# ¡Listo! Ya puedes usar los comandos /sc:
```

### Opción 2: Desde el Repositorio de GitHub

```bash
# 1. Clonar el repositorio
git clone https://github.com/NUbem000/SuperClaude-Pro.git
cd SuperClaude-Pro

# 2. Instalar
pip install .

# 3. Ejecutar instalador
superclaude-pro install

# 4. Reiniciar Claude Code
```

## 🔧 Configuración Inicial

### 1. Verificar Instalación

```bash
# Comprobar estado
superclaude-pro status
```

Deberías ver:
```
✓ SuperClaude Pro installed
Version: 3.1.0
Profile: quick
Components: commands, personas, mcp, orchestrator
```

### 2. Probar Comandos

En Claude Code:
```
/sc:analyze
```

### 3. Perfiles de Instalación

- **quick** (defecto): Instalación estándar con todo lo esencial
- **minimal**: Solo comandos básicos
- **developer**: Todas las características + herramientas de desarrollo
- **custom**: Selección interactiva de componentes

```bash
# Cambiar perfil
superclaude-pro install --profile developer
```

## 💻 Despliegue para Desarrollo

### 1. Configurar Entorno de Desarrollo

```bash
# Clonar y entrar al directorio
git clone https://github.com/NUbem000/SuperClaude-Pro.git
cd SuperClaude-Pro

# Crear entorno virtual
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Instalar en modo desarrollo
pip install -e ".[dev,docs,telemetry]"

# Instalar pre-commit hooks
pre-commit install
```

### 2. Usando Docker

```bash
# Construir imagen
docker-compose build

# Entorno de desarrollo
docker-compose run dev

# Ejecutar tests
docker-compose run test

# Servir documentación
docker-compose up docs
# Visitar http://localhost:8000
```

### 3. Comandos de Desarrollo

```bash
# Ejecutar tests
make test

# Tests con cobertura
make test-cov

# Linting y formateo
make format
make lint

# Verificar todo antes de commit
make check
```

## 🏢 Despliegue Empresarial

### 1. Instalación Centralizada

```bash
# Crear configuración compartida
sudo mkdir -p /etc/claude
sudo superclaude-pro install --claude-dir /etc/claude --profile developer

# Dar permisos a usuarios
sudo chmod -R 755 /etc/claude
```

### 2. Instalación Offline

```bash
# En máquina con internet:
pip download superclaude-pro -d ./offline-packages

# Copiar a máquina offline y ejecutar:
pip install --no-index --find-links ./offline-packages superclaude-pro
```

### 3. Automatización con Ansible

```yaml
# playbook.yml
---
- name: Deploy SuperClaude Pro
  hosts: workstations
  tasks:
    - name: Install SuperClaude Pro
      pip:
        name: superclaude-pro
        state: latest
    
    - name: Run installer
      command: superclaude-pro install --profile developer
      become_user: "{{ item }}"
      with_items: "{{ users }}"
```

## 🔄 Actualizaciones

### Actualizar a la Última Versión

```bash
# Actualizar el paquete
pip install --upgrade superclaude-pro

# Ejecutar actualización de configuración
superclaude-pro update
```

### Verificar Actualizaciones

```bash
superclaude-pro update --check
```

## 🌐 Publicación en PyPI

### Para Mantenedores

```bash
# 1. Actualizar versión en pyproject.toml
# 2. Actualizar CHANGELOG.md

# 3. Crear tag
git tag -a v3.1.0 -m "Release v3.1.0"
git push origin v3.1.0

# 4. Build y publicación (automático con CI/CD)
# O manual:
python -m build
twine upload dist/*
```

## 🐛 Solución de Problemas

### Comandos no Funcionan

1. **Reiniciar Claude Code completamente**
2. **Verificar instalación**:
   ```bash
   ls ~/.claude/commands/sc/
   cat ~/.claude/CLAUDE.md
   ```

### Errores de Permisos

```bash
# Arreglar permisos
chown -R $USER:$USER ~/.claude
chmod -R 755 ~/.claude
```

### Conflictos con Otras Extensiones

```bash
# Reinstalar solo SuperClaude Pro
superclaude-pro uninstall
superclaude-pro install --force
```

## 📋 Checklist de Despliegue

### Para Usuarios
- [ ] Python 3.8+ instalado
- [ ] Claude Code instalado
- [ ] `pip install superclaude-pro`
- [ ] `superclaude-pro install`
- [ ] Reiniciar Claude Code
- [ ] Probar comando `/sc:analyze`

### Para Desarrolladores
- [ ] Fork del repositorio
- [ ] Clonar localmente
- [ ] Instalar dependencias dev
- [ ] Configurar pre-commit
- [ ] Ejecutar tests
- [ ] Crear rama para cambios

### Para Empresas
- [ ] Evaluar perfil necesario
- [ ] Planificar despliegue
- [ ] Configurar proxy si necesario
- [ ] Crear instalación centralizada
- [ ] Documentar proceso interno
- [ ] Capacitar usuarios

## 📡 Integración con CI/CD

### GitHub Actions

```yaml
# .github/workflows/deploy.yml
name: Deploy SuperClaude Pro
on:
  workflow_dispatch:

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.11'
      - run: |
          pip install superclaude-pro
          superclaude-pro install --profile developer
```

## 📞 Soporte

- **Documentación**: [GitHub Docs](https://github.com/NUbem000/SuperClaude-Pro/tree/main/docs)
- **Issues**: [GitHub Issues](https://github.com/NUbem000/SuperClaude-Pro/issues)
- **Discusiones**: [GitHub Discussions](https://github.com/NUbem000/SuperClaude-Pro/discussions)

---

**¡SuperClaude Pro está listo para potenciar tu experiencia con Claude Code! 🚀**