import os
import time

def main():
    pid = os.fork()

    if pid > 0:
        # Proceso padre
        print(f"Padre esperando, PID del hijo: {pid}")
        # Esperar un momento para que el hijo termine
        time.sleep(5)
        # El padre no llama a wait(), dejando al hijo como zombi
        print("Padre terminando")
    else:
        # Proceso hijo
        print(f"Hijo (PID: {os.getpid()}) terminando")

if __name__ == "__main__":
    main()
