from flask import Flask, render_template, request, redirect, session, jsonify
import sqlite3
import os
from datetime import timedelta
import secrets
from datetime import datetime, timedelta
import yagmail
import random
import re
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = "la_clave_secreta"  # Cambiar esto por algo más seguro
app.permanent_session_lifetime = timedelta(minutes=30)

# Configuración para uploads
UPLOAD_FOLDER = 'static/img/profiles'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def Enviar_Correo(Correo, contents="Hola!, Enviamos esta correo con el fin de verificar si fueiste tu el que se registro dentro de nuestro sitio web Eco_chima.  Si fuiste tu?"):
    try:
        Remitente = "eco.chima.dvmat@gmail.com"
        Contra_Rem = "dijslfebycgokoro"

        yag = yagmail.SMTP(Remitente, Contra_Rem)

        yag.send(
            to=Correo,
            subject="Notificación de EcoChima",
            contents=contents
        )
        print("Correo enviado exitosamente")
    except Exception as e:
        print(f"Error al enviar correo: {e}")



"""
PAGINAS
PAGINAS
PAGINAS
"""

@app.route("/")
def PaginaPrincipal():
    return render_template("inicio.html", user=session.get('usuario', 'invitado'), foto=get_user_foto(session.get('usuario')))

@app.route("/Aun-mas-sobre-nosotros")
def SobreNosotros():
    return render_template("SobreNos.html", user=session.get('usuario', 'invitado'), foto=get_user_foto(session.get('usuario')))

@app.route("/Lecturas")
def Lecturas():
    libros = [
        {
            "id": 1,
            "nombre": "Ecologia y Medio Ambiente",
            "sinopsis": "Un libro que explica de manera sencilla que es el medio ambiente y como este se debe de cuidar. Un buen ejemplar para una lectura rápida y concisa.",
            "imagen": "Ecologia_Y_Medio_Ambiente.png",
            "descarga": "https://sinia.minam.gob.pe/sites/default/files/siar-puno/archivos/public/docs/librodeecologiaymedioambiente.pdf"
        },
        {
            "id": 2,
            "nombre": "Ecologia y Medio Ambiente, Enfoque Competencias",
            "sinopsis": "Este libro nos presenta como los organismos vivos interactúan con el medio ambiente. O en mejores palabras, como los seres vivos (incluyendo a humanos) interactuamos entre nosotros para bien o mal.",
            "imagen": "Ecologia_Y_Medio_Ambiente_Enfoque_Competencias.png",
            "descarga": "https://biblioteca.unipac.edu.mx/wp-content/uploads/2016/06/MATERIALBASEECOLOGIAYMEDIOAMBIENTE.compressed.pdf"
        },
        {
            "id": 3,
            "nombre": "Ecologia de Ecosistemas",
            "sinopsis": "Este es un gran libro ya que abarca varios temas, desde los inicios de la ciencia y de la producción del ecosistema.",
            "imagen": "Ecologia_De_Ecosistemas.png",
            "descarga": "https://fcf.unse.edu.ar/wp-content/uploads/2014/07/SD-49-Fundamentos-de-ecologia-Apuntes-de-clase-BARRIONUEVO.pdf"
        },
        {
            "id": 4,
            "nombre": "Ecologia y Observacion",
            "sinopsis": "Este libro es de igual manera uno que abarca distintos puntos de la ecología, teniendo un enfoque mas serio que muchos otros. Cada subtema que abarca es echo con la opinión de varios especialistas. Una lectura más larga, pero más seria.",
            "imagen": "Ecologia_Y_Observacion.png",
            "descarga": "https://lib2.udec.cl/wp-content/uploads/2020/04/Sagarin-Pauchard-2018-completo-OK.pdf"
        },
        {
            "id": 5,
            "nombre": "Laboratorio de Ecologia",
            "sinopsis": "Es un libro que presenta diversos ejercicios para educar y dar concientización sobre el cuidado del medio ambiente.",
            "imagen": "Laboratorio_De_Ecologia.png",
            "descarga": "https://www.epmorelos.umich.mx/assets/files/manual_ecologia.pdf"
        },
        {
            "id": 6,
            "nombre": "Ecologia y Educacion Ambiental",
            "sinopsis": "Un libro diseñado y creado para la reforma de educación ambiental. En este se nos presenta la naturaleza de una forma bella, de como debemos de apreciar esos seres vivos, pues cada uno es muy bello.",
            "imagen": "Ecologia_Y_Educacion_Ambiental.png",
            "descarga": "https://dgep.uas.edu.mx/librosdigitales/6to_SEMESTRE/54_Ecologia_y_Educacion_Ambiental.pdf"
        },
        {
            "id": 7,
            "nombre": "Te cuento mi Ambiente",
            "sinopsis": "Este es un libro que incluye diversos cuentos. No solo infantiles. Este incluye tres apartados, el “A”, diseñado para niños de 6 a 9 años como el “B” el cuál está diseñado para para niños de 9 años, como para jóvenes de 12 años. El ultimo grupo es el “C”, este siendo para jóvenes de 12 a 15 años.",
            "imagen": "Te_Cuento_Mi_Ambiente.png",
            "descarga": "https://www.neuquen.edu.ar/wp-content/uploads/2021/10/Libro-de-cuento-mi-ambiente.pdf"
        },
        {
            "id": 8,
            "nombre": "Medio Ambiente y Desarrollo",
            "sinopsis": "Esta lectura nos presenta diversos puntos de interés, tales como; La temática “Medio ambiente y Desarrollo”, La “Teoría Ecológica” o La revolución de “Mayo del 68”. Este también nos muestra el nacimiento de distintas ramas por los resultados del desarrollo industrial, tales como; El ecologismo.",
            "imagen": "Medio_Ambiente_Y_Desarrollo.png",
            "descarga": "https://biblioteca.clacso.edu.ar/Republica_Dominicana/ccp/20120801053408/medioamb.pdf"
        },
        {
            "id": 9,
            "nombre": "Fundamentos de Ecologia y Ambiente",
            "sinopsis": "Este libro, dicho por sus mismos autores. Es un buen libro para quienes estén empezando en temas ecológicos y el ambiente así mismo, explica los inicios de esta misma desde 1973. Y como este en sus inicios era de interés político como social.",
            "imagen": "Fundamentos_De_Ecologia_Y_Ambiente.png",
            "descarga": "https://ri.unlu.edu.ar/xmlui/bitstream/handle/rediunlu/1367/Ecologia%20y%20ambiente_DIGITAL.pdf?sequence=1&isAllowed=y"
        },
        {
            "id": 10,
            "nombre": "El libro del Reciclaje",
            "sinopsis": "Este libro es perfecto para quienes no saben o tienen conocimientos básicos sobre el reciclaje de residuos ósea basura orgánica e inorgánica. Este libro también explica que son los residuos, clases y que tanto contaminan, yendo desde una simple botella, hasta cantidades grandes de basura.",
            "imagen": "El_Libro_Del_Reciclaje.png",
            "descarga": "https://www.gea21.com/wp-content/uploads/2022/05/Libro-del-reciclaje-Partes-I-y-II.pdf"
        }
    ]

    return render_template("Lecturas.html", libros=libros, user=session.get('usuario', 'invitado'), foto=get_user_foto(session.get('usuario')))

