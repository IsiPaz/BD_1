import pyodbc
import random
import csv
import datetime

#FUNCIONES_AUX --------------------------------

# Transforma el booleano de legendario en 1 o 0
def boolean_to_int(legendary):
    if legendary=="True":
        return 1
    else:
        return 0

def random_state():
    states = ["Envenenado", "Paralizado", "Quemado", "Dormido","Congelado","None"]
    state = random.choice(states)
    return state

def check_in_pkm():
    time = datetime.datetime.today()
    return time

#BORRAR --------------------------------

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

#CREAR TABLAS --------------------------------

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
        print(x)
        return x


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



def Create(conn):
    cur = conn.cursor()
    pkm_name = input("\nNombre del Pokémon que desea ingresar: ")
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
    hp_act = input("\nIngrese HP actual del Pokemon, debe ser menor a "+str(hp_max)+": ")
    prio = hp_max - int(hp_act)
    print("\nSeleccione el estado de su Pokémon: ")
    for s in ["1-Envenenado", "2-Paralizado", "3-Quemado", "4-Dormido","5-Congelado","6-None"]:
        print(s)
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
    print("\nDesea ingresar a "+pkm_name+" ? S/N")
    print("N° Pokedex: "+id_pokedex1)
    print("Tipo 1: "+type1)
    print("Tipo 2: "+str(type2))
    print("HP Act: "+str(hp_act))
    print("HP Max: "+str(hp_max))
    print("Legendario: " +str(legendary))
    print("Estado: " +state)
    print("Checkin: "+str(date_checkin))
    print("Prioridad: "+str(prio))
    flag = str(input())
    idd = 1
    if flag == "S":
        cur.execute(
            f"""
                INSERT INTO SANSANITOPOKEMON(ID, N_POKEDEX, NAME, TYPE1, 
                TYPE2, HP_ACT, HP_MAX, LEGENDARY, STATE, CHECKIN, PRIORITY)
                VALUES ('{idd}','{id_pokedex}','{pkm_name}','{type1}','{type2}','{hp_act}',
                '{hp_max}','{legendary}','{state}',LOCALTIMESTAMP,'{prio}');
            """)
        cur.commit()
        print("Pokémon Ingresado con éxito!")
        
    else:
        return

    






    






connect_string = "DRIVER={Oracle en OraDB18Home3};DBQ=localhost:1521;Uid=SYSTEM;Pwd=Base1234"

# Connect string format: [username]/[password]@//[hostname]:[port]/[DB service name]
conn = pyodbc.connect(connect_string)


#create_POYO(conn)
#create_SANSANITO_POKE(conn)

#Complete_table_POYO(conn)

#print(random_date())
#print(random_state())

#Priority(conn, "'Charmander'", 25)

#Search_POYO(conn,"'Pikachu'")
Create(conn)
