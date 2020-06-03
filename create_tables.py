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





connect_string = "DRIVER={Oracle en OraDB18Home3};DBQ=localhost:1521;Uid=SYSTEM;Pwd=Base1234"

# Connect string format: [username]/[password]@//[hostname]:[port]/[DB service name]
conn = pyodbc.connect(connect_string)

