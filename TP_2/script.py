import sys
import getopt


def main(argv):
    nombre = ""
    edad = ""

    try:
        opts, args = getopt.getopt(argv, "n:e:", ["nombre=", "edad="])
    except getopt.GetoptError:
        print("Uso: script.py -n <nombre> -e <edad>")
        sys.exit(2)

    for opt, arg in opts:
        if opt in ("-n", "--nombre"):
            nombre = arg
        elif opt in ("-e", "--edad"):
            edad = arg

    print(f"Hola {nombre}, tienes {edad} años.")


if __name__ == "__main__":
    main(sys.argv[1:])
