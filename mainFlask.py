from flask import Flask,request
from flask_cors import CORS
import pandas as pd
import json

# realizo la extracion de los datos
def obtener_datosDataFrame(datos):
    dfGeneral=pd.read_csv(datos,sep=';')
    print(dfGeneral)
    return dfGeneral

#crea un objeto para flask ylo instancio
app=Flask(__name__,template_folder='Template')
CORS(app)


#realizo la prueba del funcionamiento de la api con un agradecimiento
@app.route('/')
def Bienvenido():
    return "Gracias mi dios por la sabiduria que me has dado"

#-------------------------------------------------------------------------------
# Realizo la visualizacion de todo el dataframe
#-------------------------------------------------------------------------------
@app.route('/Plataformas y sus peliculas/',methods=['GET'])
def data_completa():
    dfGeneral=obtener_datosDataFrame(datos)
    return json.loads(dfGeneral.to_json(orient='index'))

#-------------------------------------------------------------------------------
# Se realizo el primer punto del proyecto PI
#-------------------------------------------------------------------------------
#http://127.0.0.1:9000/Película con mayor duración?anio=2020&plataforma=amazon&duracion=min
@app.route('/Película con mayor duración',methods=['GET'])
def get_max_duration():
    dfGeneral=obtener_datosDataFrame(datos)
    anio=int(request.args.get('anio'))
    plat=str(request.args.get('plataforma'))
    tipoDurac=str(request.args.get('duracion'))

    consultaUno=dfGeneral[(dfGeneral['release_year']==anio) &
       (dfGeneral["plataforma"]==plat) &
       (dfGeneral["duration_type"]==tipoDurac) &
       (dfGeneral["type"]=="movie")].sort_values(by='duration_int', ascending=False).head(1)
    #a=consultaUno[["id","title","duration_int"]].style.hide(axis="index").format(precision=0)
    return json.loads(consultaUno[["id","title","duration_int"]].to_json(orient='index'))
          
#-------------------------------------------------------------------------------
# Se realizo el segundo punto del proyecto PI
#-------------------------------------------------------------------------------
# 
#  año (la función debe llamarse get_score_count(platform, scored, year))
#http://127.0.0.1:9000/Cantidad de películas por plataforma con puntaje mayor a?plataforma=amazon&scored=3,6&anio=2020
@app.route('/Cantidad de películas por plataforma con puntaje mayor a',methods=['GET'])
def get_score_count():
    dfGeneral=obtener_datosDataFrame(datos)
        
    plat=str(request.args.get('plataforma'))
    scor=float(request.args.get('scored'))
    anio=int(request.args.get('anio'))
    
    a=dfGeneral["title"][(dfGeneral["type"]=='movie') &
                (dfGeneral["plataforma"]==plat) & 
                (dfGeneral["scored"]>scor) & #----De 3.72 a 3.34
                (dfGeneral['release_year']==anio)].count()
    a=float(a)#--> el valor arrojado en entero 
    diccionari = {scor: a} #--> meto la variable en un dicionario para que flask lo reconosca
    return diccionari
#json.loads(a.to_json(orient='index'))


#-------------------------------------------------------------------------------
# Se realizo el tercer punto del proyecto PI
#-------------------------------------------------------------------------------
#http://127.0.0.1:9000/Cantidad de películas por plataforma?plataforma=amazon
@app.route('/Cantidad de películas por plataforma',methods=['GET'])
def get_count_platform():
    dfGeneral=obtener_datosDataFrame(datos)
        
    plat=str(request.args.get('plataforma'))
         
    b=dfGeneral["title"][(dfGeneral["type"]=='movie') &
                     (dfGeneral["plataforma"]==plat)].count()
   
    b=int(b)#--> el valor arrojado en entero 
    diccionario = {plat: b} #--> meto la variable en un dicionario para que flask lo reconosca
    return diccionario
   
#-------------------------------------------------------------------------------
# Se realizo el cuarto punto del proyecto PI
#-------------------------------------------------------------------------------
#/Actor que más se repite según plataforma y año?plataforma=amazon&anio=2020
@app.route('/Actor que más se repite según plataforma y año',methods=['GET'])
def get_actor():

    #extraigo los datos por medio d la funcion "obtener_datosDataFrame"
    dfGeneral=obtener_datosDataFrame(datos)

    #plat y anio son variables    
    plat=str(request.args.get('plataforma')) # -->plat resive el valor ingresado por el cliente
    anio=int(request.args.get('anio'))# -->plat resive el valor ingresado por el cliente
  
    #Pego el script que anteriormente ya provee en python
    a=dfGeneral[(dfGeneral["plataforma"]==plat) &
               (dfGeneral['release_year']==anio)]
   
    # retorno el resultado de la consulta atravez de una json.loads(variable..to_json(orient='index'))
    return json.loads(a["cast"].value_counts().head(1).to_json(orient='index'))

#-------------------------------------------------------------------------------
#Se realizaron todas las consultas solicitadas para el proyecto PI
#-------------------------------------------------------------------------------


if __name__=='__main__':
    datos="DataPlataformas.csv"
    app.run(host='0.0.0.0', port=9000,debug=True)



#python -m venv venv -- crear el ambiente virtual desde la terminal
#crear el main.py -- crear un archivo en el ambinete virtual
#cd
#.\venv\
#Set-ExecutionPolicy -ExecutionPolicy Remotesigned -Scope process
#.\Scripts\
#.\activate
#cd ..
#cd ..
#pip install (las librerias) ---> Carpeta raiz
#uvicorn main:app
#uvicorn main:app --reload  #---> para que quede cocorriendo mientras dse programa
#http://localhost:8000
#http://localhost:8000/docs   
# video esencial para realizar la api con FLASK
# https://www.youtube.com/watch?v=5wSN0l4UH38 
# ------------------------------------------------
# enviar aproducion con flask sigue los siguetes puntos
# ------------------------------------------------
#crear un archivo sin extencion llamado "procfile"
#  colocar dentro --> web:gunicorn app:app
#-------------------------------------------------
#crear un archivo llamado "requirements.txt" #--> pip freeze > requirements.txt
#  Colocar dentro si es posible con las verciones ejemplo
# --> Flask==2.2.3 #--> obligatorio
# --> Flask-Cors==3.0.10 #--> obligatorio
# --> gunicorn #--> obligatorio
# -->  mas en resto como : python, pandas,etc.
#----------------------------------------------------
# importar este libreria 
#-----------------------------------------------------
# --> from flask_cors import CORS
# --> colocar de bajo de esta linea " app=Flask(__name__) " la siguete palabra
# --> CORS(app)

