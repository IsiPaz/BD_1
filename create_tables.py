import pyodbc
import random
import csv
import datetime


# SEQUENCE ---------------------------------

# Sequence ID
def Create_sequenceID(conn):
    cur = conn.cursor()
    cur.execute("CREATE SEQUENCE SERIE_ID START WITH 1 INCREMENT BY 1;")
    cur.commit()

# Borra la secuencia SERIE_ID
def DeleteSequence(conn):
    cur = conn.cursor()
    cur.execute("DROP SEQUENCE SERIE_ID;")
    cur.commit()

# TRIGGERS ---------------------------------

# Trigger ID tabla SANSANITO
def IdSANSANITO(conn):
    cur = conn.cursor()
    cur.execute( 
        """
            CREATE OR REPLACE TRIGGER SERIE_ID_SANSANO
            BEFORE INSERT ON SANSANITOPokémon
            FOR EACH ROW 
            BEGIN
                SELECT SERIE_ID.NEXTVAL
                INTO :new.ID
                FROM dual;
            END;
        """
    )
    cur.commit()

# Borra el Trigger SERIE_ID_SANSANO
def DeleteTrigger(conn):
    cur = conn.cursor()
    cur.execute("DROP TRIGGER SERIE_ID_SANSANO;")
    cur.commit()

# FUNCIONES_AUX ------------------------------

# Transforma el booleano de legendario en 1 o 0
def Boolean_to_int(legendary):
    if legendary=="True":
        return 1
    else:
        return 0

# Entrega hora actual
def check_in_pkm():
    time = datetime.datetime.today()
    return time

# Retorna la prioridad
def Priority_no_update(hp_act, hp_max, state):
    if state != "None" :
        new_prio = hp_max - hp_act + 10
    else:
        new_prio = hp_max - hp_act
    return new_prio

# Entrega la nueva prioridad cuando se updatea el hp actual en Sansanito
def Priority(conn,id_p,hp_act):
    cur = conn.cursor()
    cur.execute(
        f"""
        SELECT  HP_MAX, STATE FROM SANSANITOPokémon WHERE ID = {id_p};
        """
    )
    for x in cur:
        hp_max = x[0]
        state = x[1]
        prio = Priority_no_update(hp_act,hp_max,state)
        return prio

# Entrega la nueva prioridad cuando se update el estado
def Priority_state(conn,id_p,state):
    cur = conn.cursor()
    cur.execute(
        f"""
        SELECT  HP_ACT, HP_MAX FROM SANSANITOPokémon WHERE ID = {id_p};
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
        SELECT * FROM POYO WHERE Pokémon_NAME = {name};
        """
    )
    cur.commit()
    for x in cur:
        #print(x)
        return x

# Buscar nombre en SANSANITOPokémon
def Search_name(conn, id_p):
    cur = conn.cursor()
    cur.execute(
        f"""
        SELECT NAME FROM SANSANITOPokémon WHERE ID = {id_p};
        """
    )
    cur.commit()
    for x in cur:
        #print(x)
        return x[0]

# Retorna la capacidad de la tabla SANSANITOPokémon
def Count(conn):
    cur = conn.cursor()
    cur.execute(
        f""" 
            SELECT * FROM SANSANITOPokémon ;
        """
    )
    count = 0
    for row in cur:
        count = count + 1
    
    cur.execute(
        f""" 
            SELECT * FROM SANSANITOPokémon WHERE LEGENDARY = 1 ;
        """
    )
    legendary = 0
    for row in cur:
        legendary = legendary + 1
    x = legendary*5
    if x != 0 :
        count = count - 1*legendary
    cap = 50 - x - count
    return cap

# Chequea si el legendario esta solo una vez ingresado
def Check_legendary(conn, name):
    cur.execute(
        f""" 
            SELECT NAME FROM SANSANITOPokémon WHERE LEGENDARY = 1 ;
        """
    )
    for row in cur : 
        if row[0] == name :
            return 1  #esta
    return 0 #no esta, se puede ingresar