@app.route("/Videos-Educativos")
def Videos():
    return render_template("VideosEducativos.html", user=session.get('usuario', 'invitado'), foto=get_user_foto(session.get('usuario')))

@app.route("/Entrevistas")
def Entrevistas():
    return render_template("Entrevistas.html", user=session.get('usuario', 'invitado'), foto=get_user_foto(session.get('usuario')))

@app.route("/Juegos")
def Juegos():
    return render_template("Juegos.html", user=session.get('usuario', 'invitado'), foto=get_user_foto(session.get('usuario')))

@app.route("/Centros-de-Reciclaje")
def CentrosReciclaje():
    return render_template("CentrosR.html", user=session.get('usuario', 'invitado'), foto=get_user_foto(session.get('usuario')))

@app.route("/Blog-Del-Equipo")
def Blog():
    return render_template("BlogEq.html", user=session.get('usuario', 'invitado'), foto=get_user_foto(session.get('usuario')))

@app.route("/perfil-usuario")
def PerfilUsuario():
    if 'usuario' not in session:
        return redirect('/Inicio-Sesion')
    
    usuario = session['usuario']
    foto = 'PerfilMaterial.png'  # predeterminada
    
    if usuario != 'invitado':
        try:
            conexion = get_db_connection()
            cursor = conexion.cursor()
            cursor.execute("SELECT FotoPerfil FROM Registros WHERE Usuario = ?", (usuario,))
            row = cursor.fetchone()
            if row and row['FotoPerfil']:
                foto = row['FotoPerfil']
        except Exception as e:
            print(f"Error obteniendo foto: {e}")
        finally:
            if 'conexion' in locals():
                conexion.close()
    
    return render_template("perfil_usuario.html", user=usuario, foto=foto)

@app.route("/cerrar-sesion")
def CerrarSesion():
    session.clear()
    return redirect('/')

