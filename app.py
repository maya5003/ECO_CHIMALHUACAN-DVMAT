from flask import Flask, render_template, request, redirect, session
import sqlite3
import os
from datetime import timedelta
import secrets
from datetime import datetime, timedelta
#import yagmail

app = Flask(__name__)
app.secret_key = "tu_clave_secreta_aqui"  # Cambiar esto por algo más seguro
app.permanent_session_lifetime = timedelta(minutes=30)

"""
def Enviar_Correo(Correo):
    Remitente = "eco.chima.dvmat@gmail.com"
    Contra_Rem = "mtshsfjtfagzybnh"

    yag = yagmail.SMTP(Remitente, Contra_Rem)

    yag.send(
        to=Correo,
        subject="Verificacion de correo",
        contents="Hola!, Enviamos esta correo con el fin de verificar si fueiste tu el que se registro dentro de nuestro sitio web Eco_chima.  Si fuiste tu?"
    )
"""

"""
PAGINAS
PAGINAS
PAGINAS
"""

@app.route("/")
def PaginaPrincipal():
    return render_template("inicio.html")

@app.route("/Aun-mas-sobre-nosotros")
def SobreNosotros():
    return render_template("SobreNos.html")

@app.route("/Lecturas")
def Lecturas():
    return render_template("Lecturas.html")

@app.route("/Videos-Educativos")
def Videos():
    return render_template("VideosEducativos.html")

@app.route("/Entrevistas")
def Entrevistas():
    return render_template("Entrevistas.html")

@app.route("/Juegos")
def Juegos():
    return render_template("Juegos.html")

@app.route("/Blog-Del-Equipo")
def Blog():
    return render_template("BlogEq.html")

"""
FORMULARIOS
FORMULARIOS
FORMULARIOS
"""
DB = "EcoChimalhuacan_DVMAT.db"

def get_db_connection():
    conexion = sqlite3.connect(DB, timeout=10.0)
    conexion.row_factory = sqlite3.Row
    return conexion

@app.route("/Comentarios-Entrevistas")
def ComentariosEntrevistas():
    return render_template("ComentariosEntrevistas.html")

@app.route("/Comentarios-Lecturas")
def ComentariosLecturas():
    return render_template("ComentariosLecturas.html")

@app.route("/Comentarios-Pagina")
def ComentariosPagina():
    return render_template("ComentariosPag.html")

@app.route("/Historias-de-Usuarios", methods=["GET"])
def HistoriasUsuariosForm():
    return render_template("HistoriasUsuario.html")

@app.route("/historiasGuardar", methods=["POST"])
def historiasGuardas():
    print("xd")   #Terminar


#Mostrara la plantilla del formulario de registro
@app.route("/Registro", methods=["GET"])
def RegistroForm():
    return render_template("Registro.html")

@app.route("/registrar", methods=["POST"])
def Registrar():
    """
    Procesa el registro de un nuevo usuario.
    
    Valida los datos del formulario, inserta el usuario en la base de datos
    y crea una sesión de usuario.
    
    Datos que recibira del formulario:
        - usuario: Nombre de usuario
        - password: Contraseña del usuario
        - correo: Correo electrónico del usuario
    
    Casos donde las alertas se mostraran:
        - {"success": True, "historial": [], "usuario": <username>} con código 200 si es exitoso
        - {"error": "El correo o usuario ya existe"} con código 400 si hay violación de integridad
        - {"error": "Error en la base de datos"} con código 500 si hay error operacional
        - {"error": "Error: <mensaje>"} con código 500 para otros errores
    """
    # Obtiene los datos del formulario
    data = request.get_json()
    usuario = data.get("usuario")
    contraseña = data.get("password")
    correo = data.get("correo")

    conexion = None
    try:
        # Establece conexión con la base de datos
        conexion = get_db_connection()
        cursor = conexion.cursor()
        
        # Log de intento de registro
        print(f"Intentando registrar: usuario= {usuario}, correo= {correo}")
        
        # Inserta el nuevo registro en la tabla Registros
        cursor.execute("INSERT INTO Registros (Usuario, Contraseña, CorreoElectronico) VALUES (?, ?, ?)",
                       (usuario, contraseña, correo))
        conexion.commit()
        
        print("Registro exitoso")
        
        # Crea la sesión del usuario
        session.permanent = True
        session["usuario"] = usuario
        session["correo"] = correo
        
        # Regres una respuesta exitosa
        return {"success": True, "historial": [], "usuario": usuario}
    
    # Maneja el caso donde usuario o correo ya existen
    except sqlite3.IntegrityError as e:
        print(f"IntegrityError: {e}")
        return {"error": "El correo o usuario ya existe"}, 400
    
    # Maneja errores de operación en la base de datos
    except sqlite3.OperationalError as e:
        print(f"OperationalError: {e}")
        return {"error": "Error en la base de datos"}, 500
    
    # Maneja cualquier otro error inesperado
    except Exception as e:
        print(f"Error inesperado: {type(e).__name__}: {e}")
        return {"error": f"Error: {str(e)}"}, 500
    
    # Cierra la conexión de base de datos
    finally:
        if conexion:
            conexion.close()
            #Envia el correo de verificacion al usuario
            #Enviar_Correo(correo)

