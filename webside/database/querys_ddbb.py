from .database_connection  import Data_Base  as bbdd
import hashlib

def get_idcheck(user_cod, password): 
    cn = bbdd()
    cr = cn.get_connection()
    t_hashed = hashlib.sha256(password.encode())
    t_password = t_hashed.hexdigest()
    cr.execute("SELECT * FROM USUARIO WHERE user_cod = {} AND password  = '{}' ".format(user_cod, t_password))
    ids = cr.fetchall()
    cn.close_connection()
    return ids
    