@app.route("/borrar-cuenta")
def BorrarCuenta():
    if 'usuario' not in session:
        return redirect('/Inicio-Sesion')
    usuario = session['usuario']
    correo = session['correo']
    try:
        Enviar_Correo(correo, "Tu cuenta en EcoChima ha sido eliminada. Si no fuiste tú, contacta con soporte.")
        conexion = get_db_connection()
        cursor = conexion.cursor()
        cursor.execute("DELETE FROM Registros WHERE Usuario = ?", (usuario,))
        conexion.commit()
        session.clear()
        return redirect('/')
    except Exception as e:
        print(e)
        return "Error al borrar cuenta", 500
    finally:
        if conexion:
            conexion.close()

@app.route("/cambiar-usuario", methods=["POST"])
def CambiarUsuario():
    if 'usuario' not in session:
        return {"success": False, "error": "No hay sesión iniciada"}, 401
    
    data = request.get_json()
    nuevoUsuario = data.get("usuario")
    usuarioActual = session['usuario']
    correo = session['correo']
    
    if not nuevoUsuario or len(nuevoUsuario.strip()) == 0:
        return {"success": False, "error": "El nombre de usuario no puede estar vacío"}
    
    conexion = None
    try:
        conexion = get_db_connection()
        cursor = conexion.cursor()
        
        # Verificar que el nuevo usuario no exista
        cursor.execute("SELECT Usuario FROM Registros WHERE Usuario = ? AND Usuario != ?", (nuevoUsuario, usuarioActual))
        if cursor.fetchone():
            return {"success": False, "error": "El nombre de usuario ya existe"}
        
        # Actualizar usuario
        cursor.execute("UPDATE Registros SET Usuario = ? WHERE Usuario = ?", (nuevoUsuario, usuarioActual))
        conexion.commit()
        
        # Actualizar sesión
        session['usuario'] = nuevoUsuario
        
        # Enviar correo
        Enviar_Correo(correo, f"Tu nombre de usuario en EcoChima ha sido actualizado a: {nuevoUsuario}")
        
        return {"success": True, "mensaje": "Nombre de usuario actualizado"}
    except Exception as e:
        print(f"Error al cambiar usuario: {e}")
        return {"success": False, "error": "Error en la base de datos"}
    finally:
        if conexion:
            conexion.close()

@app.route("/cambiar-contraseña", methods=["POST"])
def CambiarContraseña():
    if 'usuario' not in session:
        return {"success": False, "error": "No hay sesión iniciada"}, 401
    
    data = request.get_json()
    nuevaContraseña = data.get("contraseña")
    usuario = session['usuario']
    correo = session['correo']
    
    # Validar contraseña
    if len(nuevaContraseña) < 8 or not re.search(r'[A-Z]', nuevaContraseña) or not re.search(r'\d', nuevaContraseña):
        return {"success": False, "error": "La contraseña debe tener al menos 8 caracteres, incluir al menos un número y una letra mayúscula"}
    
    conexion = None
    try:
        conexion = get_db_connection()
        cursor = conexion.cursor()
        
        # Actualizar contraseña
        cursor.execute("UPDATE Registros SET Contraseña = ? WHERE Usuario = ?", (nuevaContraseña, usuario))
        conexion.commit()
        
        # Enviar correo
        Enviar_Correo(correo, "Tu contraseña en EcoChima ha sido actualizada exitosamente.")
        
        return {"success": True, "mensaje": "Contraseña actualizada"}
    except Exception as e:
        print(f"Error al cambiar contraseña: {e}")
        return {"success": False, "error": "Error en la base de datos"}
    finally:
        if conexion:
            conexion.close()

@app.route("/cambiar-foto", methods=["POST"])
def CambiarFoto():
    if 'usuario' not in session:
        return {"success": False, "error": "No hay sesión iniciada"}, 401
    
    data = request.get_json()
    foto = data.get("foto")
    usuario = session['usuario']
    
    if not foto:
        return {"success": False, "error": "Foto no especificada"}
    
    # Verificar que la foto sea una de las predeterminadas o una ruta válida
    predeterminadas = ['PerfilMaterial.png', 'perfil1.png', 'perfil2.png', 'perfil3.png', 'perfil4.png', 'perfil5.png']
    if foto not in predeterminadas and not foto.startswith('profiles/'):
        return {"success": False, "error": "Foto no válida"}
    
    conexion = None
    try:
        conexion = get_db_connection()
        cursor = conexion.cursor()
        
        # Actualizar foto
        cursor.execute("UPDATE Registros SET FotoPerfil = ? WHERE Usuario = ?", (foto, usuario))
        conexion.commit()
        
        return {"success": True, "mensaje": "Foto de perfil actualizada"}
    except Exception as e:
        print(f"Error al cambiar foto: {e}")
        return {"success": False, "error": "Error en la base de datos"}
    finally:
        if conexion:
            conexion.close()

