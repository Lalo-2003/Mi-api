from flask import Flask, jsonify, request, send_file, render_template
import mysql.connector


app = Flask(__name__)
from flask_cors import CORS

# Esto habilitará CORS para todas las rutas
CORS(app)


def get_connection():
    return mysql.connector.connect(
        host='35.228.92.221',
        user='lalo',
        password='lalo',
        database='Hospital'
    )

@app.route('/')
def home():
    return jsonify({"message": "Welcome to the Users API!"}), 200
############################################
#Usuarios

# Ruta para obtener todos los usuarios
@app.route('/users', methods=['GET'])
def get_users():
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM users")
        users = cursor.fetchall()
        return jsonify(users), 200
    except mysql.connector.Error as err:
        return jsonify({"error": str(err)}), 500
    finally:
        cursor.close()
        conn.close()


# Ruta para obtener un usuario por ID
@app.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))
        user = cursor.fetchone()
        if user:
            return jsonify(user), 200
        else:
            return jsonify({"error": "User not found"}), 404
    except mysql.connector.Error as err:
        return jsonify({"error": str(err)}), 500
    finally:
        cursor.close()
        conn.close()


# Ruta para crear un nuevo usuario
@app.route('/users', methods=['POST'])
def create_user():
    data = request.json
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO users (id, name_surname, email_user, pass_user, id_status) "
            "VALUES (%s, %s, %s, %s, %s)",
            (data['id'], data['name_surname'], data['email_user'], data['pass_user'], data['id_status'])
        )
        conn.commit()
        return jsonify({"message": "User created successfully"}), 201
    except mysql.connector.Error as err:
        return jsonify({"error": str(err)}), 500
    finally:
        cursor.close()
        conn.close()


# Ruta para actualizar un usuario
@app.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    data = request.json
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE users SET name_surname = %s, email_user = %s, pass_user = %s, id_status = %s WHERE id = %s",
            (data['name_surname'], data['email_user'], data['pass_user'], data['id_status'], user_id)
        )
        conn.commit()
        if cursor.rowcount:
            return jsonify({"message": "User updated successfully"}), 200
        else:
            return jsonify({"error": "User not found"}), 404
    except mysql.connector.Error as err:
        return jsonify({"error": str(err)}), 500
    finally:
        cursor.close()
        conn.close()


# Ruta para eliminar un usuario
@app.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM users WHERE id = %s", (user_id,))
        conn.commit()
        if cursor.rowcount:
            return jsonify({"message": "User deleted successfully"}), 200
        else:
            return jsonify({"error": "User not found"}), 404
    except mysql.connector.Error as err:
        return jsonify({"error": str(err)}), 500
    finally:
        cursor.close()
        conn.close()
############################################################

#Status

# Obtener todos los estados
@app.route('/status', methods=['GET'])
def get_status():
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM status")
        status = cursor.fetchall()
        cursor.close()
        conn.close()
        return jsonify(status), 200
    except mysql.connector.Error as err:
        return jsonify({"error": str(err)}), 500

# Obtener un estado por ID
@app.route('/status/<int:id_status>', methods=['GET'])
def get_status_by_id(id_status):
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM status WHERE id_status = %s", (id_status,))
        status = cursor.fetchone()
        cursor.close()
        conn.close()
        if status:
            return jsonify(status), 200
        else:
            return jsonify({"message": "Estado no encontrado"}), 404
    except mysql.connector.Error as err:
        return jsonify({"error": str(err)}), 500

# Crear un nuevo estado
@app.route('/status', methods=['POST'])
def create_status():
    try:
        new_status = request.get_json()
        id_status = new_status['id_status']
        descripcion_status = new_status['descripcion_status']

        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO status (id_status, descripcion_status) VALUES (%s, %s)",
                       (id_status, descripcion_status))
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({"message": "Estado creado exitosamente"}), 201
    except mysql.connector.Error as err:
        return jsonify({"error": str(err)}), 500

# Actualizar un estado existente
@app.route('/status/<int:id_status>', methods=['PUT'])
def update_status(id_status):
    try:
        updated_status = request.get_json()
        descripcion_status = updated_status['descripcion_status']

        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE status SET descripcion_status = %s WHERE id_status = %s",
                       (descripcion_status, id_status))
        conn.commit()
        cursor.close()
        conn.close()

        if cursor.rowcount > 0:
            return jsonify({"message": "Estado actualizado exitosamente"}), 200
        else:
            return jsonify({"message": "Estado no encontrado"}), 404
    except mysql.connector.Error as err:
        return jsonify({"error": str(err)}), 500

# Eliminar un estado
@app.route('/status/<int:id_status>', methods=['DELETE'])
def delete_status(id_status):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM status WHERE id_status = %s", (id_status,))
        conn.commit()
        cursor.close()
        conn.close()

        if cursor.rowcount > 0:
            return jsonify({"message": "Estado eliminado exitosamente"}), 200
        else:
            return jsonify({"message": "Estado no encontrado"}), 404
    except mysql.connector.Error as err:
        return jsonify({"error": str(err)}), 500