#Mostrara la plantilla del formulario de inicio de sesion
@app.route("/Inicio-Sesion", methods=["GET"])
def InicioSesion():
    return render_template("InicioSesion.html")

@app.route("/iniciar-sesion", methods=["POST"])
def IniciarSesion():
    """
    Autentica un usuario y crea una sesión.
    
    Valida las credenciales del usuario contra la base de datos
    y establece una sesión si las credenciales son correctas.
    
    Datos que recibira del formulario:
        - usuario: Nombre de usuario registrado
        - contraseña: Contraseña del usuario
    
    Posibles respuestas (Estas respuestas tendran una alerta dentro del formulario con sweetalert):
        - {"success": True, "usuario": <username>, "mensaje": "Sesión iniciada correctamente"} 
              con código 200 si la autenticación es exitosa
        - {"error": "Usuario y contraseña son requeridos"} con código 400 si faltan datos
        - {"error": "Usuario o contraseña incorrectos"} con código 401 si las credenciales son inválidas
        - {"error": "Error en el servidor"} con código 500 si ocurre un error inesperado
    """
    #Datos del formulario
    data = request.get_json()
    usuario = data.get("usuario")
    contraseña = data.get("contraseña")
    
    # Valida que ambos campos estén presentes
    if not usuario or not contraseña:
        return {"error": "Usuario y contraseña son requeridos"}, 400
    
    conexion = None
    try:
        # Establece conexión con la base de datos
        conexion = get_db_connection()
        cursor = conexion.cursor()
        
        # Busca el usuario con las credenciales proporcionadas
        cursor.execute("SELECT * FROM Registros WHERE Usuario = ? AND Contraseña = ?", 
                       (usuario, contraseña))
        user = cursor.fetchone()
        
        # Si el usuario existe y las credenciales son correctas
        if user:
            # Limpia cualquier sesión anterior
            session.clear()
            
            # Crea una nueva sesión persistente
            session.permanent = True
            session["usuario"] = usuario
            session["correo"] = user["CorreoElectronico"]
            
            # Regresa una respuesta exitosa
            return {"success": True, "usuario": usuario, "mensaje": "Sesión iniciada correctamente"}
        else:
            # En el caso de que las credenciales sean inválidas
            return {"error": "Usuario o contraseña incorrectos"}, 401
    
    # Maneja cualquier error inesperado
    except Exception as e:
        print(f"Error: {type(e).__name__}: {e}")
        return {"error": "Error en el servidor"}, 500
    finally:
        # Cierra la conexión de base de datos
        if conexion:
            conexion.close()

"""
CATALOGO
CATALOGO
CATALOGO
"""

@app.route("/Catalogo")
def Catalogo():
    productos = [
        {"nombre": "Material Educativo 1", "descripcion": "Descripcion del material educativo 1", "img": "CatMaterial_1.jpeg"},
        {"nombre": "Material Educativo 2", "descripcion": "Descripcion del material educativo 2", "img": "CatMaterial_2.jpeg"},
        {"nombre": "Material Educativo 3", "descripcion": "Descripcion del material educativo 3", "img": "CatMaterial_3.jpeg"},
    ]
    return render_template("Catalogo.html", productos=productos)

"""
JUEGOS
JUEGOS
JUEGOS
"""

@app.route("/Aventura-Verde")
def AventuraVerde():
    return render_template("AventuraVerde.html")


"""
MANEJO DE CONTRASEÑA OLVIDADA
MANEJO DE CONTRASEÑA OLVIDADA
MANEJO DE CONTRASEÑA OLVIDADA
"""

# Diccionario temporal para almacenar tokens de recuperación (en producción usar BD)
recovery_tokens = {}

@app.route("/Olvide-Contraseña", methods=["GET"])
def OlvideContraseña():
    """
    Muestra el formulario para recuperar contraseña.
    
    Returns:
        str: Plantilla HTML del formulario de recuperación
    """
    return render_template("OlvideContraseña.html")