@app.route("/subir-foto", methods=["POST"])
def SubirFoto():
    if 'usuario' not in session:
        return {"success": False, "error": "No hay sesión iniciada"}, 401
    
    if 'file' not in request.files:
        return {"success": False, "error": "No se encontró el archivo"}
    
    file = request.files['file']
    if file.filename == '':
        return {"success": False, "error": "Archivo no seleccionado"}
    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        # Generar nombre único
        unique_filename = f"{session['usuario']}_{secrets.token_hex(8)}_{filename}"
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
        file.save(filepath)
        
        # Guardar en BD
        foto_path = f"profiles/{unique_filename}"
        usuario = session['usuario']
        
        conexion = None
        try:
            conexion = get_db_connection()
            cursor = conexion.cursor()
            
            cursor.execute("UPDATE Registros SET FotoPerfil = ? WHERE Usuario = ?", (foto_path, usuario))
            conexion.commit()
            
            return {"success": True, "mensaje": "Foto subida exitosamente", "foto": foto_path}
        except Exception as e:
            print(f"Error al subir foto: {e}")
            return {"success": False, "error": "Error en la base de datos"}
        finally:
            if conexion:
                conexion.close()
    else:
        return {"success": False, "error": "Tipo de archivo no permitido"}

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

def get_user_foto(usuario):
    if usuario == 'invitado' or not usuario:
        return 'PerfilMaterial.png'
    try:
        conexion = get_db_connection()
        cursor = conexion.cursor()
        cursor.execute("SELECT FotoPerfil FROM Registros WHERE Usuario = ?", (usuario,))
        row = cursor.fetchone()
        if row and row['FotoPerfil']:
            return row['FotoPerfil']
        else:
            return 'PerfilMaterial.png'
    except Exception as e:
        print(f"Error obteniendo foto: {e}")
        return 'PerfilMaterial.png'
    finally:
        if 'conexion' in locals():
            conexion.close()

@app.route("/Comentarios-Entrevistas")
def ComentariosEntrevistas():
    return render_template("ComentariosEntrevistas.html")

@app.route("/Comentarios-Lecturas")
def ComentariosLecturas():
    return render_template("ComentariosLecturas.html")

@app.route("/Comentarios-Pagina")
def ComentariosPagina():
    return render_template("ComentariosPag.html")