############################################################
#Seguridad

# Obtener todas las entradas de seguridad
@app.route('/seguridad', methods=['GET'])
def get_seguridad():
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM seguridad")
        seguridad = cursor.fetchall()
        cursor.close()
        conn.close()
        return jsonify(seguridad), 200
    except mysql.connector.Error as err:
        return jsonify({"error": str(err)}), 500

# Obtener una entrada de seguridad por ID
@app.route('/seguridad/<int:id_seguridad>', methods=['GET'])
def get_seguridad_by_id(id_seguridad):
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM seguridad WHERE id_seguridad = %s", (id_seguridad,))
        seguridad = cursor.fetchone()
        cursor.close()
        conn.close()
        if seguridad:
            return jsonify(seguridad), 200
        else:
            return jsonify({"message": "Registro no encontrado"}), 404
    except mysql.connector.Error as err:
        return jsonify({"error": str(err)}), 500

# Crear una nueva entrada de seguridad
@app.route('/seguridad', methods=['POST'])
def create_seguridad():
    try:
        new_seguridad = request.get_json()
        id_usuario = new_seguridad['id_usuario']
        token = new_seguridad['token']
        ultimo_login = new_seguridad.get('ultimo_login')
        fecha_modificacion = new_seguridad.get('fecha_modificacion')
        id_usuario_modificacion = new_seguridad.get('id_usuario_modificacion')
        id_status = new_seguridad['id_status']

        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO seguridad (id_usuario, token, ultimo_login, fecha_modificacion, id_usuario_modificacion, id_status)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (id_usuario, token, ultimo_login, fecha_modificacion, id_usuario_modificacion, id_status))
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({"message": "Registro de seguridad creado exitosamente"}), 201
    except mysql.connector.Error as err:
        return jsonify({"error": str(err)}), 500

