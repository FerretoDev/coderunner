# Funcionalidad Administrativa - CodeRunner

## Descripción

Se ha implementado completamente la **Sección Administrativa** del juego CodeRunner con las siguientes características:

### ✅ Funcionalidades Implementadas

#### 1. Autenticación de Administrador
- Acceso mediante clave secreta (por defecto: `casa`)
- Verificación de credenciales antes de acceder al panel administrativo
- Mensajes de confirmación y error según el resultado

#### 2. Carga de Laberintos
- **Campo de texto** para ingresar la ruta del archivo manualmente
- **Formato soportado**: `.json` únicamente
- **4 Botones de acceso rápido** a laberintos predefinidos:
  - 📁 Laberinto 1 (Fácil) - Diseño clásico con pasillos amplios
  - 📁 Laberinto 2 (Medio) - Diseño en espiral con más desafío
  - 📁 Laberinto 3 (Difícil) - Diseño caótico con múltiples rutas
  - 📁 Laberinto Ejemplo - Laberinto de demostración
- **Validación completa** de la estructura del archivo:
  - Verifica la existencia del archivo
  - Verifica la existencia de la clave `mapa`
  - Valida que el mapa sea una matriz rectangular
  - **Verifica posición inicial del jugador** (`inicio_jugador`)
  - **Verifica posición inicial de la computadora** (`inicio_computadora`)
  - Reporta errores específicos si falta información
- **Búsqueda automática** en `src/data/` para rutas relativas

#### 3. Reinicio del Salón de Fama
- Opción para eliminar todos los registros del Salón de Fama
- **Modal de confirmación** para prevenir eliminaciones accidentales
- Mensajes de éxito tras completar la operación

#### 4. Confirmación de Salida
- Modal de confirmación al seleccionar "Salir" del menú principal
- Previene cierres accidentales de la aplicación

---

## 🎮 Cómo Usar

### Acceder al Panel Administrativo

1. Ejecutar el juego: `python src/main.py`
2. En el menú principal, seleccionar **"Administración"**
3. Ingresar la clave (por defecto: `casa`)
4. Se mostrará el menú administrativo con tres opciones

### Opciones del Menú Administrativo

#### 📁 Cargar Laberinto

1. Hacer clic en **"Cargar Laberinto"**
2. Ingresar la ruta del archivo en el campo de texto
   - Puede ser una ruta relativa (ej: `laberinto1.json`)
   - O una ruta absoluta (ej: `/home/usuario/laberinto.json`)
   - Si la ruta es relativa, el sistema buscará en `src/data/`
3. Usar los **botones de acceso rápido** para cargar laberintos predefinidos:
   - 📁 **Laberinto 1 (Fácil)** - Diseño clásico con pasillos amplios, ideal para principiantes
   - 📁 **Laberinto 2 (Medio)** - Diseño en espiral que requiere estrategia
   - 📁 **Laberinto 3 (Difícil)** - Diseño caótico con múltiples rutas y mayor complejidad
   - 📁 **Laberinto Ejemplo** - Laberinto de demostración para pruebas
4. Presionar **Enter** o hacer clic en **"Cargar"**
5. El sistema validará automáticamente:
   - Que exista el archivo
   - Que sea un archivo JSON válido
   - Que tenga el mapa
   - Que tenga la posición inicial del jugador
   - Que tenga la posición inicial de la computadora
6. Si la validación es exitosa, se mostrará un mensaje de confirmación
7. Si hay errores, se mostrarán los detalles específicos

**Formato del archivo JSON:**
```json
{
  "nombre": "Nombre del laberinto",
  "dificultad": "normal",
  "mapa": [[1, 0, 1], [0, 0, 0], [1, 0, 1]],
  "inicio_jugador": {"col": 1, "fila": 1},
  "inicio_computadora": {"col": 1, "fila": 2},
  "obsequios": [
    {"posicion": [5, 3], "valor": 50}
  ]
}
```

#### 🗑️ Reiniciar Salón de Fama

1. Hacer clic en **"Reiniciar Salón de Fama"**
2. Se mostrará un modal de confirmación
3. Confirmar la acción para eliminar todos los registros
4. Se mostrará un mensaje de éxito

#### ⬅️ Volver al Menú

Regresa al menú principal del juego

---

## 📁 Archivos Modificados/Creados

### Modificados:
- `src/models/administrador.py` - Implementación completa de lógica administrativa
- `src/game/interfaz.py` - Nuevas pantallas: `PantallaMenuAdministrador`, `PantallaCargaLaberinto`, `ModalConfirmacion`
- `src/game/juego.py` - Integración del flujo administrativo y confirmación de salida
- `src/game/__init__.py` - Exportación de nuevas clases