@app.route("/enviar-comentario", methods=["POST"])
def EnviarComentario():
    """
    Procesa el envío de comentarios desde los formularios de comentarios.
    
    Valida que el usuario esté registrado con el correo electrónico proporcionado
    y envía un email con los comentarios a ben208093@gmail.com.
    
    Datos que recibira del formulario:
        - correoElectronico: Correo del usuario registrado
        - comentarios: Diccionario con los comentarios del usuario
    
    Respuestas posibles:
        - {"success": True, "mensaje": "Comentario enviado exitosamente"} código 200
        - {"error": "El correo no está registrado en el sistema"} código 401
        - {"error": "Campos requeridos faltantes"} código 400
        - {"error": "Error al enviar el comentario"} código 500
    """
    try:
        # Obtener datos del formulario
        data = request.get_json()
        correo_usuario = data.get("correoElectronico")
        comentarios = data.get("comentarios", {})
        
        # Validar que se proporcionen los datos requeridos
        if not correo_usuario or not comentarios:
            return {"error": "Campos requeridos faltantes"}, 400
        
        # Conectarse a la base de datos y verificar que el correo esté registrado
        conexion = get_db_connection()
        cursor = conexion.cursor()
        
        cursor.execute("SELECT Usuario FROM Registros WHERE CorreoElectronico = ?", (correo_usuario,))
        usuario_encontrado = cursor.fetchone()
        
        conexion.close()
        
        # Si el correo no está registrado, retornar error
        if not usuario_encontrado:
            return {"error": "El correo no está registrado en el sistema"}, 401
        
        # Construir el contenido del email con los comentarios
        contenido_email = f"<h2>Nuevo Comentario Recibido</h2>\n"
        contenido_email += f"<p><strong>Correo del usuario:</strong> {correo_usuario}</p>\n"
        contenido_email += f"<p><strong>Usuario:</strong> {usuario_encontrado['Usuario']}</p>\n"
        contenido_email += "<h3>Comentarios:</h3>\n"
        
        for campo, valor in comentarios.items():
            # Formatear los nombres de los campos para que sean legibles
            nombre_campo = campo.replace('_', ' ').title()
            contenido_email += f"<p><strong>{nombre_campo}:</strong> {valor}</p>\n"
        
        contenido_email += f"<p><em>Enviado el: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}</em></p>"
        
        # Enviar el correo
        Enviar_Correo("ben208093@gmail.com", contenido_email)
        
        return {"success": True, "mensaje": "Comentario enviado exitosamente"}, 200
        
    except Exception as e:
        print(f"Error al procesar comentario: {type(e).__name__}: {e}")
        return {"error": "Error al enviar el comentario"}, 500

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

    # Validar contraseña
    if len(contraseña) < 8 or not re.search(r'[A-Z]', contraseña) or not re.search(r'\d', contraseña):
        return {"error": "La contraseña debe tener al menos 8 caracteres, incluir al menos un número y una letra mayúscula"}, 400

    conexion = None
    try:
        # Establece conexión con la base de datos
        conexion = get_db_connection()
        cursor = conexion.cursor()
        
        # Log de intento de registro
        print(f"Intentando registrar: usuario= {usuario}, correo= {correo}")
        
        # Inserta el nuevo registro en la tabla Registros
        cursor.execute("INSERT INTO Registros (Usuario, Contraseña, CorreoElectronico, FotoPerfil) VALUES (?, ?, ?, ?)",
                       (usuario, contraseña, correo, 'PerfilMaterial.png'))
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
            Enviar_Correo(correo)

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
        {"nombre": "Plastico PET no. 1", "descripcion": "Se trata del plástico más común empleado en la producción de envases como botellas de refrescos, agua, aceite.",
         "IdeasRec": "Este material tiene la ventaja de ser reciclable para obtener fibras con las que rellenar almohadas o confeccionar alfombras; por tanto, se recomienda introducirlo en el contenedor correspondiente. Asimismo, es reutilizable si está profundamente limpio.", "TiempoDegr": "Entre 500 y 1.000 años en desaparecer en la naturaleza.", 
         "CaracFisc": ["Alta transparencia, ideal para mostrar el contenido.", "Buena barrera contra gases y humedad.", "Ligero y resistente a impactos"], 
         "ProductPop": ["Botellas de agua y refresco", "Envases de alimentos preparados.", "Frascos de medicamentos."], 
         "img": "CatMaterial_PET.png"},

        {"nombre": "Plastico HDPE no. 2", "descripcion": "Se distingue por su mayor grosor y rigidez, lo que le confiere más resistencia tanto al calor como al frío. Se emplea para fabricar botellas de lácteos, garrafas, detergentes, bolsas de plástico",
         "IdeasRec": "Es reciclable y se puede emplear para hacer macetas o contenedores de basura. También es reutilizable si está en óptimas condiciones higiénicas.", "TiempoDegr": "150 años en degradarse.", 
         "CaracFisc": ["Superficie cerosa y opaca", "Flexible- Excelente resistencia química.", "Muy rígido y resistente a impactos."], 
         "ProductPop": ["Envases de detergente y productos de limpieza.", "Jarras de leche y jugo.", "Tuberías de agua y gas"],
         "img": "CatMaterial_HDPE.png"},

        {"nombre": "Plastico PVC no. 3", "descripcion": "Este material, por sus características, es perfecto para la fabricación de botellas de champú y detergentes, juguetes, tuberías, mangueras e incluso envoltorios de alimentos.", 
         "IdeasRec": " A diferencia de los materiales anteriores, no es reciclable y no conviene reutilizarlo.", "TiempoDegr": "100-1000 años", 
         "CaracFisc": ["Puede ser rígido o flexible según los aditivos.", "Alta resistencia al fuego y a la intemperie.", "- Buena durabilidad en aplicaciones de construcción."], 
         "ProductPop": ["Tuberías de drenaje y agua potable.", "Tarjetas bancarias y de identificación.", "Marcos de ventanas y puertas."], 
         "img": "CatMaterial_PVC.png"},

        {"nombre": "Plastico LDPE no. 4", "descripcion": "Destaca por ser un material muy seguro. De ahí que esté presente en envases como botellas de agua, bolsas de supermercado, plásticos para envolver y guantes.",
         "IdeasRec": "Puede ser reciclado, especialmente como bolsa.", "TiempoDegr": "Puede tardar en torno a 150 años en descomponerse.", 
         "CaracFisc": ["Muy flexible y elástico.", "Tacto suave y superficie brillante.", "Baja resistencia térmica, se deforma con el calor."], 
         "ProductPop": ["Bolsas de supermercado y pan", "Películas plásticas para envolver alimentos.", "Botellas exprimibles."], 
         "img": "CatMaterial_LDPE.png"},

        {"nombre": "Plastico PP no. 5", "descripcion": "Es un material resistente al calor y no deja pasar la humedad, grasa o productos químicos. Esta propiedad lo hace idóneo para la fabricación de envases de mantequilla y yogures, así como para pajitas y tapas de botellas.",
         "IdeasRec": " Se puede reutilizar con toda seguridad y, además, permite ser reciclado (peldaños para registros de drenaje, cajas de baterías para automóvil, etc.).", "TiempoDegr": "Puede tardar hasta 500 años en degradarse en la naturaleza.", 
         "CaracFisc": ["- Ligero y translúcido.", "- Buena resistencia al calor, incluso en microondas.", "Duradero"], 
         "ProductPop": ["Tapas de botellas y envases.", "Envases para microondas.", "Pajillas y utensilios reutilizables."], 
         "img": "CatMaterial_PP.png"},

        {"nombre": "Plastico PS no. 6", "descripcion": "Su uso está muy extendido entre las cafeterías y restaurantes de comida rápida porque, concretamente, se encuentra en los envases de las hamburguesas, vasos desechables para bebidas calientes, cubiertos y tarrinas de helado.",
         "IdeasRec": " Hay que tener en cuenta su alto grado de contaminación, por lo que no debe reutilizarse para contener otro alimento. Sin embargo, puede reciclarse porque es indicado para hacer viguetas de plástico o macetas.", "TiempoDegr": "Podría tardar hasta 500 años en desintegrarse totalmente en la naturaleza, convirtiéndose no obstante en microplásticos.", 
         "CaracFisc": ["Frágil y quebradizo en su forma rígida.", "Buena claridad óptica en su versión cristal.", "- Aislante térmico en su forma espumada (unicel)."], 
         "ProductPop": ["Vasos y platos desechables.", "Bandejas para carne y alimentos frescos.", "Carcasas de electrodomésticos pequeños."], 
         "img": "CatMaterial_PS.png"},

        {"nombre": "Otros plasticos no. 7", "descripcion": "Esta categoría es una combinación de diversos plásticos. Está compuesta por el PC (Policarbonato), muy común en botellas de kétchup, biberones, jeringuillas, CDs o DVDs; y también por los nuevos plásticos biodegradables fabricados con almidones vegetales.",
         "IdeasRec": "Estos envases no son reutilizables ni tampoco reciclables, excepto los etiquetados como “PLA”, que al ser biodegradables sirven para obtener compost.", "TiempoDegr": "Un envase puede tardar hasta 1000 años en degradarse en el medio ambiente.", 
         "CaracFisc": ["Puede ser rigido, flexible o facil de moldear.", "PLA es biodegradable.", "Puede ser transparente y resistente a impactos."], 
         "ProductPop": ["PC (Policarbonato): Lentes de seguridad, discos compactos (CD/DVD), visores de cascos.", "ABS: Piezas de LEGO, carcasas de computadoras, partes de automóviles.", "PLA: Envases biodegradables, cubiertos compostables, filamento para impresión 3D."], 
         "img": "CatMaterial_Otros.png"},

