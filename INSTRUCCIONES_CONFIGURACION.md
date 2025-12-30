# Guía de Configuración: Predicciones 2026

Para que el juego funcione y guarde los datos, debes seguir estos pasos:

### 1. Crear el Google Sheet
1. Crea una nueva hoja de cálculo en [Google Sheets](https://sheets.new).
2. Cambia el nombre de la primera pestaña a **`Players`**.
3. En la primera fila (A1), escribe el encabezado: **`Nombre`**.
4. Crea una segunda pestaña llamada **`Predictions`**.
5. No hace falta que pongas encabezados en `Predictions`, la app los creará al guardar la primera vez.

### 2. Obtener las Credenciales
1. Ve a [Google Cloud Console](https://console.cloud.google.com/).
2. Crea un proyecto y habilita la **Google Sheets API**.
3. Crea una **Service Account** y descarga el archivo JSON de llaves.
4. Comparte tu Google Sheet con el email de la Service Account (ej: `tu-sa@proyecto.iam.gserviceaccount.com`) dándole permisos de **Editor**.

### 3. Configurar `.streamlit/secrets.toml`
Copia los datos del JSON en el archivo `.streamlit/secrets.toml` siguiendo este formato:

```toml
[connections.gsheets]
spreadsheet = "URL_DE_TU_GOOGLE_SHEET"
type = "service_account"
project_id = "..."
private_key_id = "..."
private_key = "..."
client_email = "..."
client_id = "..."
auth_uri = "https://accounts.google.com/o/oauth2/auth"
token_uri = "https://oauth2.googleapis.com/token"
auth_provider_x509_cert_url = "https://www.googleapis.com/oauth2/v1/certs"
client_x509_cert_url = "..."
```

### 4. Desplegar en Streamlit.com
Cuando subas el código a GitHub y lo conectes con Streamlit Cloud:
1. Ve a **Settings** -> **Secrets** en el dashboard de Streamlit.
2. Pega el contenido de tu `secrets.toml` allí.

¡Y listo! Ya tendrás persistencia total y gratuita.