### Creados:
- `src/data/laberintos/` - Carpeta que contiene todos los laberintos
- `src/data/laberintos/laberinto_ejemplo.json` - Archivo de ejemplo para probar la carga
- `test_admin.py` - Script de pruebas unitarias

---

## 🧪 Pruebas

Se incluye un script de pruebas completo en `test_admin.py`:

```bash
python test_admin.py
```

**Pruebas incluidas:**
- ✅ Autenticación correcta e incorrecta
- ✅ Carga de laberinto válido
- ✅ Validación de estructura (detecta archivos inválidos)
- ✅ Reinicio del Salón de Fama

---

## 🔧 Detalles Técnicos

### Clase `Administrador`
**Ubicación:** `src/models/administrador.py`

**Métodos principales:**
- `autenticar(clave: str) -> bool` - Verifica credenciales
- `cargar_laberinto(ruta: str) -> tuple[Laberinto | None, str]` - Carga y valida laberinto
- `reiniciar_salon_fama(salon: SalonFama) -> str` - Elimina todos los registros

### Pantallas Nuevas

#### `PantallaMenuAdministrador`
Menú con tres botones verticales para las opciones administrativas

#### `PantallaCargaLaberinto`
- Campo de texto (`InputTexto`) para ingresar la ruta del archivo
- Botones de acceso rápido a laberintos predefinidos
- Validación y mensajes de error detallados
- Búsqueda inteligente en directorio `src/data/`

#### `ModalConfirmacion`
Modal reutilizable con botones Sí/No para acciones críticas

---

## 📝 Validaciones Implementadas

El sistema valida automáticamente:

1. **Extensión del archivo**: Solo `.json` o `.txt`
2. **Existencia del archivo**: Verifica que el archivo exista
3. **JSON válido**: Parseo correcto del contenido
4. **Estructura mínima requerida:**
   - ✅ Clave `mapa` presente
   - ✅ Mapa no vacío
   - ✅ Posición `inicio_jugador` presente y con formato correcto
   - ✅ Posición `inicio_computadora` presente y con formato correcto

**Mensajes de error específicos:**
- "El archivo no existe"
- "Solo se permiten archivos .json o .txt"
- "El archivo no contiene JSON válido"
- "Falta la clave 'mapa'"
- "Falta la posición inicial del jugador"
- "Falta la posición inicial de la computadora"

---

## 🎯 Ejemplo de Uso

```python
# Crear administrador
from src.models.administrador import Administrador
admin = Administrador("casa")

# Autenticar
if admin.autenticar("casa"):
    print("Acceso concedido")

# Cargar laberinto
laberinto, mensaje = admin.cargar_laberinto("ruta/al/archivo.json")
if laberinto:
    print(f"✓ {mensaje}")
else:
    print(f"✗ {mensaje}")

# Reiniciar salón de fama
from src.models.salon_fama import SalonFama
salon = SalonFama()
resultado = admin.reiniciar_salon_fama(salon)
print(resultado)
```

---

## ⚙️ Configuración

### Cambiar la clave de administrador

Modificar en `src/game/juego.py`, línea ~73:

```python
admin = Administrador("tu_nueva_clave")
```

---

## 🐛 Solución de Problemas

### No encuentra el archivo
- Verificar que la ruta esté correcta
- Para rutas relativas, el archivo debe estar en `src/data/`
- Usar los botones de acceso rápido para cargar archivos predefinidos

### Error al cargar laberinto
- Verificar que el archivo JSON tenga el formato correcto
- Asegurarse de que todas las claves requeridas estén presentes
- Revisar el mensaje de error específico para más detalles

---

## 📦 Dependencias

- `pygame` - Motor gráfico del juego (incluye interfaz de usuario)

**Nota:** Se eliminó la dependencia de `tkinter` para mantener compatibilidad total con pygame.

---

## ✨ Características Adicionales Implementadas

- ✅ Interfaz gráfica consistente con el resto del juego
- ✅ Mensajes visuales claros (éxito, error, advertencia)
- ✅ Navegación intuitiva con teclas Escape y Enter
- ✅ Diseño responsive que se adapta al tamaño de ventana
- ✅ Iconos emoji para mejor UX
- ✅ Confirmaciones para prevenir errores del usuario

---

## 📄 Licencia

Parte del proyecto CodeRunner - Todos los derechos reservados