######################################################

        {"nombre": "Carton", "descripcion": "El cartón es un material resistente y muy divertido, no tires tus cajas de carton a la basura mejor construye algun Divertido juego con ellas y cuando te aburras, acude a tu centro de reciclaje mas cercano y reciclalas",
         "IdeasRec": "Construir cajas, juguetes, o arte.", "TiempoDegr": "3-6 meses", 
         "CaracFisc": ["Arrugado", "Resistente", "Absorbente"],
         "ProductPop": ["Cajas de cartón", "Cartulina", "Papel corrugado"], 
         "img": "CatMaterial_Carton.png"}, 

        {"nombre": "Cobre", "descripcion": "El cobre aun que es un material dificil de encontrar suelto, vale la pena sacar cantidades significativas de él por su precio en centros de reciclaje.", 
         "IdeasRec": "Crear joyería, cables, o esculturas.", "TiempoDegr": "No se degrada", 
         "CaracFisc": ["Conductivo", "Maleable", "Corrosión verde"], 
         "ProductPop": ["Alambres", "Tuberías", "Monedas"], 
         "img": "CatMaterial_Cobre.png"},

        {"nombre": "Aluminio", "descripcion": "El aluminio podria ser unos de los marteriales mas reutilizables dentro de nuestras casas, el principal re uso de las latas de aluminio son las macetas!, ayuda a la naturaleza y planta algunas plantitas en latas y llevalas al sol", 
         "IdeasRec": "Macetas, utensilios de cocina, o arte.", "TiempoDegr": "200-500 años", 
         "CaracFisc": ["Ligero", "No magnético", "Reflectante"], 
         "ProductPop": ["Latas", "Foil", "Perfiles"], 
         "img": "CatMaterial_Aluminio.png"},

        {"nombre": "Vidrio", "descripcion": "El vidrio es un material que unque un poco peligroso siempre sera mejor vender algun cristal roto en tu centro de recilclaje que tirarlo a la basura y aumentar el riesgo de lesion a otras personas.", 
         "IdeasRec": "Crear jarrones, decoraciones, o reutilizar como frascos.", "TiempoDegr": "Millones de años", 
         "CaracFisc": ["Frágil", "Transparente", "Inerte"], 
         "ProductPop": ["Botellas", "Frascos", "Vidrios planos"], 
         "img": "CatMaterial_Vidrio.png"},

        {"nombre": "Papel", "descripcion": "El papel es un material muy común en nuestras casas, por lo tanto, se acomula considerablemente en nuestras casas lo que lo hace perfecto para irlo a reciclar en algun centro de reciclaje y tener una remoneracion por este.", 
         "IdeasRec": "Crear tarjetas, origami, o compost.", "TiempoDegr": "2-5 meses", 
         "CaracFisc": ["Blanco", "Absorbente", "Fácil de doblar"], 
         "ProductPop": ["Periódicos", "Revistas", "Papel de oficina"], 
         "img": "CatMaterial_Papel.png"},

        {"nombre": "Textiles", "descripcion": "Los textiles viejos como la ropa rota y vieja o algun trapo roto, siguen siendo candidatos a darles una segunda vida util como trapeador o trapo de mesa.", 
         "IdeasRec": "Crear trapos, bolsos, o patchwork.", "TiempoDegr": "1-5 años", 
         "CaracFisc": ["Suave", "Absorbente", "Tejido"], 
         "ProductPop": ["Algodón", "Sintéticos", "Lana"], 
         "img": "CatMaterial_Textil.png"},

        {"nombre": "Desecho electronico", "descripcion": "Es bien sabido que el desecho electronico necesita un trato especial para ser desechado de manera seguro, por lo tanto, lo mejor es llevarlo a algun centro de reciclaje para que le den un trato adecuado.", 
         "IdeasRec": "Reciclar componentes, donar para reparación.", "TiempoDegr": "Varios años", 
         "CaracFisc": ["Eléctrico", "Complejo", "Tóxico"], 
         "ProductPop": ["Teléfonos", "Computadoras", "Baterías"], 
         "img": "CatMaterial_Electr.png"},

        {"nombre": "Baterias / Pilas", "descripcion": "Al igual que el desecho electronico, las baterias y pilas necesitan un trato especial para evitar dañar el ambiente, por lo tanto, lo mejor es llevarlas a algun centro de reciclaje para que le den un trato adecuado.", 
         "IdeasRec": "Reciclar en centros especializados.", "TiempoDegr": "No biodegradable",
         "CaracFisc": ["Químico", "Peligroso", "Energético"], 
         "ProductPop": ["Alcalinas", "Litio", "Plomo-ácido"], 
         "img": "CatMaterial_Pilas.png"},
    ]

    return render_template("Catalogo.html", productos=productos, user=session.get('usuario', 'invitado'), foto=get_user_foto(session.get('usuario')))

