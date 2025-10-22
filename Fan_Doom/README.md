# Fan-Doom: Red Social para Fandoms

Fan-Doom es una red social que fusiona características de plataformas como Reddit y Wikipedia, diseñada para que los usuarios puedan crear, compartir y discutir contenido sobre sus fandoms favoritos. El proyecto está construido con Django y sigue una arquitectura robusta para facilitar su mantenimiento y escalabilidad.

## Tabla de Contenidos
1. [Features](#features)
2. [Tecnologías Utilizadas](#tecnologías-utilizadas)
3. [Prerrequisitos](#prerrequisitos)
4. [Instalación y Configuración](#instalación-y-configuración)
5. [Estructura del Proyecto](#estructura-del-proyecto)
6. [Modelos de la Base de Datos](#modelos-de-la-base-de-datos)
7. [Rutas y Endpoints](#rutas-y-endpoints)
8. [Ejecutar Pruebas](#ejecutar-pruebas)
9. [Contribuciones](#contribuciones)
10. [Licencia](#licencia)

## Features

- **Autenticación de Usuarios**: Registro, inicio de sesión y gestión de perfiles de usuario.
- **Perfiles Personalizables**: Los usuarios pueden editar su biografía y cambiar sus imágenes de perfil y de portada.
- **Sistema de Autores y Obras**: Los usuarios con rol de "autor" pueden registrar sus obras (libros, series, etc.) y publicarlas en la plataforma.
- **Publicaciones (Posts)**: Creación de posts con título, contenido de texto, e imágenes, asociados a una obra específica.
- **Sistema de Votos**: Los usuarios pueden votar a favor o en contra de las publicaciones.
- **Comentarios**: Hilos de discusión en cada publicación.
- **Sistema de Seguimiento**: Los usuarios pueden seguir a sus autores y obras favoritas para ver su contenido.
- **Páginas de Wiki**: Contenido estático para describir fandoms (funcionalidad básica).

## Tecnologías Utilizadas

- **Backend**: Django 5.2.7
- **Base de Datos**: SQLite3 (por defecto para desarrollo)
- **Frontend**: HTML, CSS, JavaScript
- **Gestión de Paquetes**: pip

## Prerrequisitos

- Python 3.10 o superior
- `pip` (gestor de paquetes de Python)
- `venv` (para la gestión de entornos virtuales)

## Instalación y Configuración

Sigue estos pasos para configurar el entorno de desarrollo local.

1.  **Clonar el repositorio**:
    ```bash
    git clone https://github.com/tu-usuario/Fan-Doom-red-social-.git
    cd Fan-Doom-red-social-
    ```

2.  **Navegar al directorio del proyecto Django**:
    ```bash
    cd Fan_Doom
    ```

3.  **Crear y activar el entorno virtual**:
    *   Dentro del directorio `Fan_Doom`, crea el entorno:
        ```bash
        python -m venv venv
        ```
    *   Actívalo:
        -   **Linux/macOS**: `source venv/bin/activate`
        -   **Windows**: `venv\Scripts\activate`

4.  **Instalar dependencias**:
    Asegúrate de estar en el directorio raíz del repositorio (`Fan-Doom-red-social-`) donde se encuentra `requirements.txt`.
    ```bash
    pip install -r requirements.txt
    ```

5.  **Aplicar migraciones de la base de datos**:
    Desde el directorio `Fan_Doom` (donde está `manage.py`):
    ```bash
    python manage.py migrate
    ```

6.  **Iniciar el servidor de desarrollo**:
    ```bash
    python manage.py runserver
    ```
    La aplicación estará disponible en `http://127.0.0.1:8000/`.

## Estructura del Proyecto

```
Fan-Doom-red-social-/
├── Fan_Doom/               # Contenedor del proyecto Django
│   ├── core/               # App principal de la red social
│   │   ├── migrations/
│   │   ├── static/
│   │   ├── templates/
│   │   ├── admin.py
│   │   ├── apps.py
│   │   ├── forms.py
│   │   ├── models.py       # Define la estructura de la base de datos
│   │   ├── urls.py         # Define las rutas de la app 'core'
│   │   └── views.py        # Lógica de las vistas y páginas
│   ├── fan_doom/           # Configuración del proyecto Django
│   │   ├── settings.py
│   │   └── urls.py         # Rutas principales del proyecto
│   ├── media/              # Archivos subidos por usuarios (imágenes)
│   ├── venv/               # Entorno virtual
│   ├── manage.py           # Utilidad de línea de comandos de Django
│   └── README.md
└── requirements.txt        # Dependencias de Python
```

## Modelos de la Base de Datos

La aplicación `core` define los siguientes modelos en `core/models.py`:

-   `Author`: Representa a un usuario con rol de autor. Vinculado `OneToOne` con el modelo `User` de Django.
-   `Profile`: Almacena información extendida del usuario, como biografía e imágenes de perfil/portada.
-   `Work`: Representa una obra creada por un `Author` (ej. un libro, una saga).
-   `Follow`: Modela la relación de seguimiento entre usuarios (`follower` y `followed`).
-   `WorkFollow`: Modela la relación de seguimiento de un `User` a una `Work`.
-   `Fandom`: Define una categoría de fandom (actualmente no muy integrada).
-   `Post`: La publicación principal. Puede contener texto, una imagen o ser un "re-post" de otro `Post`. Está asociado a un `User` y a una `Work`.
-   `Vote`: Almacena los votos (positivos o negativos) que un `User` da a un `Post`.
-   `Comment`: Comentarios realizados por usuarios en un `Post`.
-   `WikiPage`: Para páginas de contenido estático tipo wiki.

## Rutas y Endpoints

Las rutas principales de la aplicación se definen en `core/urls.py`:

-   `/`: **Home (`home`)** - Página principal, muestra el feed de publicaciones.
-   `/login/`: **Login (`login`)** - Página de inicio de sesión.
-   `/signup/`: **Signup (`signup`)** - Página de registro para nuevos usuarios.
-   `/logout/`: **Logout (`logout`)** - Cierra la sesión del usuario.
-   `/profile/<str:username>/`: **Perfil de Usuario (`profile`)** - Muestra el perfil y las publicaciones de un usuario.
-   `/profile/edit/`: **Editar Perfil (`edit_profile`)** - Formulario para editar el perfil del usuario autenticado.
-   `/author/<str:username>/`: **Perfil de Autor (`author_profile`)** - Muestra el perfil público de un autor y sus obras.
-   `/work/add/`: **Añadir Obra (`add_work`)** - Formulario para que un autor registre una nueva obra.
-   `/work/<int:work_id>/edit/`: **Editar Obra (`edit_work`)** - Formulario para editar una obra existente.
-   `/post/<int:post_id>/`: **Detalle de Post (`post_detail`)** - Muestra una publicación y sus comentarios.
-   `/vote/`: **Votar (`vote`)** - Endpoint (solo POST) para registrar un voto en una publicación.
-   `/follow_author/`: **Seguir Autor (`follow_author`)** - Endpoint (solo POST) para seguir a un autor.
-   `/follow_work/`: **Seguir Obra (`follow_work`)** - Endpoint (solo POST) para seguir una obra.

## Ejecutar Pruebas

Para ejecutar el conjunto de pruebas básicas del proyecto, utiliza el siguiente comando desde el directorio `Fan_Doom`:

```bash
python manage.py test core
```

## Contribuciones

Las contribuciones son bienvenidas. Por favor, siéntete libre de enviar un *pull request* o abrir un *issue* para cualquier sugerencia o mejora.

## Licencia

Este proyecto está bajo la Licencia MIT. Consulta el archivo `LICENSE` para más detalles.