# Intercambia el legendario con menos prioridad de la tabla por el que se desea ingresar
def Swap_legendary(conn, name, id0, prio):
    cur.execute(
        f""" 
            SELECT * FROM (SELECT ID, NAME, PRIORITY FROM SANSANITOPokémon WHERE LEGENDARY = 1 ORDER BY PRIORITY ASC) WHERE ROWNUM <= 1;
        """
    )
    dic = {}
    count = 0
    for row in cur :
        dic[count] = row
        count = count + 1
    if len(dic) == 0:
            print("┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓")
            print("   No hay Pokémon legendarios, operación invalida")
            print("┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛")
            input()
            return
    # info pkm leg con menos prioridad en la tabla
    id1 = row[0]
    name1 = row[1]
    prio1 = row[2]
    
    if prio > prio1 :
        cur.execute(f"DELETE FROM SANSANITOPokémon WHERE ID = {id1};")
        print("┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓")
        print("  Se ha eliminado a " +name1+" de la Base de datos")
        print("┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛")
        input()
        return
    else : 
        cur.execute(f"DELETE FROM SANSANITOPokémon WHERE ID = {id0};") 
        print("┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓")
        print("  La operación anterior ha sido invalidada")
        print("  No fue posible agregar a "+name+" por falta de espacio")
        print("┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛")
        input()
        return

# Intercambia un pkm normal por otro de menor prioridad que se encuentre en la tabla SANSANITO
def Swap_normal(conn, name, id0, prio):
    cur.execute(
        f""" 
            SELECT * FROM (SELECT ID, NAME, PRIORITY FROM SANSANITOPokémon WHERE LEGENDARY = 0 ORDER BY PRIORITY ASC) WHERE ROWNUM <= 1;
        """
    )
    for row in cur : 
        id1 = row[0]
        name1 = row[1]
        prio1 = row[2]
    
    if prio > prio1 :
        cur.execute(f"DELETE FROM SANSANITOPokémon WHERE ID = {id1};")
        print("┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓")
        print("  Se ha eliminado a " +name1+" de la Base de datos")
        print("┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛")
        input()
        return
    else : 
        cur.execute(f"DELETE FROM SANSANITOPokémon WHERE ID = {id0};") 
        print("┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓")
        print("  La operación anterior ha sido invalidada")
        print("  No fue posible agregar a "+name+" por falta de espacio")
        print("┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛")
        input()
        return


# Retorna id y prioridad del ultimo pkm ingresado    
def Last_one_pkm(conn):
    cur = conn.cursor()
    cur.execute(
        """
        SELECT * FROM (SELECT ID, PRIORITY FROM SANSANITOPokémon ORDER BY CHECKIN DESC) WHERE ROWNUM <= 1;
        """
    )
    cur.commit()
    for row in cur:
        i = row[0]
        p = row[1]
    return i,p

# BORRAR TABLAS -------------------------------------

# Borra la tabla POYO
def Delete_POYO(conn):
    cur = conn.cursor()
    cur.execute(
        "DROP TABLE POYO")
    cur.commit()

# Borra la tabla SANSANITO
def Delete_SANSANITO_POKE(conn):
    cur = conn.cursor()
    cur.execute(
        "DROP TABLE SANSANITOPokémon")
    cur.commit()

# CREAR TABLAS --------------------------------

# Crea la tabla poyo
def Create_POYO(conn):
    cur = conn.cursor()
    cur.execute(
        """
    	CREATE TABLE POYO(
            POKEDEX_ID INTEGER NOT NULL,
            Pokémon_NAME VARCHAR2(50) NOT NULL,
            Pokémon_TYPE_1 VARCHAR(25) NOT NULL,
            Pokémon_TYPE_2 VARCHAR(25),
            MAX_HP INTEGER NOT NULL,
            LEGENDARY INTEGER NOT NULL)    
        """
        )
    cur.commit()

