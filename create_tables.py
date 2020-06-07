import pyodbc
import random
import csv
import datetime

# TRIGGERS ---------------------------------

# Trigger ID tabla SANSANITO
def IdSANSANITO(conn):
    cur = conn.cursor()
    cur.execute("CREATE SEQUENCE SERIE_ID START WITH 1;")
    cur.execute(
        """
            CREATE OR REPLACE TRIGGER SERIE_ID_SANSANO
            BEFORE INSERT ON SANSANITOPOKEMON
            FOR EACH ROW BEGIN
                SELECT SERIE_ID.NEXTVAL
                INTO :new.ID
                FROM dual;
            END;
        """
    )
    cur.commit()

def DeleteSequence(conn):
    cur = conn.cursor()
    cur.execute("DROP TRIGGER SERIE_ID_SANSANO;")
    cur.commit()

# FUNCIONES_AUX ------------------------------

# Transforma el booleano de legendario en 1 o 0
def boolean_to_int(legendary):
    if legendary=="True":
        return 1
    else:
        return 0

# Entrega hora actual
def check_in_pkm():
    time = datetime.datetime.today()
    return time

# Entrega la nueva prioridad cuando se updatea el hp actual
def Priority(conn,id_p,hp_act):
    cur = conn.cursor()
    cur.execute(
        f"""
        SELECT  HP_MAX, STATE FROM SANSANITOPOKEMON WHERE ID = {id_p};
        """
    )
    for x in cur:
        hp_max = x[0]
        state = x[1]
        if state != 'None' :
            new_prio = hp_max - hp_act + 10
        else:
            new_prio = hp_max - hp_act
        #print(new_prio)
    return new_prio

# Entrega la nueva prioridad cuando se update el estado
def Priority_state(conn,id_p,state):
    cur = conn.cursor()
    cur.execute(
        f"""
        SELECT  HP_ACT, HP_MAX FROM SANSANITOPOKEMON WHERE ID = {id_p};
        """
    )
    for x in cur:
        hp_act = x[0]
        hp_max = x[1]
        if state != 'None' :
            new_prio = hp_max - hp_act + 10
        else:
            new_prio = hp_max - hp_act
        #print(new_prio)
    return new_prio

# Busca en POYO segun el nombre del pkm
def Search_POYO(conn, name):
    cur = conn.cursor()
    cur.execute(
        f"""
        SELECT * FROM POYO WHERE POKEMON_NAME = {name};
        """
    )
    cur.commit()
    for x in cur:
        #print(x)
        return x
    

# BORRAR -------------------------------------

# Borra la tabla POYO
def delete_POYO(conn):
    cur = conn.cursor()
    cur.execute(
        "DROP TABLE POYO")
    cur.commit()

# Borra la tabla SANSANITO
def delete_SANSANITO_POKE(conn):
    cur = conn.cursor()
    cur.execute(
        "DROP TABLE SANSANITOPOKEMON")
    cur.commit()

# CREAR TABLAS --------------------------------

# Crea la tabla poyo
def create_POYO(conn):
    cur = conn.cursor()
    cur.execute(
        """
    	CREATE TABLE POYO(
            POKEDEX_ID INTEGER NOT NULL,
            POKEMON_NAME VARCHAR2(25) NOT NULL,
            POKEMON_TYPE_1 VARCHAR(25) NOT NULL,
            POKEMON_TYPE_2 VARCHAR(25),
            MAX_HP INTEGER NOT NULL,
            LEGENDARY INTEGER NOT NULL);    
        """
        )
    cur.commit()

# Crea la tabla SANSANITO POKEMON
def create_SANSANITO_POKE(conn):
    cur = conn.cursor()
    cur.execute(
        """
        CREATE TABLE SANSANITOPOKEMON(
            ID INTEGER NOT NULL,
            N_POKEDEX INTEGER NOT NULL,
            NAME VARCHAR2(20),
            TYPE1 VARCHAR2(20),
            TYPE2 VARCHAR2(20),
            HP_ACT INTEGER NOT NULL,
            HP_MAX INTEGER NOT NULL,
            LEGENDARY INTEGER,
            STATE VARCHAR2(20),
            CHECKIN TIMESTAMP,
            PRIORITY INTEGER);
        """
        )
    cur.commit()


