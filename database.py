from sqlalchemy import Table, Column, String, Float
from sqlalchemy import create_engine, MetaData, select, delete, insert
from datetime import datetime

'''
структура БД:
city: string
pressure: float
temp: float
wind: float
last_request: time
'''

#создет таблицу, если её нет
def create_table():
    engine = create_engine('sqlite:///cities.sqlite')
    metadata = MetaData()
    data = Table('data', metadata,
             Column('city', String(255)),
             Column('pressure', Float()),
             Column('temp', Float()),
             Column('wind', Float()),                   
             Column('last_request', String(255)))
    metadata.create_all(engine)

#создает соединение с таблицей
def get_connect():
    create_table()
    engine = create_engine('sqlite:///cities.sqlite')
    metadata = MetaData()
    data = Table('data', metadata, autoload=True, autoload_with=engine)
    connection = engine.connect()
    return data, connection

#проверка, если ли город в таблице
def city_in_da_base(city):

    data, connection = get_connect()
    
    stmt = select([data])
    stmt = stmt.where(data.columns.city == city)
    results = connection.execute(stmt).fetchall()
    if len(results) == 0:
        return False
    else:
        last_time = datetime.strptime(results[0][-1], "%Y-%m-%d %H:%M:%S.%f")
        current_time = datetime.now()
        difference = (current_time - last_time).total_seconds()/60
        if difference >= 30:
            stmt_del = delete(data)
            stmt_del = stmt_del.where(data.columns.city == city)
            results = connection.execute(stmt_del)
            return False
        else:
            return True

#получение города из таблицы
def get_city_from_base(city):
    
    data, connection = get_connect()
    
    stmt = select([data])
    stmt = stmt.where(data.columns.city == city)
    results = connection.execute(stmt).fetchall()[0]
    ans = {}
    ans["city"] = results[0]
    ans["pressure"] = results[1]
    ans["temp"] = results[2]
    ans["wind"] = results[3]
    
    return ans

#запись города в таблицу
def write_city_to_base(ans):
    
    data, connection = get_connect()    

    stmt = insert(data).values(city=ans["city"], temp=ans["temp"], 
                 pressure=ans["pressure"], wind=ans["wind"],
                 last_request=str(datetime.now()))
    results = connection.execute(stmt)
    return