# Crea la tabla SANSANITO Pokémon
def Create_SANSANITO_POKE(conn):
    cur = conn.cursor()
    cur.execute(
        """
        CREATE TABLE SANSANITOPokémon(
            ID INTEGER NOT NULL,
            N_POKEDEX INTEGER NOT NULL,
            NAME VARCHAR2(50),
            TYPE1 VARCHAR2(25),
            TYPE2 VARCHAR2(25),
            HP_ACT INTEGER NOT NULL,
            HP_MAX INTEGER NOT NULL,
            LEGENDARY INTEGER,
            STATE VARCHAR2(20),
            CHECKIN TIMESTAMP,
            PRIORITY INTEGER)
        """
        )
    cur.commit()

# PRIMARY KEY constraint -----------------------------

# Define la PK en SANSANITO
def PK_Sansanito(conn):
    cur = conn.cursor()
    cur.execute(
        """
        ALTER TABLE SANSANITOPokémon
        ADD CONSTRAINT sansa_pk PRIMARY KEY (ID)
        """
    )
    cur.commit()

# Define la PK en POYO
def PK_Poyo(conn):
    cur = conn.cursor()
    cur.execute(
        """
        ALTER TABLE POYO
        ADD CONSTRAINT poyo_pk PRIMARY KEY (Pokémon_NAME)
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
                #print("Cargando columnas"+","+row[0]+","+row[1]+","+row[2]+","+row[3]+","+row[5]+","+row[12] )
                line_count +=1
            else : 
                #print("ID:" + row[0]+","+row[1]+","+row[2]+","+row[3]+","+row[5]+","+row[12] )
                poke_id = int(row[0])
                name = str(row[1])
                type1 = str(row[2])
                type2 = str(row[3])
                hp = int(row[5])
                legendary = Boolean_to_int(row[12])

                #print(poke_id,name,type1,type2,hp,legendary)

  
                cur.execute(
                    f"""
                        INSERT INTO POYO (POKEDEX_ID, Pokémon_NAME, Pokémon_TYPE_1, Pokémon_TYPE_2, MAX_HP, LEGENDARY)
                        VALUES ('{poke_id}','{name}','{type1}','{type2}','{hp}','{legendary}')
                    """
                    )
                cur.commit()

# Completa la tabla SANSANITO a partir de un número dado
def Complete_table_SANSA(conn):
    cur = conn.cursor()
    print("┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓")
    print("   Ingrese la cantidad máxima de Pokémon que desea agregar: ")
    print("┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛")
    cant = int(input())
    insert = 0
    status = ["Envenenado", "Paralizado", "Quemado", "Dormido","Congelado","None"]
    if cant > 50:
        print("┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓")
        print("   Lo sentimos, la base de datos no soporta más de 50 Pokémon")
        print("┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛")
        return Complete_table_SANSA(conn)
    else:
        while cant > 0:
            n = random.randint(0, 721)
            i = 0
            dic = {}
            c = Count(conn)
            cur.execute(
                f"""
                SELECT * FROM POYO WHERE POKEDEX_ID = '{n}'
                """
            )
            for row in cur:
                lista = [int(row[0]),row[1],row[2],row[3],int(row[4]),int(row[5])]
                dic[i] = lista
                i = i + 1
            i = random.randint(0, i-1)
            lista = dic.get(i)        
            id_pokedex = lista[0]
            pkm_name = lista[1]
            type1 = lista[2]
            type2 = lista[3]
            hp_max = lista[4]
            hp_act = random.randint(0,hp_max)
            legendary = lista[5]
            state = random.choice(status)
            prio = Priority_no_update(hp_act, hp_max, state)
            if 5 > c & c > 0 & legendary == 1:
                cant = cant - 1
            elif 5 > c & c > 0 & legendary != 1:
                cur.execute(
                f"""
                    INSERT INTO SANSANITOPokémon( N_POKEDEX, NAME, TYPE1, 
                    TYPE2, HP_ACT, HP_MAX, LEGENDARY, STATE, CHECKIN, PRIORITY)
                    VALUES ('{id_pokedex}','{pkm_name}','{type1}','{type2}','{hp_act}',
                    '{hp_max}','{legendary}','{state}',LOCALTIMESTAMP,'{prio}')
                """
                )
                cur.commit()
                cant = cant - 1
                insert = insert + 1
            elif c > 5 :
                cur.execute(
                    f"""
                        INSERT INTO SANSANITOPokémon( N_POKEDEX, NAME, TYPE1, 
                        TYPE2, HP_ACT, HP_MAX, LEGENDARY, STATE, CHECKIN, PRIORITY)
                        VALUES ('{id_pokedex}','{pkm_name}','{type1}','{type2}','{hp_act}',
                        '{hp_max}','{legendary}','{state}',LOCALTIMESTAMP,'{prio}')
                    """
                )
                cur.commit()
                cant = cant - 1
                insert = insert + 1
            else :
                print("Error ?")     
    print("┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓")
    print("   Se han ingresado "+str(insert)+" Pokémon")
    print("   en la base de datos con éxito!")
    print("┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛")

#CRUD ----------------------------------------

# Crea un PKM en la tabla Sansanito
def Create(conn, pkm_name):
    cur = conn.cursor()
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
    hp_act = int(input())
    if hp_act > hp_max :
        print("┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓")
        print("   Input invalido" )
        print("┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛")
        return Create(conn, pkm_name)
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
                INSERT INTO SANSANITOPokémon( N_POKEDEX, NAME, TYPE1, 
                TYPE2, HP_ACT, HP_MAX, LEGENDARY, STATE, CHECKIN, PRIORITY)
                VALUES ('{id_pokedex}','{pkm_name}','{type1}','{type2}','{hp_act}',
                '{hp_max}','{legendary}','{state}',LOCALTIMESTAMP,'{prio}')
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
            SELECT * FROM SANSANITOPokémon ;
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
        if c == 0 :
            return
        elif c == 1 :  
            print("┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓")
            print("   Ingrese ID del Pokémon que desea actualizar el HP ACTUAL")
            print("┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛")      
            id_p =  int(input())
            cur.execute(
            f""" 
            SELECT NAME, HP_MAX FROM SANSANITOPokémon WHERE ID = {id_p} ;
            """
            )
            for row in cur:
                name = row[0]
                lim = row[1]
            print("┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓")
            print("   Ingrese nuevo HP ACTUAL de "+name+", debe ser menor a " +str(lim))
            print("┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛")
            hp_act_new = int(input())  ##debe ser menor al hp max
            prio_new = Priority(conn,id_p,hp_act_new)
            cur.execute(
                f"""
                    UPDATE SANSANITOPokémon SET
                    HP_ACT = '{hp_act_new}', PRIORITY = '{prio_new}'
                    WHERE ID = {id_p};
                """
                )
            cur.commit()
            print("┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓")
            print("   Datos de "+name+" actualizados con éxito!")
            print("┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛")
            flag = 1
        elif c == 2 : 
            
            print("┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓")
            print("   Ingrese ID del Pokémon que desea actualizar el ESTADO ACTUAL")
            print("┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛")  
            id_p =  int(input())
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
                    UPDATE SANSANITOPokémon SET
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
    return

# Borra pkm de la tabla SANSANITO
def Delete(conn):
    cur = conn.cursor()
    print("┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓")
    print("   DELETE MENU ")   
    print("   0- Regresar al Menú principal ")                                       
    print("   1- Eliminar información de un Pokémon ")
    print("   2- Eliminar toda la información de la tabla ")
    print("\n")
    print("   Seleccione un opción")
    print("┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛")
    c = int(input())
    if c == 0 :
        return
    elif c == 1 :
        print("┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓")
        print("   Ingrese el ID del Pokémon que desea eliminar")
        print("┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛") 
        id_p = int(input())  
        n = str(Search_name(conn,id_p))
        print("┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓")
        print("   Seguro que desea eliminar a S" +n+ "? S/N")
        print("┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛")
        check = str(input())
        if check == "S" :
            cur.execute(f"DELETE FROM SANSANITOPokémon WHERE ID = {id_p};")
            cur.commit()
            print("┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓")
            print("   Pokémon eliminado de la base de datos con éxito!")
            print("┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛")
            return
        else :
            print("┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓")
            print("   Operación cancelada")
            print("┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛")
            return
    elif c == 2: 
        print("┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓")
        print("   Seguro que desea eliminar toda la información de la tabla? S/N")
        print("┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛")
        check = str(input())
        if check == "S" :
            cur.execute(f"DELETE FROM SANSANITOPokémon;")
            cur.commit()
            print("┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓")
            print("   Se ha eliminado todos los registros de la base de datos.")
            print("┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛")
            return
        else :
            print("┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓")
            print("   Operación cancelada")
            print("┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛")
            return
    else :
        print("retorna al menu principal")
        return

#VIEWS ----------------------------------------

# Vista PKM más antiguo
def View_oldest_pkm(conn):
    cur = conn.cursor()
    cur.execute(
        """
            CREATE OR REPLACE VIEW oldest_pkm AS
                SELECT * FROM (SELECT * FROM SANSANITOPokémon ORDER BY CHECKIN ASC) WHERE ROWNUM <= 1
                WITH READ ONLY;
        """
    )
    cur.commit()

# Elimina vista oldest_pkm
def Delete_view_oldest_pkm(conn):
    cur = conn.cursor()
    cur.execute(
        """
            DROP VIEW oldest_pkm ;
        """
    )
    cur.commit()

# Vista de los 10 PKM con mayor prioridad
def View_top_ten_highest(conn):
    cur = conn.cursor()
    cur.execute(
        """
            CREATE OR REPLACE VIEW top_ten_h AS
                SELECT * FROM (SELECT * FROM SANSANITOPokémon ORDER BY PRIORITY DESC) WHERE ROWNUM <= 10
                WITH READ ONLY;
        """
    )
    cur.commit()

# Elimina vista top_ten_h
def Delete_top_ten_highest(conn):
    cur = conn.cursor()
    cur.execute(
        """
            DROP VIEW top_ten_h ;
        """
    )
    cur.commit()

# Vista de los 10 PKM con menor prioridad
def View_top_ten_lowest(conn):
    cur = conn.cursor()
    cur.execute(
        """
            CREATE OR REPLACE VIEW top_ten_l AS
                SELECT * FROM (SELECT * FROM SANSANITOPokémon ORDER BY PRIORITY ASC) WHERE ROWNUM <= 10
                WITH READ ONLY;
        """
    )
    cur.commit()

# Elimina vista top_ten_l
def Delete_top_ten_lowest(conn):
    cur = conn.cursor()
    cur.execute(
        """
            DROP VIEW top_ten_l ;
        """
    )
    cur.commit()

# Vista de los PKM legendarios
def View_all_legendary(conn):
    cur = conn.cursor()
    cur.execute(
        """
            CREATE OR REPLACE VIEW all_legendary AS
                SELECT * FROM (SELECT * FROM SANSANITOPokémon WHERE LEGENDARY = 1)
            WITH READ ONLY;
        """
    )

# Elimina vista all_legendary
def Delete_all_legendary(conn):
    cur = conn.cursor()
    cur.execute(
        """
            DROP VIEW all_legendary ;
        """
    )
    cur.commit()

# Vista de los PKM según un estado especifico
def View_all_state(conn,state):
    cur = conn.cursor()
    cur.execute(
        f"""
            CREATE OR REPLACE VIEW all_state AS
                SELECT * FROM (SELECT * FROM SANSANITOPokémon WHERE STATE = '{state}')
            WITH READ ONLY;
        """
    )

# Elimina vista all_state
def Delete_all_state(conn):
    cur = conn.cursor()
    cur.execute(
        """
            DROP VIEW all_state ;
        """
    )
    cur.commit()

# Vista de todos los PKM ordenados por prioridad
def View_all_pkm_prio(conn):
    cur = conn.cursor()
    cur.execute(
        """
            CREATE OR REPLACE VIEW all_prio AS
                SELECT * FROM (SELECT NAME, HP_ACT, HP_MAX, PRIORITY FROM SANSANITOPokémon ORDER BY PRIORITY DESC) 
                WITH READ ONLY;
        """
    )
    cur.commit()

# Elimina vista all_prio
def Delete_all_prio(conn):
    cur = conn.cursor()
    cur.execute(
        """
            DROP VIEW all_prio ;
        """
    )
    cur.commit()

# Funcion que muestra el nombre más repetido
def Most_popular_pkm(conn):
    cur = conn.cursor()
    cur.execute(
        f"""
        SELECT * FROM (SELECT NAME, COUNT( NAME ) AS total FROM SANSANITOPokémon GROUP BY NAME ORDER BY total DESC) WHERE ROWNUM <= 1;
        """
    )
    cur.commit()
    for row in cur:
        name = row[0]
        return name
    
# Ingresar
def Ingresar(conn):
    cur = conn.cursor()
    print("┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓")
    print("   Qué tipo de Pokémon desea ingresar?")
    print("   0- Regresar al Menu")
    print("   1- Normal")
    print("   2- Legendario")
    print("┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛")
    o = int(input())
    if o == 0 :
        return
    elif o == 1 :
        cap = Count(conn)
        if cap > 0 :
            print("┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓")
            print("   Escriba el nombre del Pokémon que desea ingresar")
            print("┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛")
            name = input()
            Create(conn,name)
        else : 
            print("┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓")
            print("   La capacidad esta al máximo, se intercambiara el Pokémon")
            print("   por uno de menor prioridad")
            print("┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛")
            input()
            print("┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓")
            print("   Escriba el nombre del Pokémon que desea ingresar")
            print("┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛")
            name = input()
            Create(conn,name)
            id0, prio = Last_one_pkm(conn)
            Swap_normal(conn, name, id0, prio)
            return
    elif o == 2 :
        cap = Count(conn)
        if cap > 5 :
            print("┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓")
            print("   Escriba el nombre del Pokémon que desea ingresar")
            print("┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛")
            name = input()
            check =  Check_legendary(conn, name)
            if check == 0 :
                Create(conn,name)
            else :
                print("┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓")
                print("   El Pokémon ya se encuentra ingresado")
                print("┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛")
                input()
                return
        else :
            print("┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓")
            print("   Escriba el nombre del Pokémon que desea ingresar")
            print("┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛")
            name = input()
            check =  Check_legendary(conn, name)
            if check == 0 :
                Create(conn,name)
                id0, prio = Last_one_pkm(conn)
                Swap_legendary(conn, name, id0, prio)
            else :
                print("┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓")
                print("   El Pokémon ya se encuentra ingresado")
                print("┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛")
                input()
                return
            

    else :
        print("┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓")
        print("   Opción invalida")
        print("┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛")
        input()
        return Ingresar(conn)




#MENU ----------------------------------------

connect_string = "DRIVER={Oracle en OraDB18Home3};DBQ=localhost:1521;Uid=SYSTEM;Pwd=Base1234"

# Connect string format: [username]/[password]@//[hostname]:[port]/[DB service name]
conn = pyodbc.connect(connect_string)
cur = conn.cursor()

""" DeleteTrigger(conn)
DeleteSequence(conn)
Delete_POYO(conn)
Delete_SANSANITO_POKE(conn)
Delete_view_oldest_pkm(conn)
Delete_top_ten_highest(conn)
Delete_top_ten_lowest(conn)
Delete_all_legendary(conn)
Delete_all_state(conn)
Delete_all_prio(conn) """

print("┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓")
print("   Bienvenido!")
print("┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛")
input()
print("┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓")
print("   Un momento, se esta creando la tabla Poyo.")
print("┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛")

Create_POYO(conn)
PK_Poyo(conn)
Complete_table_POYO(conn)
input()
print("┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓")
print("   Tabla Poyo creada en la base de datos con éxito!")
print("┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛")
input()
print("┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓")
print("   Un momento, se esta creando la tabla Sansanito Pokémon.")
print("┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛")

Create_SANSANITO_POKE(conn)
PK_Sansanito(conn)
Create_sequenceID(conn)
IdSANSANITO(conn)
input()
print("┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓")
print("   Tabla Sansanito Pokémon creada en la base de datos con éxito!")
print("┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛")
input()
print("┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓")
print("   Se necesita llenar la tabla Sansanito Pokémon")
print("┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛")
c = Count(conn)
#print ("capacidad " +str(c))
Complete_table_SANSA(conn)
input()   
a = 0

View_top_ten_highest(conn)
View_top_ten_lowest(conn)
View_all_legendary(conn)
View_oldest_pkm(conn)
View_all_pkm_prio(conn)
while a < 1:

    print("┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓")
    print("   MENU ")
    print("   0- Salir. ")                                     
    print("   1- Ingresar un Pokémon. ")
    print("   2- Mostrar a los 10 Pokémon con mayor prioridad. ")
    print("   3- Mostrar a los 10 Pokémon con menor prioridad. ")
    print("   4- Mostrar todos los Pokémon con un estado especifico. ")
    print("   5- Mostrar a todos los Pokémon legendarios. ")
    print("   6- Mostrar el Pokémon que lleva más tiempo ingresado. ")
    print("   7- Mostrar nombre del Pokémon más repetido en la base de datos. ")
    print("   8- Mostrar todos los Pokémon ordenados por prioridad. ")
    print("   9- Capacidad actual de la tabla. ")
    print("   10- CRUD ")
    print("\n")
    print("   Seleccione un opción")
    print("┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛")
    option = int(input())
    if option == 0 :
        a = 1
    elif option == 1 :
        Ingresar(conn)
    elif option == 2 :
        print("┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓")
        print("   Los 10 Pokémon con mayor prioridad son :")
        print(" ")
        cur.execute(
            """
            SELECT * FROM top_ten_h;
            """
        )
        for row in cur:
            id_sansa = row[0]
            n_poke = row[1]
            name = row[2]
            t1 = row[3]
            t2 = row[4]
            hp_act = row[5]
            hp_max = row[6]
            leg = row[7]
            state = row[8]
            checkin = row[9]
            prio = row[10]
            print("   ID:                  "+str(id_sansa))
            print("   N° Pokedex:          "+str(n_poke))
            print("   Name:                "+str(name))
            print("   Tipo 1:              "+str(t1))
            print("   Tipo 2:              "+str(t2))
            print("   HP Act:              "+str(hp_act))
            print("   HP Max:              "+str(hp_max))
            print("   Legendario:          "+str(leg))
            print("   Estado:              "+str(state))
            print("   Checkin:             "+str(checkin))
            print("   Prioridad:           "+str(prio))
            print("   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
        input()
    elif option == 3 :
        print("┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓")
        print("   Los 10 Pokémon con mayor prioridad son :")
        cur.execute(
            """
            SELECT * FROM top_ten_l;
            """
        )
        for row in cur:
            id_sansa = row[0]
            n_poke = row[1]
            name = row[2]
            t1 = row[3]
            t2 = row[4]
            hp_act = row[5]
            hp_max = row[6]
            leg = row[7]
            state = row[8]
            checkin = row[9]
            prio = row[10]
            print("   ID:                  "+str(id_sansa))
            print("   N° Pokedex:          "+str(n_poke))
            print("   Name:                "+str(name))
            print("   Tipo 1:              "+str(t1))
            print("   Tipo 2:              "+str(t2))
            print("   HP Act:              "+str(hp_act))
            print("   HP Max:              "+str(hp_max))
            print("   Legendario:          "+str(leg))
            print("   Estado:              "+str(state))
            print("   Checkin:             "+str(checkin))
            print("   Prioridad:           "+str(prio))
            print("   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
        input()
    elif option == 4 :  #REVISAR CUANDO NO HAY PKMS CON ESE ESTADOS
            print("┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓")
            for s in ["   Seleccione el estado por el que desea filtrar: ","   1-Envenenado", "   2-Paralizado", "   3-Quemado", "   4-Dormido","   5-Congelado","   6-None"]:
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
            View_all_state(conn,state)
            cur.execute(
            """
            SELECT * FROM all_state;
            """
            )
            print("┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓")
            print("   Los Pokémon con estado "+state+" son :")
            for row in cur:
                id_sansa = row[0]
                n_poke = row[1]
                name = row[2]
                t1 = row[3]
                t2 = row[4]
                hp_act = row[5]
                hp_max = row[6]
                leg = row[7]
                state = row[8]
                checkin = row[9]
                prio = row[10]
                print("   ID:                  "+str(id_sansa))
                print("   N° Pokedex:          "+str(n_poke))
                print("   Name:                "+str(name))
                print("   Tipo 1:              "+str(t1))
                print("   Tipo 2:              "+str(t2))
                print("   HP Act:              "+str(hp_act))
                print("   HP Max:              "+str(hp_max))
                print("   Legendario:          "+str(leg))
                print("   Estado:              "+str(state))
                print("   Checkin:             "+str(checkin))
                print("   Prioridad:           "+str(prio))
                print("   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
            input()

    elif option == 5 :
        cur.execute(
            """
            SELECT * FROM all_legendary;
            """
        )
        dic = {}
        count = 0
        for row in cur :
            dic[count] = row
            count = count + 1
        if len(dic) == 0:
            print("┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓")
            print("   No hay Pokémon legendarios")
            print("┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛")
            input()
        else :
            print("┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓")
            print("   Los Pokémon legendarios son :")
            for row in cur:
                id_sansa = row[0]
                n_poke = row[1]
                name = row[2]
                t1 = row[3]
                t2 = row[4]
                hp_act = row[5]
                hp_max = row[6]
                leg = row[7]
                state = row[8]
                checkin = row[9]
                prio = row[10]
                print("   ID:                  "+str(id_sansa))
                print("   N° Pokedex:          "+str(n_poke))
                print("   Name:                "+str(name))
                print("   Tipo 1:              "+str(t1))
                print("   Tipo 2:              "+str(t2))
                print("   HP Act:              "+str(hp_act))
                print("   HP Max:              "+str(hp_max))
                print("   Legendario:          "+str(leg))
                print("   Estado:              "+str(state))
                print("   Checkin:             "+str(checkin))
                print("   Prioridad:           "+str(prio))
                print("   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
            input()
    elif option == 6 :
        cur.execute(
            """
            SELECT NAME FROM oldest_pkm;
            """
        )
        for row in cur:
            n = row[0]
        print("┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓")
        print("   El Pokémon que lleva más tiempo ingresado es " +n )
        print("┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛")
    elif option == 7 : # PROBARLAAA
        n = Most_popular_pkm(conn)
        print("┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓")
        print("   El nombre más repetido es " +n )
        print("┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛")
    elif option == 8 :
        print("┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓")
        print("   Lista de Pokémon ordenada por prioridad DESCENDENTE")
        cur.execute(
            """
            SELECT * FROM all_prio;
            """
        )
        for row in cur:
            name = row[0]
            hp_act = row[1]
            hp_max = row[2]
            prio = row[3]
            print("   Name:                "+str(name))
            print("   HP Act:              "+str(hp_act))
            print("   HP Max:              "+str(hp_max))
            print("   Prioridad:           "+str(prio))
            print("   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
        input()
    elif option == 9 :
        r = Count(conn)
        print("┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓")
        print("   La capacidad actual de la base de datos es " +str(r))
        print("┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛")
        input()

    elif option == 10 :
        b = 0
        while b != 1 :
            print("┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓")
            print("   CRUD MENU ")   
            print("   0- Regresar al Menú principal ")                                      # Arreglar dsp 
            print("   1- CREATE ")
            print("   2- READ ")
            print("   3- UPDATE ")
            print("   4- DELETE ")
            print("\n")
            print("   Seleccione un opción")
            print("┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛")
            op1 = int(input())
            if op1 == 0 :
                break
            elif op1 == 1 :
                Ingresar(conn)
            elif op1 == 2 :
                Read(conn)
                input()
            elif op1 == 3 :
                Update(conn)
            elif op1 == 4 :
                Delete(conn)
            else :
                print("┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓")
                print("   Opción invalida ")
                print("┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛")
                input()
    else : 
        print("┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓")
        print("   Opción invalida ")
        print("┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛")
        input()


