##########################################
#####      CLASE PERSONAJE           #####
##########################################
import sqlite3

class DnDPersonaje:
    def __init__(self):
        self.raza = None
        self.clase = None
        self.guardado = False

    def to_dict(self):
        return {
            "raza": self.raza,
            "clase": self.clase
        }

def save_character_to_db(char_dict):
    conn = sqlite3.connect("./api/bd/dnd.db")
    c = conn.cursor()
    c.execute('''
    INSERT INTO characters (raza, clase) VALUES (?, ?)
''', (
    char_dict["raza"],
    char_dict["clase"]
    ))
    conn.commit()
    conn.close()