@app.route("/Manual-de-Manualidades")
def Manual_de_Manualidades():
    return render_template("ManualManualidades.html", user=session.get('usuario', 'invitado'), foto=get_user_foto(session.get('usuario')))

"""
JUEGOS
JUEGOS
JUEGOS
"""

@app.route("/Recicla-y-Gana")
def Recicla_y_Gana():
    return render_template("AventuraVerde.html")

@app.route("/Eco-Defensor")
def EcoDefensor():
    return render_template("EcoDef.html")

"""
TRIVIA
TRIVIA
TRIVIA
"""

niveles = {
    "facil": [
        {
            "pregunta": "¿De qué color es el contenedor para papel?",
            "opciones": ["Azul", "Verde", "Rojo"],
            "respuesta": "Azul"
        },
        {
            "pregunta": "¿Reciclar ayuda al planeta?",
            "opciones": ["Sí", "No", "A veces"],
            "respuesta": "Sí"
        }
    ],
    "medio": [
        {
            "pregunta": "¿Qué material va en el contenedor amarillo?",
            "opciones": ["Vidrio", "Plástico", "Papel"],
            "respuesta": "Plástico"
        },
        {
            "pregunta": "¿Qué contenedor se usa para el vidrio?",
            "opciones": ["Azul", "Verde", "Amarillo"],
            "respuesta": "Verde"
        }
    ],
    "dificil": [
        {
            "pregunta": "¿Qué significa reducir?",
            "opciones": [
                "Usar menos recursos",
                "Separar basura",
                "Reutilizar objetos"
            ],
            "respuesta": "Usar menos recursos"
        },
        {
            "pregunta": "¿Cuál NO es una de las 3R?",
            "opciones": ["Reducir", "Reciclar", "Reemplazar"],
            "respuesta": "Reemplazar"
        }
    ]
}

@app.route("/Nivel")
def nivel():
    return render_template("TriviaNivel.html")

@app.route("/Trivia", methods=["POST"])
def Trivia():
    nivel = request.form["nivel"]
    preguntas = niveles[nivel]

    puntaje = None

    if "enviado" in request.form:
        puntaje = 0
        for i, p in enumerate(preguntas):
            respuesta = request.form.get(f"pregunta_{i}")
            if respuesta == p["respuesta"]:
                puntaje += 1

    return render_template(
        "Trivia.html",
        preguntas=preguntas,
        nivel=nivel,
        puntaje=puntaje,
        total=len(preguntas)
    )

