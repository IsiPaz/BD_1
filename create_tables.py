import pyodbc
import random
import csv


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
            CHECKIN DATE,
            PRIORITY INTEGER);
        """
        )
    cur.commit()



def boolean_to_int(legendary):
    if legendary=="True":
        return 1
    else:
        return 0



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


connect_string = "DRIVER={Oracle en OraDB18Home3};DBQ=localhost:1521;Uid=SYSTEM;Pwd=Base1234"

# Connect string format: [username]/[password]@//[hostname]:[port]/[DB service name]
conn = pyodbc.connect(connect_string)

Complete_table_POYO(conn)