@app.route("/solicitar-recuperacion", methods=["POST"])
def SolicitarRecuperacion():
    """
    Genera un token de recuperación y lo envía por correo.
    
    Expected JSON payload:
        - correo (str): Correo electrónico registrado
    
    Returns:
        dict: {"success": True, "mensaje": "Se envió un correo de recuperación"} con código 200
        dict: {"error": "El correo no está registrado"} con código 404
        dict: {"error": "Error en el servidor"} con código 500
    """
    data = request.get_json()
    correo = data.get("correo")
    
    if not correo:
        return {"error": "El correo es requerido"}, 400
    
    conexion = None
    try:
        conexion = get_db_connection()
        cursor = conexion.cursor()
        
        # Verifica que el correo exista en la BD
        cursor.execute("SELECT Usuario FROM Registros WHERE CorreoElectronico = ?", (correo,))
        user = cursor.fetchone()
        
        if not user:
            return {"error": "El correo no está registrado"}, 404
        
        # Genera un token único
        token = secrets.token_urlsafe(32)
        expiracion = datetime.now() + timedelta(hours=1)  # El token expira en 1 hora
        
        # Almacena el token (en producción, guardar en BD)
        recovery_tokens[token] = {
            "correo": correo,
            "usuario": user["Usuario"],
            "expiracion": expiracion
        }
        
        # TODO: Descomenta y configura para enviar correo real
        # Enviar_Correo(correo, token)
        
        print(f"Token de recuperación generado para {correo}: {token}")
        
        return {"success": True, "mensaje": "Se envió un correo de recuperación a tu bandeja de entrada"}
    
    except Exception as e:
        print(f"Error: {type(e).__name__}: {e}")
        return {"error": "Error en el servidor"}, 500
    finally:
        if conexion:
            conexion.close()

@app.route("/recuperar-contraseña/<token>", methods=["GET"])
def ValidarToken(token):
    """
    Valida el token de recuperación y muestra el formulario para nueva contraseña.
    
    Args:
        token (str): Token de recuperación enviado por correo
    
    Returns:
        str: Plantilla HTML con formulario para nueva contraseña
        redirect: Redirige a página de error si el token es inválido
    """
    if token not in recovery_tokens:
        return render_template("ErrorRecuperacion.html", mensaje="Token inválido o expirado")
    
    token_data = recovery_tokens[token]
    
    # Verifica que el token no haya expirado
    if datetime.now() > token_data["expiracion"]:
        del recovery_tokens[token]
        return render_template("ErrorRecuperacion.html", mensaje="El token ha expirado")
    
    return render_template("RestablecerContraseña.html", token=token, usuario=token_data["usuario"])

@app.route("/restablecer-contraseña", methods=["POST"])
def RestablecerContraseña():
    """
    Actualiza la contraseña del usuario con un token válido.
    
    Expected JSON payload:
        - token (str): Token de recuperación
        - nueva_contraseña (str): Nueva contraseña
        - confirmar_contraseña (str): Confirmación de la nueva contraseña
    
    Returns:
        dict: {"success": True, "mensaje": "Contraseña actualizada correctamente"} con código 200
        dict: {"error": "Token inválido o expirado"} con código 401
        dict: {"error": "Las contraseñas no coinciden"} con código 400
        dict: {"error": "Error en el servidor"} con código 500
    """
    data = request.get_json()
    token = data.get("token")
    nueva_contraseña = data.get("nueva_contraseña")
    confirmar_contraseña = data.get("confirmar_contraseña")
    
    # Validaciones
    if not token or token not in recovery_tokens:
        return {"error": "Token inválido o expirado"}, 401
    
    if nueva_contraseña != confirmar_contraseña:
        return {"error": "Las contraseñas no coinciden"}, 400
    
    if len(nueva_contraseña) < 6:
        return {"error": "La contraseña debe tener al menos 6 caracteres"}, 400
    
    token_data = recovery_tokens[token]
    
    # Verifica que el token no haya expirado
    if datetime.now() > token_data["expiracion"]:
        del recovery_tokens[token]
        return {"error": "El token ha expirado"}, 401
    
    conexion = None
    try:
        conexion = get_db_connection()
        cursor = conexion.cursor()
        
        # Actualiza la contraseña en la BD
        cursor.execute("UPDATE Registros SET Contraseña = ? WHERE CorreoElectronico = ?",
                       (nueva_contraseña, token_data["correo"]))
        conexion.commit()
        
        # Elimina el token usado
        del recovery_tokens[token]
        
        print(f"Contraseña actualizada para {token_data['usuario']}")
        
        return {"success": True, "mensaje": "Contraseña actualizada correctamente"}
    
    except Exception as e:
        print(f"Error: {type(e).__name__}: {e}")
        return {"error": "Error en el servidor"}, 500
    finally:
        if conexion:
            conexion.close()

if __name__ == "__main__":
    #debug=True activa el modo depuracion
    # - muestra errores en la consola/browser

    #Inicia un servidor de prueba y muestra errores si los hay
    # - recarga la appp automaticamente cuando camvbias archivos (util en desarrollo)
    app.run(debug=True)