"""
GUARDIANES
GUARDIANES
GUARDIANES
"""
objetos = [
    {"nombre": "Botella de plástico", "recicla": True},
    {"nombre": "Papel", "recicla": True},
    {"nombre": "Cartón", "recicla": True},
    {"nombre": "Lata", "recicla": True},
    {"nombre": "Vidrio", "recicla": True},
    {"nombre": "Revista", "recicla": True},

    {"nombre": "Pila", "recicla": False},
    {"nombre": "Pañal", "recicla": False},
    {"nombre": "Cáscara de banana", "recicla": False},
    {"nombre": "Restos de comida", "recicla": False},
    {"nombre": "Colilla de cigarro", "recicla": False},
    {"nombre": "Vaso sucio", "recicla": False}
]

@app.route("/Guardianes")
def Guardianes():
    return render_template("Guardianes.html")

@app.route("/objeto")
def obtener_objeto():
    return jsonify(random.choice(objetos))


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
        expiracion = datetime.now() + timedelta(hours=2)  # El token expira en 2 horas
        
        # Almacena el token (en producción, guardar en BD)
        recovery_tokens[token] = {
            "correo": correo,
            "usuario": user["Usuario"],
            "expiracion": expiracion
        }
        
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

@app.route("/obtener-comentarios-blog", methods=["GET"])
def ObtenerComentariosBlog():
    """
    Obtiene todos los comentarios del blog.
    Solo usuarios autenticados pueden ver comentarios.
    """
    if 'usuario' not in session:
        return {"error": "No autenticado"}, 401
    
    conexion = None
    try:
        conexion = get_db_connection()
        cursor = conexion.cursor()
        
        # Obtener todos los comentarios con info del usuario
        cursor.execute("""
            SELECT 
                cb.id,
                cb.usuario,
                cb.comentario,
                cb.fecha,
                r.FotoPerfil
            FROM ComentariosBlog cb
            JOIN Registros r ON cb.usuario = r.Usuario
            ORDER BY cb.fecha DESC
        """)
        
        comentarios = cursor.fetchall()
        
        # Convertir a lista de diccionarios
        comentarios_list = []
        for comentario in comentarios:
            comentarios_list.append({
                'id': comentario['id'],
                'nombre_usuario': comentario['usuario'],
                'comentario': comentario['comentario'],
                'fecha': comentario['fecha'],
                'foto_perfil': f"{request.host_url}static/img/{comentario['FotoPerfil']}" if comentario['FotoPerfil'] else f"{request.host_url}static/img/PerfilMaterial.png"
            })
        
        return jsonify(comentarios_list)
    
    except Exception as e:
        print(f"Error al obtener comentarios: {e}")
        return {"error": "Error al obtener comentarios"}, 500
    finally:
        if conexion:
            conexion.close()

@app.route("/agregar-comentario-blog", methods=["POST"])
def AgregarComentarioBlog():
    """
    Agrega un nuevo comentario al blog.
    Solo usuarios autenticados pueden comentar.
    """
    if 'usuario' not in session:
        return {"error": "No autenticado"}, 401
    
    data = request.get_json()
    comentario = data.get('comentario', '').strip()
    usuario = session['usuario']
    
    # Validaciones
    if not comentario:
        return {"success": False, "error": "El comentario no puede estar vacío"}, 400
    
    if len(comentario) > 5000:
        return {"success": False, "error": "El comentario es demasiado largo (máximo 5000 caracteres)"}, 400
    
    conexion = None
    try:
        conexion = get_db_connection()
        cursor = conexion.cursor()
        
        # Verificar que el usuario existe en la tabla Registros
        cursor.execute("SELECT Usuario FROM Registros WHERE Usuario = ?", (usuario,))
        if not cursor.fetchone():
            return {"success": False, "error": "Usuario no válido"}, 403
        
        # Insertar el comentario
        cursor.execute("""
            INSERT INTO ComentariosBlog (usuario, comentario, fecha)
            VALUES (?, ?, CURRENT_TIMESTAMP)
        """, (usuario, comentario))
        
        conexion.commit()
        
        return {"success": True, "mensaje": "Comentario publicado exitosamente"}
    
    except Exception as e:
        print(f"Error al agregar comentario: {e}")
        return {"success": False, "error": "Error al publicar el comentario"}, 500
    finally:
        if conexion:
            conexion.close()

if __name__ == "__main__":
    #debug=True activa el modo depuracion
    # - muestra errores en la consola/browser

    #Inicia un servidor de prueba y muestra errores si los hay
    # - recarga la appp automaticamente cuando camvbias archivos (util en desarrollo)
    app.run(debug=True)