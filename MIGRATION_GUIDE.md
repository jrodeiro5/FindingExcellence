# 🔄 Guía de Migración a Entorno Virtual

## ¿Por qué migrar a venv?

**Problema actual:** Al trabajar sin entorno virtual, las versiones de librerías instaladas globalmente pueden:
- Cambiar sin aviso cuando instalas otras aplicaciones Python
- Crear conflictos entre proyectos
- Causar comportamiento inconsistente entre máquinas
- Hacer que el ejecutable se comporte diferente según la máquina

**Solución:** Entorno virtual aislado con versiones exactas.

## 🚀 Migración Paso a Paso

### 1. Crear Entorno Virtual
```bash
# Opción A: Menu interactivo (recomendado)
dev_menu.bat
# Selecciona opción 1

# Opción B: Directo
setup_venv.bat
```

### 2. Verificar Migración
```bash
# Activar entorno
activate_venv.bat

# Verificar que estás en el venv
python --version
pip list
```

### 3. Crear Ejecutable con venv
```bash
# Opción A: Desde el menu
dev_menu.bat
# Selecciona opción 3

# Opción B: Directo  
build_with_venv.bat
```

## 📁 Archivos Creados

### Nuevos Scripts:
- **`setup_venv.bat`** - Crea entorno virtual inicial
- **`activate_venv.bat`** - Activa entorno para desarrollo  
- **`build_with_venv.bat`** - Build aislado
- **`dev_menu.bat`** - Menu interactivo
- **`requirements_exact.txt`** - Versiones exactas capturadas

### Carpetas:
- **`finding_excellence_env/`** - Entorno virtual (ignorado por git)

## 🛡️ Beneficios del Entorno Aislado

| Sin venv | Con venv |
|----------|----------|
| ❌ Versiones pueden cambiar | ✅ Versiones fijadas |
| ❌ Conflictos entre proyectos | ✅ Completamente aislado |
| ❌ Dependencias globales | ✅ Solo lo necesario |
| ❌ Comportamiento inconsistente | ✅ Reproducible siempre |

## 🔧 Workflow de Desarrollo

### Para desarrollo diario:
1. `activate_venv.bat` o `dev_menu.bat`
2. `python main.py`
3. `deactivate` al terminar

### Para crear ejecutable:
1. `build_with_venv.bat` o `dev_menu.bat` → opción 3
2. Ejecutable en `dist/`

### Para nuevas dependencias:
1. Activar venv: `activate_venv.bat`
2. `pip install nueva_libreria`
3. `pip freeze > build_resources/requirements_venv.txt`

## ⚠️ Migración desde Sistema Actual

Si ya tienes el proyecto funcionando sin venv:

1. **Captura versiones actuales** (el script lo hace automáticamente)
2. **NO elimines** las instalaciones globales (otros proyectos las pueden usar)
3. **Usa el nuevo workflow** para este proyecto

## 🔍 Verificación Post-Migración

Ejecuta el ejecutable creado con venv y verifica que:
- ✅ Las búsquedas se cancelan automáticamente  
- ✅ No hay errores de librerías
- ✅ El comportamiento es consistente

## 🆘 Solución de Problemas

### "Python no encontrado"
```bash
# Verifica instalación
python --version
# Si falla, añade Python al PATH
```

### "No se puede crear venv"
```bash
# Python muy antiguo, actualiza a 3.8+
python -m pip install --upgrade setuptools
```

### "Entorno no se activa"
```bash
# Verifica ruta
dir finding_excellence_env\Scripts\
# Debe existir activate.bat
```

## 📈 Mejores Prácticas

1. **Siempre usa el venv** para este proyecto
2. **No mezcles** instalaciones globales y venv para el mismo proyecto
3. **Actualiza requirements_venv.txt** cuando agregues librerías
4. **Haz backup** del venv antes de cambios grandes

## 🎯 Comandos Rápidos

```bash
# Desarrollo rápido
dev_menu.bat

# Solo ejecutar
activate_venv.bat
python main.py

# Solo build
build_with_venv.bat

# Estado del proyecto  
dev_menu.bat → opción 5
```

---

**¡La migración está lista!** Tu proyecto ahora tiene versiones aisladas y estables. 🎉