#COMPLETAR TABLA  -----------------------------

# Completa la tabla POYO a partir del csv
def Complete_table_POYO(conn):
    cur = conn.cursor()
    line_count = 0
    with open ('pokemon.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for row in csv_reader:
            if line_count == 0:
                print("Cargando columnas"+","+row[0]+","+row[1]+","+row[2]+","+row[3]+","+row[5]+","+row[12] )
                line_count +=1
            else : 
                #print("ID:" + row[0]+","+row[1]+","+row[2]+","+row[3]+","+row[5]+","+row[12] )
                poke_id = int(row[0])
                name = str(row[1])
                type1 = str(row[2])
                type2 = str(row[3])
                hp = int(row[5])
                legendary = boolean_to_int(row[12])

                print(poke_id,name,type1,type2,hp,legendary)

  
                cur.execute(
                    f"""
                        INSERT INTO POYO (POKEDEX_ID, POKEMON_NAME, POKEMON_TYPE_1, POKEMON_TYPE_2, MAX_HP, LEGENDARY)
                        VALUES ('{poke_id}','{name}','{type1}','{type2}','{hp}','{legendary}');
                    """
                    )
                cur.commit()


#CRUD ----------------------------------------

# Crea un PKM en la tabla Sansanito
def Create(conn):
    cur = conn.cursor()
    print("┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓")
    print("   Escriba el nombre del Pokémon que desea ingresar")
    print("┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛")
    pkm_name = input()
    pkm_name1 = "'"+pkm_name+"'"
    row = Search_POYO(conn,pkm_name1)
    id_pokedex = row[0]
    id_pokedex1 = str(id_pokedex)
    type1 = row[2]
    type2 = row[3]
    hp_max = row[4]
    legendary = row[5]
    date_checkin = check_in_pkm()
    #print(id_pokedex,type1,type2,hp_max,legendary)
    print("┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓")
    print("   Ingrese HP actual del Pokémon, debe ser menor a "+str(hp_max)+":" )
    print("┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛")
    hp_act = input()
    prio = hp_max - int(hp_act)
    print("┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓")
    for s in ["   Seleccione el estado de su Pokémon: ","   1-Envenenado", "   2-Paralizado", "   3-Quemado", "   4-Dormido","   5-Congelado","   6-None"]:
        print(s)
    print("┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛")
    state = int(input())
    if state == 1 :
        state = "Envenenado"
        prio = prio+10
    elif state == 2 :
        state = "Paralizado"
        prio = prio+10
    elif state == 3 :
        state = "Quemado"
        prio = prio+10
    elif state == 4 :
        state = "Dormido"
        prio = prio+10
    elif state == 5 : 
        state = "Congelado"
        prio = prio+10
    else :
        state = "None"
    print("┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓")
    print("   Desea ingresar a "+pkm_name+" ? S/N")
    print("   N° Pokedex:          "+id_pokedex1)
    print("   Tipo 1:              "+type1)
    print("   Tipo 2:              "+str(type2))
    print("   HP Act:              "+str(hp_act))
    print("   HP Max:              "+str(hp_max))
    print("   Legendario:          "+str(legendary))
    print("   Estado:              "+state)
    print("   Checkin:             "+str(date_checkin))
    print("   Prioridad:           "+str(prio))
    print("┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛")
    flag = str(input())
    if flag == "S":
        cur.execute(
            f"""
                INSERT INTO SANSANITOPOKEMON( N_POKEDEX, NAME, TYPE1, 
                TYPE2, HP_ACT, HP_MAX, LEGENDARY, STATE, CHECKIN, PRIORITY)
                VALUES ('{id_pokedex}','{pkm_name}','{type1}','{type2}','{hp_act}',
                '{hp_max}','{legendary}','{state}',LOCALTIMESTAMP,'{prio}');
            """)
        cur.commit()
        print("┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓")
        print("   Pokémon Ingresado con éxito!")
        print("┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛")
        
    else:
        return

# Lee toda la tabla SANSANITO
def Read(conn):
    cur = conn.cursor()
    cur.execute(
        f""" 
            SELECT * FROM SANSANITOPOKEMON ;
        """
    )
    for x in cur :
        print("┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓")
        print("   ID:                  "+str(x[0]))
        print("   N° Pokedex:          "+str(x[1]))
        print("   Nombre:              "+str(x[2]))
        print("   Tipo 1:              "+str(x[3]))
        print("   Tipo 2:              "+str(x[4]))
        print("   HP Act:              "+str(x[5]))
        print("   HP Max:              "+str(x[6]))
        print("   Legendario:          "+str(x[7]))
        print("   Estado:              "+str(x[8]))
        print("   Checkin:             "+str(x[9]))
        print("   Prioridad:           "+str(x[10]))
        print("┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛")

# Updatea informacion en la tabla SANSANITO
def Update(conn):
    cur = conn.cursor()
    flag = 1
    while flag > 0 :
        print("┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓")
        print("   UPDATE MENU ") 
        print("   0- Regresar al Menú principal ")                                       # Arreglar dsp 
        print("   1- Actualizar HP ACTUAL ")
        print("   2- Actualizar ESTADO actual ")
        print("\n")
        print("   Seleccione un opción")
        print("┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛")
        c = int(input())
        if c == 1 :        
            id_p =  int(input("Ingrese ID del Pokémon que desea actualizar el HP ACTUAL"))
            hp_act_new = int(input("\nIngrese nuevo HP ACTUAL: "))  ##debe ser menor al hp max
            prio_new = Priority(conn,id_p,hp_act_new)
            cur.execute(
                f"""
                    UPDATE SANSANITOPOKEMON SET
                    HP_ACT = '{hp_act_new}', PRIORITY = '{prio_new}'
                    WHERE ID = {id_p};
                """
                )
            cur.commit()
            print("┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓")
            print("   Datos actualizados con éxito!")
            print("┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛")
            flag = 1
        elif c == 2 : 
            id_p =  int(input("Ingrese ID del Pokémon que desea actualizar el HP ACTUAL"))
            #print("\nSeleccione el estado de su Pokémon: ")
            print("┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓")
            for s in ["   Seleccione el estado de su Pokémon: ","   1-Envenenado", "   2-Paralizado", "   3-Quemado", "   4-Dormido","   5-Congelado","   6-None"]:
                print(s)
            print("┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛")
            state = int(input())
            if state == 1 :
                state = "Envenenado"
            elif state == 2 :
                state = "Paralizado"
            elif state == 3 :
                state = "Quemado"
            elif state == 4 :
                state = "Dormido"
            elif state == 5 : 
                state = "Congelado"
            else :
                state = "None"
            prio_new = Priority_state(conn,id_p,state)
            cur.execute(
                f"""
                    UPDATE SANSANITOPOKEMON SET
                    STATE = '{state}', PRIORITY = '{prio_new}'
                    WHERE ID = {id_p};
                """
            )
            cur.commit()
            print("┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓")
            print("   Datos actualizados con éxito!")
            print("┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛")
            flag = 1
        else :
            flag = 0

# Deletea
def Delete(conn):
    cur = conn.cursor()
    print("┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓")
    print("   DELETE MENU ")   
    print("   0- Regresar al Menú principal ")                                      # Arreglar dsp 
    print("   1- Eliminar información de un Pokémon ")
    print("   2- Eliminar toda la información de la tabla ")
    print("\n")
    print("   Seleccione un opción")
    print("┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛")
    c = int(input())
    if c == 1 :
        print("┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓")
        print("   Ingrese el ID del Pokemon que desea eliminar")
        print("┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛") 
        id_p = int(input())  
        print("┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓")
        print("   Seguro que desea eliminar este Pokémon? S/N")
        print("┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛")
        check = str(input())
        if check == "S":
            cur.execute(f"DELETE FROM SANSANITOPOKEMON WHERE ID = {id_p};")
            cur.commit()
            print("┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓")
            print("   Pokémon eliminado de la base de datos con éxito!")
            print("┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛")
        else :
            print("┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓")
            print("   Operación cancelada")
            print("┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛")
    else: 
            cur.execute(f"DELETE FROM SANSANITOPOKEMON;")
            cur.commit()
            print("┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓")
            print("   Se ha eliminado todos los registros de la base de datos.")
            print("┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛")


#VIEWS ----------------------------------------

# Vista PKM más antiguo
def View_oldest_pkm(conn):
    cur = conn.cursor()
    cur.execute(
        """
            CREATE OR REPLACE VIEW oldest_pkm AS
                SELECT * FROM (SELECT * FROM SANSANITOPOKEMON ORDER BY CHECKIN ASC) WHERE ROWNUM <= 1
                WITH READ ONLY;
        """
    )
    cur.commit()

# Vista PKM más antiguo
def View_top_ten_highest(conn):
    cur = conn.cursor()
    cur.execute(
        """
            CREATE OR REPLACE VIEW top_ten_h AS
                SELECT * FROM (SELECT * FROM SANSANITOPOKEMON ORDER BY PRIORITY DESC) WHERE ROWNUM <= 10
                WITH READ ONLY;
        """
    )
    cur.commit()

# Vista PKM más antiguo
def View_top_ten_lowest(conn):
    cur = conn.cursor()
    cur.execute(
        """
            CREATE OR REPLACE VIEW top_ten_l AS
                SELECT * FROM (SELECT * FROM SANSANITOPOKEMON ORDER BY PRIORITY ASC) WHERE ROWNUM <= 10
                WITH READ ONLY;
        """
    )
    cur.commit()

def View_all_legendary(conn):
    cur = conn.cursor()
    cur.execute(
        """
            CREATE OR REPLACE VIEW all_legendary AS
                SELECT * FROM (SELECT * FROM SANSANITOPOKEMON WHERE LEGENDARY = 1)
            WITH READ ONLY;
        """
    )

def View_all_state(conn,state):
    cur = conn.cursor()
    cur.execute(
        f"""
            CREATE OR REPLACE VIEW all_state AS
                SELECT * FROM (SELECT * FROM SANSANITOPOKEMON WHERE STATE = '{state}')
            WITH READ ONLY;
        """
    )


# 
def View_all_pkm_prio(conn):
    cur = conn.cursor()
    cur.execute(
        """
            CREATE OR REPLACE VIEW all_prio AS
                SELECT * FROM (SELECT NAME, HP_ACT, HP_MAX, PRIORITY FROM SANSANITOPOKEMON ORDER BY PRIORITY DESC) 
                WITH READ ONLY;
        """
    )
    cur.commit()

#┏━━━━━━━━━━━━━━━┓

#┗━━━━━━━━━━━━━━━┛

    

"""    
print("┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓")
print("   1- Buscar todos los datos de un Pokémon")
print("┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛")
 """



connect_string = "DRIVER={Oracle en OraDB18Home3};DBQ=localhost:1521;Uid=SYSTEM;Pwd=Base1234"

# Connect string format: [username]/[password]@//[hostname]:[port]/[DB service name]
conn = pyodbc.connect(connect_string)

#delete_SANSANITO_POKE(conn)
#create_POYO(conn)
#create_SANSANITO_POKE(conn)

#Complete_table_POYO(conn)



#DeleteSequence(conn)
#IdSANSANITO(conn)
#Create(conn)
#Read(conn)
#Delete(conn)

#View_oldest_pkm(conn)
#View_top_ten_highest(conn)
#View_top_ten_lowest(conn)
#View_all_legendary(conn)
#View_all_state(conn,"Quemado")
View_all_pkm_prio(conn)
#Priority(conn,2,20)

#Update(conn)