import threading
import time
import random

class SalaDeFestas:
    __acaoReitor = "nao esta aqui"
    __numEstudantes = 0
    __lock = None

    def __init__(self, numEstudantes):
        self.__numEstudantes = numEstudantes
        self.__lock = threading.Lock()

    def entraFesta(self):
        with self.__lock:
            self.__numEstudantes += 1
            return self.__numEstudantes

    def saiFesta(self):
        with self.__lock:
            self.__numEstudantes -= 1
            return self.__numEstudantes

    def getEstudantes(self):
        with self.__lock:
            return self.__numEstudantes
    
    def getAcao(self):
        with self.__lock:
            return self.__acaoReitor

    def putAcao(self, acao):
        with self.__lock:
            self.__acaoReitor = acao
            return self.__acaoReitor

def Estudantes(sala, mutex, nome):
    dentro = False
    while True:
        time.sleep(random.randint(1,5))
        mutex.acquire()
        if(sala.getAcao() == "nao esta aqui" and (not dentro)):
            sala.entraFesta()
            dentro = True
            print("estudante: "+ str(nome)+ " entrou na sala")

        elif (sala.getAcao() == "na sala" and dentro):
            sala.saiFesta()
            dentro = False
            print("estudante: "+ str(nome)+ " saiu da sala")
            time.sleep(1)

        elif(dentro):
            print("estudante: "+ str(nome) + " curtindo a doidado")
            time.sleep(4)
        mutex.release()

def Reitor(sala, mutex):
    while True:
        mutex.acquire()
        if(sala.getAcao() == "nao esta aqui"):
            if(sala.getEstudantes() >= 50):
                sala.putAcao("na sala")
                print("reitor: entrou na sala, acabou a festa")
                time.sleep(1)
                mutex.release()
            elif(sala.getEstudantes() == 0):
                sala.putAcao("estudando...")
                print("reitor: comecou a estudar")
                mutex.release()

        if(sala.getAcao() == "na sala" and sala.getEstudantes() == 0):
            sala.putAcao("nao esta aqui")
            print("reitor: saiu da sala")
            mutex.release()

        if(sala.getAcao() == "estudando..."):
            time.sleep(7)
            print("reitor: saiu da sala")
            sala.putAcao("nao esta aqui")
            mutex.release()


        time.sleep(random.randint(0,3))
        mutex.release()

def Main():
    sala = SalaDeFestas(0)
    mutex = threading.Semaphore(1)
    reitor = threading.Thread(target=Reitor,args=(sala, mutex))
    reitor.start()
    i = 0
    for i in range(60):
        threading.Thread(target=Estudantes,args=(sala, mutex, i)).start()

Main()