# Actualizar una entrada de seguridad existente
@app.route('/seguridad/<int:id_seguridad>', methods=['PUT'])
def update_seguridad(id_seguridad):
    try:
        updated_seguridad = request.get_json()
        token = updated_seguridad['token']
        ultimo_login = updated_seguridad.get('ultimo_login')
        fecha_modificacion = updated_seguridad.get('fecha_modificacion')
        id_usuario_modificacion = updated_seguridad.get('id_usuario_modificacion')
        id_status = updated_seguridad['id_status']

        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE seguridad
            SET token = %s, ultimo_login = %s, fecha_modificacion = %s, id_usuario_modificacion = %s, id_status = %s
            WHERE id_seguridad = %s
        """, (token, ultimo_login, fecha_modificacion, id_usuario_modificacion, id_status, id_seguridad))
        conn.commit()
        cursor.close()
        conn.close()

        if cursor.rowcount > 0:
            return jsonify({"message": "Registro de seguridad actualizado exitosamente"}), 200
        else:
            return jsonify({"message": "Registro no encontrado"}), 404
    except mysql.connector.Error as err:
        return jsonify({"error": str(err)}), 500

# Eliminar una entrada de seguridad
@app.route('/seguridad/<int:id_seguridad>', methods=['DELETE'])
def delete_seguridad(id_seguridad):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM seguridad WHERE id_seguridad = %s", (id_seguridad,))
        conn.commit()
        cursor.close()
        conn.close()

        if cursor.rowcount > 0:
            return jsonify({"message": "Registro de seguridad eliminado exitosamente"}), 200
        else:
            return jsonify({"message": "Registro no encontrado"}), 404
    except mysql.connector.Error as err:
        return jsonify({"error": str(err)}), 500


##############################
#relacion usuario perfil

# Obtener todas las relaciones usuario-perfil
@app.route('/relacionusuarioperfil', methods=['GET'])
def get_relacion_usuarios_perfiles():
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM relacionusuarioperfil")
        rows = cursor.fetchall()
        return jsonify(rows), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()

# Obtener una relación usuario-perfil por id_usuario e id_perfil
@app.route('/relacionusuarioperfil/<int:id_usuario>/<int:id_perfil>', methods=['GET'])
def get_relacion_usuario_perfil(id_usuario, id_perfil):
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM relacionusuarioperfil WHERE id_usuario = %s AND id_perfil = %s", (id_usuario, id_perfil))
        row = cursor.fetchone()
        if row:
            return jsonify(row), 200
        else:
            return jsonify({"message": "Relación no encontrada"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()

# Crear una nueva relación usuario-perfil
@app.route('/relacionusuarioperfil', methods=['POST'])
def create_relacion_usuario_perfil():
    try:
        data = request.get_json()
        id_usuario = data['id_usuario']
        id_perfil = data['id_perfil']
        
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO relacionusuarioperfil (id_usuario, id_perfil) VALUES (%s, %s)", (id_usuario, id_perfil))
        conn.commit()
        
        return jsonify({"message": "Relación creada exitosamente"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()

# Actualizar una relación usuario-perfil por id_usuario e id_perfil
@app.route('/relacionusuarioperfil/<int:id_usuario>/<int:id_perfil>', methods=['PUT'])
def update_relacion_usuario_perfil(id_usuario, id_perfil):
    try:
        data = request.get_json()
        # Asumimos que se quieren actualizar todos los valores
        new_id_usuario = data.get('id_usuario', id_usuario)
        new_id_perfil = data.get('id_perfil', id_perfil)
        
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE relacionusuarioperfil
            SET id_usuario = %s, id_perfil = %s
            WHERE id_usuario = %s AND id_perfil = %s
        """, (new_id_usuario, new_id_perfil, id_usuario, id_perfil))
        conn.commit()

        if cursor.rowcount > 0:
            return jsonify({"message": "Relación actualizada exitosamente"}), 200
        else:
            return jsonify({"message": "Relación no encontrada para actualizar"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()

# Eliminar una relación usuario-perfil por id_usuario e id_perfil
@app.route('/relacionusuarioperfil/<int:id_usuario>/<int:id_perfil>', methods=['DELETE'])
def delete_relacion_usuario_perfil(id_usuario, id_perfil):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            DELETE FROM relacionusuarioperfil
            WHERE id_usuario = %s AND id_perfil = %s
        """, (id_usuario, id_perfil))
        conn.commit()

        if cursor.rowcount > 0:
            return jsonify({"message": "Relación eliminada exitosamente"}), 200
        else:
            return jsonify({"message": "Relación no encontrada para eliminar"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()


##################################################
## Perfil

# Obtener todos los perfiles
@app.route('/perfil', methods=['GET'])
def get_perfiles():
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM perfil")
        rows = cursor.fetchall()
        return jsonify(rows), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()

# Obtener un perfil por id_perfil
@app.route('/perfil/<int:id_perfil>', methods=['GET'])
def get_perfil(id_perfil):
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM perfil WHERE id_perfil = %s", (id_perfil,))
        row = cursor.fetchone()
        if row:
            return jsonify(row), 200
        else:
            return jsonify({"message": "Perfil no encontrado"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()

# Crear un nuevo perfil
@app.route('/perfil', methods=['POST'])
def create_perfil():
    try:
        data = request.get_json()
        nombre_perfil = data['nombre_perfil']
        descripcion = data.get('descripcion', '')
        fecha_creacion = data['fecha_creacion']
        id_status = data['id_status']
        
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO perfil (nombre_perfil, descripcion, fecha_creacion, id_status)
            VALUES (%s, %s, %s, %s)
        """, (nombre_perfil, descripcion, fecha_creacion, id_status))
        conn.commit()
        
        return jsonify({"message": "Perfil creado exitosamente"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()

# Actualizar un perfil por id_perfil
@app.route('/perfil/<int:id_perfil>', methods=['PUT'])
def update_perfil(id_perfil):
    try:
        data = request.get_json()
        nombre_perfil = data.get('nombre_perfil')
        descripcion = data.get('descripcion')
        fecha_modificacion = data.get('fecha_modificacion')
        id_usuario_modificacion = data.get('id_usuario_modificacion')
        id_status = data.get('id_status')
        
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE perfil
            SET nombre_perfil = %s, descripcion = %s, fecha_modificacion = %s,
                id_usuario_modificacion = %s, id_status = %s
            WHERE id_perfil = %s
        """, (nombre_perfil, descripcion, fecha_modificacion, id_usuario_modificacion, id_status, id_perfil))
        conn.commit()

        if cursor.rowcount > 0:
            return jsonify({"message": "Perfil actualizado exitosamente"}), 200
        else:
            return jsonify({"message": "Perfil no encontrado para actualizar"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()

# Eliminar un perfil por id_perfil
@app.route('/perfil/<int:id_perfil>', methods=['DELETE'])
def delete_perfil(id_perfil):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM perfil WHERE id_perfil = %s", (id_perfil,))
        conn.commit()

        if cursor.rowcount > 0:
            return jsonify({"message": "Perfil eliminado exitosamente"}), 200
        else:
            return jsonify({"message": "Perfil no encontrado para eliminar"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()


##########################################################33
## Metodo de pago

# Obtener todos los métodos de pago
@app.route('/metodopago', methods=['GET'])
def get_metodos_pago():
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM metodopago")
        rows = cursor.fetchall()
        return jsonify(rows), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()

# Obtener un método de pago por id_metodo_pago
@app.route('/metodopago/<int:id_metodo_pago>', methods=['GET'])
def get_metodo_pago(id_metodo_pago):
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM metodopago WHERE id_metodo_pago = %s", (id_metodo_pago,))
        row = cursor.fetchone()
        if row:
            return jsonify(row), 200
        else:
            return jsonify({"message": "Método de pago no encontrado"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()

# Crear un nuevo método de pago
@app.route('/metodopago', methods=['POST'])
def create_metodo_pago():
    try:
        data = request.get_json()
        nombre_metodo = data['nombre_metodo']
        fecha_modificacion = data.get('fecha_modificacion', None)
        id_usuario_modificacion = data.get('id_usuario_modificacion', None)
        id_status = data['id_status']
        
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO metodopago (nombre_metodo, fecha_modificacion, id_usuario_modificacion, id_status)
            VALUES (%s, %s, %s, %s)
        """, (nombre_metodo, fecha_modificacion, id_usuario_modificacion, id_status))
        conn.commit()
        
        return jsonify({"message": "Método de pago creado exitosamente"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()

# Actualizar un método de pago por id_metodo_pago
@app.route('/metodopago/<int:id_metodo_pago>', methods=['PUT'])
def update_metodo_pago(id_metodo_pago):
    try:
        data = request.get_json()
        nombre_metodo = data.get('nombre_metodo')
        fecha_modificacion = data.get('fecha_modificacion')
        id_usuario_modificacion = data.get('id_usuario_modificacion')
        id_status = data.get('id_status')
        
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE metodopago
            SET nombre_metodo = %s, fecha_modificacion = %s, id_usuario_modificacion = %s, id_status = %s
            WHERE id_metodo_pago = %s
        """, (nombre_metodo, fecha_modificacion, id_usuario_modificacion, id_status, id_metodo_pago))
        conn.commit()

        if cursor.rowcount > 0:
            return jsonify({"message": "Método de pago actualizado exitosamente"}), 200
        else:
            return jsonify({"message": "Método de pago no encontrado para actualizar"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()

# Eliminar un método de pago por id_metodo_pago
@app.route('/metodopago/<int:id_metodo_pago>', methods=['DELETE'])
def delete_metodo_pago(id_metodo_pago):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM metodopago WHERE id_metodo_pago = %s", (id_metodo_pago,))
        conn.commit()

        if cursor.rowcount > 0:
            return jsonify({"message": "Método de pago eliminado exitosamente"}), 200
        else:
            return jsonify({"message": "Método de pago no encontrado para eliminar"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()


######################
#Impuesto

# Obtener todos los impuestos
@app.route('/impuesto', methods=['GET'])
def get_impuestos():
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM impuesto")
        rows = cursor.fetchall()
        return jsonify(rows), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()

# Obtener un impuesto por id_impuesto
@app.route('/impuesto/<int:id_impuesto>', methods=['GET'])
def get_impuesto(id_impuesto):
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM impuesto WHERE id_impuesto = %s", (id_impuesto,))
        row = cursor.fetchone()
        if row:
            return jsonify(row), 200
        else:
            return jsonify({"message": "Impuesto no encontrado"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()

# Crear un nuevo impuesto
@app.route('/impuesto', methods=['POST'])
def create_impuesto():
    try:
        data = request.get_json()
        nombre_impuesto = data['nombre_impuesto']
        porcentaje_impuesto = data['porcentaje_impuesto']
        fecha_modificacion = data.get('fecha_modificacion', None)
        id_usuario_modificacion = data.get('id_usuario_modificacion', None)
        id_status = data['id_status']
        
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO impuesto (nombre_impuesto, porcentaje_impuesto, fecha_modificacion, id_usuario_modificacion, id_status)
            VALUES (%s, %s, %s, %s, %s)
        """, (nombre_impuesto, porcentaje_impuesto, fecha_modificacion, id_usuario_modificacion, id_status))
        conn.commit()
        
        return jsonify({"message": "Impuesto creado exitosamente"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()

# Actualizar un impuesto por id_impuesto
@app.route('/impuesto/<int:id_impuesto>', methods=['PUT'])
def update_impuesto(id_impuesto):
    try:
        data = request.get_json()
        nombre_impuesto = data.get('nombre_impuesto')
        porcentaje_impuesto = data.get('porcentaje_impuesto')
        fecha_modificacion = data.get('fecha_modificacion')
        id_usuario_modificacion = data.get('id_usuario_modificacion')
        id_status = data.get('id_status')
        
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE impuesto
            SET nombre_impuesto = %s, porcentaje_impuesto = %s, fecha_modificacion = %s, id_usuario_modificacion = %s, id_status = %s
            WHERE id_impuesto = %s
        """, (nombre_impuesto, porcentaje_impuesto, fecha_modificacion, id_usuario_modificacion, id_status, id_impuesto))
        conn.commit()

        if cursor.rowcount > 0:
            return jsonify({"message": "Impuesto actualizado exitosamente"}), 200
        else:
            return jsonify({"message": "Impuesto no encontrado para actualizar"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()

# Eliminar un impuesto por id_impuesto
@app.route('/impuesto/<int:id_impuesto>', methods=['DELETE'])
def delete_impuesto(id_impuesto):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM impuesto WHERE id_impuesto = %s", (id_impuesto,))
        conn.commit()

        if cursor.rowcount > 0:
            return jsonify({"message": "Impuesto eliminado exitosamente"}), 200
        else:
            return jsonify({"message": "Impuesto no encontrado para eliminar"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()


#########################################333333
#Factura

# Obtener todas las facturas
@app.route('/factura', methods=['GET'])
def get_facturas():
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM factura")
        rows = cursor.fetchall()
        return jsonify(rows), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()

# Obtener una factura por id_factura
@app.route('/factura/<int:id_factura>', methods=['GET'])
def get_factura(id_factura):
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM factura WHERE id_factura = %s", (id_factura,))
        row = cursor.fetchone()
        if row:
            return jsonify(row), 200
        else:
            return jsonify({"message": "Factura no encontrada"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()

# Crear una nueva factura
@app.route('/factura', methods=['POST'])
def create_factura():
    try:
        data = request.get_json()
        fecha_factura = data['fecha_factura']
        total = data['total']
        estado = data['estado']
        descuento_aplicado = data.get('descuento_aplicado', None)
        descuento_especial = data.get('descuento_especial', None)
        impuestos_aplicados = data.get('impuestos_aplicados', None)
        id_impuesto = data.get('id_impuesto', None)
        id_metodo_pago = data.get('id_metodo_pago', None)
        id_estado = data.get('id_estado', None)
        fecha_modificacion = data.get('fecha_modificacion', None)
        id_usuario_modificacion = data.get('id_usuario_modificacion', None)
        id_status = data['id_status']
        
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO factura (fecha_factura, total, estado, descuento_aplicado, descuento_especial, 
                                 impuestos_aplicados, id_impuesto, id_metodo_pago, id_estado, 
                                 fecha_modificacion, id_usuario_modificacion, id_status)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (fecha_factura, total, estado, descuento_aplicado, descuento_especial, impuestos_aplicados,
              id_impuesto, id_metodo_pago, id_estado, fecha_modificacion, id_usuario_modificacion, id_status))
        conn.commit()
        
        return jsonify({"message": "Factura creada exitosamente"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()

# Actualizar una factura por id_factura
@app.route('/factura/<int:id_factura>', methods=['PUT'])
def update_factura(id_factura):
    try:
        data = request.get_json()
        fecha_factura = data.get('fecha_factura')
        total = data.get('total')
        estado = data.get('estado')
        descuento_aplicado = data.get('descuento_aplicado')
        descuento_especial = data.get('descuento_especial')
        impuestos_aplicados = data.get('impuestos_aplicados')
        id_impuesto = data.get('id_impuesto')
        id_metodo_pago = data.get('id_metodo_pago')
        id_estado = data.get('id_estado')
        fecha_modificacion = data.get('fecha_modificacion')
        id_usuario_modificacion = data.get('id_usuario_modificacion')
        id_status = data.get('id_status')
        
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE factura
            SET fecha_factura = %s, total = %s, estado = %s, descuento_aplicado = %s, descuento_especial = %s, 
                impuestos_aplicados = %s, id_impuesto = %s, id_metodo_pago = %s, id_estado = %s, 
                fecha_modificacion = %s, id_usuario_modificacion = %s, id_status = %s
            WHERE id_factura = %s
        """, (fecha_factura, total, estado, descuento_aplicado, descuento_especial, impuestos_aplicados,
              id_impuesto, id_metodo_pago, id_estado, fecha_modificacion, id_usuario_modificacion, 
              id_status, id_factura))
        conn.commit()

        if cursor.rowcount > 0:
            return jsonify({"message": "Factura actualizada exitosamente"}), 200
        else:
            return jsonify({"message": "Factura no encontrada para actualizar"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()

# Eliminar una factura por id_factura
@app.route('/factura/<int:id_factura>', methods=['DELETE'])
def delete_factura(id_factura):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM factura WHERE id_factura = %s", (id_factura,))
        conn.commit()

        if cursor.rowcount > 0:
            return jsonify({"message": "Factura eliminada exitosamente"}), 200
        else:
            return jsonify({"message": "Factura no encontrada para eliminar"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()

###########################################33
#Estado factura

# Obtener todos los estados de factura
@app.route('/estadofactura', methods=['GET'])
def get_estadofacturas():
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM estadofactura")
        rows = cursor.fetchall()
        return jsonify(rows), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()

# Obtener un estado de factura por id_estado
@app.route('/estadofactura/<int:id_estado>', methods=['GET'])
def get_estadofactura(id_estado):
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM estadofactura WHERE id_estado = %s", (id_estado,))
        row = cursor.fetchone()
        if row:
            return jsonify(row), 200
        else:
            return jsonify({"message": "Estado de factura no encontrado"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()

# Crear un nuevo estado de factura
@app.route('/estadofactura', methods=['POST'])
def create_estadofactura():
    try:
        data = request.get_json()
        descripcion_estado = data['descripcion_estado']
        fecha_modificacion = data.get('fecha_modificacion', None)
        id_usuario_modificacion = data.get('id_usuario_modificacion', None)
        id_status = data['id_status']
        
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO estadofactura (descripcion_estado, fecha_modificacion, 
                                       id_usuario_modificacion, id_status)
            VALUES (%s, %s, %s, %s)
        """, (descripcion_estado, fecha_modificacion, id_usuario_modificacion, id_status))
        conn.commit()
        
        return jsonify({"message": "Estado de factura creado exitosamente"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()

# Actualizar un estado de factura por id_estado
@app.route('/estadofactura/<int:id_estado>', methods=['PUT'])
def update_estadofactura(id_estado):
    try:
        data = request.get_json()
        descripcion_estado = data.get('descripcion_estado')
        fecha_modificacion = data.get('fecha_modificacion')
        id_usuario_modificacion = data.get('id_usuario_modificacion')
        id_status = data.get('id_status')
        
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE estadofactura
            SET descripcion_estado = %s, fecha_modificacion = %s, 
                id_usuario_modificacion = %s, id_status = %s
            WHERE id_estado = %s
        """, (descripcion_estado, fecha_modificacion, id_usuario_modificacion, id_status, id_estado))
        conn.commit()

        if cursor.rowcount > 0:
            return jsonify({"message": "Estado de factura actualizado exitosamente"}), 200
        else:
            return jsonify({"message": "Estado de factura no encontrado para actualizar"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()

# Eliminar un estado de factura por id_estado
@app.route('/estadofactura/<int:id_estado>', methods=['DELETE'])
def delete_estadofactura(id_estado):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM estadofactura WHERE id_estado = %s", (id_estado,))
        conn.commit()

        if cursor.rowcount > 0:
            return jsonify({"message": "Estado de factura eliminado exitosamente"}), 200
        else:
            return jsonify({"message": "Estado de factura no encontrado para eliminar"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()

###############################33333
#empleados

# Obtener todos los empleados
@app.route('/empleado', methods=['GET'])
def get_empleados():
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM empleado")
        rows = cursor.fetchall()
        return jsonify(rows), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()

# Obtener un empleado por id_empleado
@app.route('/empleado/<int:id_empleado>', methods=['GET'])
def get_empleado(id_empleado):
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM empleado WHERE id_empleado = %s", (id_empleado,))
        row = cursor.fetchone()
        if row:
            return jsonify(row), 200
        else:
            return jsonify({"message": "Empleado no encontrado"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()

# Crear un nuevo empleado
@app.route('/empleado', methods=['POST'])
def create_empleado():
    try:
        data = request.get_json()
        nombre_empleado = data['nombre_empleado']
        apellido_empleado = data.get('apellido_empleado', None)
        sexo_empleado = data.get('sexo_empleado', None)
        telefono_empleado = data.get('telefono_empleado', None)
        email_empleado = data.get('email_empleado', None)
        profesion_empleado = data.get('profesion_empleado', None)
        salario_empleado = data.get('salario_empleado', None)
        fecha_contratacion = data.get('fecha_contratacion', None)
        id_usuario_modificacion = data.get('id_usuario_modificacion', None)
        id_status = data['id_status']
        
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO empleado (nombre_empleado, apellido_empleado, sexo_empleado, 
                                  telefono_empleado, email_empleado, profesion_empleado, 
                                  salario_empleado, fecha_contratacion, id_usuario_modificacion, 
                                  id_status)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (nombre_empleado, apellido_empleado, sexo_empleado, telefono_empleado, 
              email_empleado, profesion_empleado, salario_empleado, fecha_contratacion, 
              id_usuario_modificacion, id_status))
        conn.commit()
        
        return jsonify({"message": "Empleado creado exitosamente"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()

# Actualizar un empleado por id_empleado
@app.route('/empleado/<int:id_empleado>', methods=['PUT'])
def update_empleado(id_empleado):
    try:
        data = request.get_json()
        nombre_empleado = data.get('nombre_empleado')
        apellido_empleado = data.get('apellido_empleado')
        sexo_empleado = data.get('sexo_empleado')
        telefono_empleado = data.get('telefono_empleado')
        email_empleado = data.get('email_empleado')
        profesion_empleado = data.get('profesion_empleado')
        salario_empleado = data.get('salario_empleado')
        fecha_contratacion = data.get('fecha_contratacion')
        id_usuario_modificacion = data.get('id_usuario_modificacion')
        id_status = data.get('id_status')

        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE empleado
            SET nombre_empleado = %s, apellido_empleado = %s, sexo_empleado = %s, 
                telefono_empleado = %s, email_empleado = %s, profesion_empleado = %s, 
                salario_empleado = %s, fecha_contratacion = %s, 
                id_usuario_modificacion = %s, id_status = %s
            WHERE id_empleado = %s
        """, (nombre_empleado, apellido_empleado, sexo_empleado, telefono_empleado, 
              email_empleado, profesion_empleado, salario_empleado, fecha_contratacion, 
              id_usuario_modificacion, id_status, id_empleado))
        conn.commit()

        if cursor.rowcount > 0:
            return jsonify({"message": "Empleado actualizado exitosamente"}), 200
        else:
            return jsonify({"message": "Empleado no encontrado para actualizar"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()

# Eliminar un empleado por id_empleado
@app.route('/empleado/<int:id_empleado>', methods=['DELETE'])
def delete_empleado(id_empleado):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM empleado WHERE id_empleado = %s", (id_empleado,))
        conn.commit()

        if cursor.rowcount > 0:
            return jsonify({"message": "Empleado eliminado exitosamente"}), 200
        else:
            return jsonify({"message": "Empleado no encontrado para eliminar"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()

##################################333
#detalle factura

# Obtener todos los detalles de factura
@app.route('/detallefactura', methods=['GET'])
def get_detallefacturas():
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM detallefactura")
        rows = cursor.fetchall()
        return jsonify(rows), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()

# Obtener un detalle de factura por id_detalle
@app.route('/detallefactura/<int:id_detalle>', methods=['GET'])
def get_detallefactura(id_detalle):
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM detallefactura WHERE id_detalle = %s", (id_detalle,))
        row = cursor.fetchone()
        if row:
            return jsonify(row), 200
        else:
            return jsonify({"message": "Detalle de factura no encontrado"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()

# Crear un nuevo detalle de factura
@app.route('/detallefactura', methods=['POST'])
def create_detallefactura():
    try:
        data = request.get_json()
        id_factura = data['id_factura']
        id_medicamento = data.get('id_medicamento', None)
        id_procedimiento_medico = data.get('id_procedimiento_medico', None)
        cantidad = data['cantidad']
        precio_unitario = data['precio_unitario']
        subtotal = data['subtotal']
        id_usuario_modificacion = data.get('id_usuario_modificacion', None)
        id_status = data['id_status']
        
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO detallefactura (id_factura, id_medicamento, id_procedimiento_medico, 
                                       cantidad, precio_unitario, subtotal, id_usuario_modificacion, 
                                       id_status)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """, (id_factura, id_medicamento, id_procedimiento_medico, cantidad, precio_unitario, 
              subtotal, id_usuario_modificacion, id_status))
        conn.commit()
        
        return jsonify({"message": "Detalle de factura creado exitosamente"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()

# Actualizar un detalle de factura por id_detalle
@app.route('/detallefactura/<int:id_detalle>', methods=['PUT'])
def update_detallefactura(id_detalle):
    try:
        data = request.get_json()
        id_factura = data.get('id_factura')
        id_medicamento = data.get('id_medicamento')
        id_procedimiento_medico = data.get('id_procedimiento_medico')
        cantidad = data.get('cantidad')
        precio_unitario = data.get('precio_unitario')
        subtotal = data.get('subtotal')
        id_usuario_modificacion = data.get('id_usuario_modificacion')
        id_status = data.get('id_status')

        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE detallefactura
            SET id_factura = %s, id_medicamento = %s, id_procedimiento_medico = %s, 
                cantidad = %s, precio_unitario = %s, subtotal = %s, 
                id_usuario_modificacion = %s, id_status = %s
            WHERE id_detalle = %s
        """, (id_factura, id_medicamento, id_procedimiento_medico, cantidad, precio_unitario, 
              subtotal, id_usuario_modificacion, id_status, id_detalle))
        conn.commit()

        if cursor.rowcount > 0:
            return jsonify({"message": "Detalle de factura actualizado exitosamente"}), 200
        else:
            return jsonify({"message": "Detalle de factura no encontrado para actualizar"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()

# Eliminar un detalle de factura por id_detalle
@app.route('/detallefactura/<int:id_detalle>', methods=['DELETE'])
def delete_detallefactura(id_detalle):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM detallefactura WHERE id_detalle = %s", (id_detalle,))
        conn.commit()

        if cursor.rowcount > 0:
            return jsonify({"message": "Detalle de factura eliminado exitosamente"}), 200
        else:
            return jsonify({"message": "Detalle de factura no encontrado para eliminar"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()

#####################################3
#Descuento

# Obtener todos los descuentos
@app.route('/descuento', methods=['GET'])
def get_descuentos():
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM descuento")
        rows = cursor.fetchall()
        return jsonify(rows), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()

# Obtener un descuento por id_descuento
@app.route('/descuento/<int:id_descuento>', methods=['GET'])
def get_descuento(id_descuento):
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM descuento WHERE id_descuento = %s", (id_descuento,))
        row = cursor.fetchone()
        if row:
            return jsonify(row), 200
        else:
            return jsonify({"message": "Descuento no encontrado"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()

# Crear un nuevo descuento
@app.route('/descuento', methods=['POST'])
def create_descuento():
    try:
        data = request.get_json()
        nombre_descuento = data['nombre_descuento']
        porcentaje_descuento = data.get('porcentaje_descuento', None)
        id_usuario_modificacion = data.get('id_usuario_modificacion', None)
        id_status = data['id_status']
        
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO descuento (nombre_descuento, porcentaje_descuento, id_usuario_modificacion, id_status)
            VALUES (%s, %s, %s, %s)
        """, (nombre_descuento, porcentaje_descuento, id_usuario_modificacion, id_status))
        conn.commit()
        
        return jsonify({"message": "Descuento creado exitosamente"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()

# Actualizar un descuento por id_descuento
@app.route('/descuento/<int:id_descuento>', methods=['PUT'])
def update_descuento(id_descuento):
    try:
        data = request.get_json()
        nombre_descuento = data.get('nombre_descuento')
        porcentaje_descuento = data.get('porcentaje_descuento')
        id_usuario_modificacion = data.get('id_usuario_modificacion')
        id_status = data.get('id_status')

        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE descuento
            SET nombre_descuento = %s, porcentaje_descuento = %s, 
                id_usuario_modificacion = %s, id_status = %s
            WHERE id_descuento = %s
        """, (nombre_descuento, porcentaje_descuento, id_usuario_modificacion, id_status, id_descuento))
        conn.commit()

        if cursor.rowcount > 0:
            return jsonify({"message": "Descuento actualizado exitosamente"}), 200
        else:
            return jsonify({"message": "Descuento no encontrado para actualizar"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()

# Eliminar un descuento por id_descuento
@app.route('/descuento/<int:id_descuento>', methods=['DELETE'])
def delete_descuento(id_descuento):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM descuento WHERE id_descuento = %s", (id_descuento,))
        conn.commit()

        if cursor.rowcount > 0:
            return jsonify({"message": "Descuento eliminado exitosamente"}), 200
        else:
            return jsonify({"message": "Descuento no encontrado para eliminar"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()

###############################
# #corte de caja

# Obtener todos los cortes de caja
@app.route('/cortedecaja', methods=['GET'])
def get_cortes_de_caja():
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM cortedecaja")
        rows = cursor.fetchall()
        return jsonify(rows), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()

# Obtener un corte de caja por id_corte
@app.route('/cortedecaja/<int:id_corte>', methods=['GET'])
def get_corte_de_caja(id_corte):
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM cortedecaja WHERE id_corte = %s", (id_corte,))
        row = cursor.fetchone()
        if row:
            return jsonify(row), 200
        else:
            return jsonify({"message": "Corte de caja no encontrado"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()

# Crear un nuevo corte de caja
@app.route('/cortedecaja', methods=['POST'])
def create_corte_de_caja():
    try:
        data = request.get_json()
        fecha_corte = data['fecha_corte']
        monto_total = data['monto_total']
        detalles = data.get('detalles', None)
        id_usuario_modificacion = data.get('id_usuario_modificacion', None)
        id_status = data['id_status']
        
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO cortedecaja (fecha_corte, monto_total, detalles, id_usuario_modificacion, id_status)
            VALUES (%s, %s, %s, %s, %s)
        """, (fecha_corte, monto_total, detalles, id_usuario_modificacion, id_status))
        conn.commit()
        
        return jsonify({"message": "Corte de caja creado exitosamente"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()

# Actualizar un corte de caja por id_corte
@app.route('/cortedecaja/<int:id_corte>', methods=['PUT'])
def update_corte_de_caja(id_corte):
    try:
        data = request.get_json()
        fecha_corte = data.get('fecha_corte')
        monto_total = data.get('monto_total')
        detalles = data.get('detalles')
        id_usuario_modificacion = data.get('id_usuario_modificacion')
        id_status = data.get('id_status')

        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE cortedecaja
            SET fecha_corte = %s, monto_total = %s, detalles = %s, 
                id_usuario_modificacion = %s, id_status = %s
            WHERE id_corte = %s
        """, (fecha_corte, monto_total, detalles, id_usuario_modificacion, id_status, id_corte))
        conn.commit()

        if cursor.rowcount > 0:
            return jsonify({"message": "Corte de caja actualizado exitosamente"}), 200
        else:
            return jsonify({"message": "Corte de caja no encontrado para actualizar"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()

# Eliminar un corte de caja por id_corte
@app.route('/cortedecaja/<int:id_corte>', methods=['DELETE'])
def delete_corte_de_caja(id_corte):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM cortedecaja WHERE id_corte = %s", (id_corte,))
        conn.commit()

        if cursor.rowcount > 0:
            return jsonify({"message": "Corte de caja eliminado exitosamente"}), 200
        else:
            return jsonify({"message": "Corte de caja no encontrado para eliminar"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()

if __name__ == '__main__':
    app.run(debug=True)
