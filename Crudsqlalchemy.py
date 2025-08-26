from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Configuración de la base de datos (SQLite)
engine = create_engine("sqlite:///estudiantes.db", echo=False)
Base = declarative_base()
Session = sessionmaker(bind=engine)
session = Session()

# Definición del modelo
class Estudiante(Base):
    __tablename__ = "estudiantes"
    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String, nullable=False)
    edad = Column(Integer, nullable=False)
    cedula = Column(String, unique=True, nullable=False)
    correo = Column(String, unique=True, nullable=False)

Base.metadata.create_all(engine)

# ------------------ FUNCIONES CRUD ------------------ #

def crear_estudiante():
    nombre = input("Nombre: ")
    edad = int(input("Edad: "))
    cedula = input("Cédula: ")
    correo = input("Correo: ")
    estudiante = Estudiante(nombre=nombre, edad=edad, cedula=cedula, correo=correo)
    session.add(estudiante)
    session.commit()
    print("✅ Estudiante agregado.\n")

def listar_estudiantes():
    estudiantes = session.query(Estudiante).all()
    if estudiantes:
        print("\n--- Lista de estudiantes ---")
        for e in estudiantes:
            print(f"{e.id} - {e.nombre} - {e.edad} años - {e.cedula} - {e.correo}")
        print()
    else:
        print("⚠️ No hay estudiantes registrados.\n")

def actualizar_estudiante():
    id = int(input("Ingrese el ID del estudiante a actualizar: "))
    estudiante = session.query(Estudiante).filter_by(id=id).first()
    if estudiante:
        print("Deje en blanco si no quiere modificar un campo.")
        nuevo_nombre = input(f"Nuevo nombre ({estudiante.nombre}): ") or estudiante.nombre
        nueva_edad = input(f"Nueva edad ({estudiante.edad}): ")
        nueva_edad = int(nueva_edad) if nueva_edad else estudiante.edad
        nueva_cedula = input(f"Nueva cédula ({estudiante.cedula}): ") or estudiante.cedula
        nuevo_correo = input(f"Nuevo correo ({estudiante.correo}): ") or estudiante.correo

        estudiante.nombre = nuevo_nombre
        estudiante.edad = nueva_edad
        estudiante.cedula = nueva_cedula
        estudiante.correo = nuevo_correo
        session.commit()
        print("✅ Estudiante actualizado.\n")
    else:
        print("❌ Estudiante no encontrado.\n")

def eliminar_estudiante():
    id = int(input("Ingrese el ID del estudiante a eliminar: "))
    estudiante = session.query(Estudiante).filter_by(id=id).first()
    if estudiante:
        session.delete(estudiante)
        session.commit()
        print("✅ Estudiante eliminado.\n")
    else:
        print("❌ Estudiante no encontrado.\n")

# ------------------ MENÚ INTERACTIVO ------------------ #

def menu():
    while True:
        print("""
========= CRUD Estudiantes =========
1. Crear estudiante
2. Listar estudiantes
3. Actualizar estudiante
4. Eliminar estudiante
5. Salir
""")
        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            crear_estudiante()
        elif opcion == "2":
            listar_estudiantes()
        elif opcion == "3":
            actualizar_estudiante()
        elif opcion == "4":
            eliminar_estudiante()
        elif opcion == "5":
            print("👋 Saliendo...")
            break
        else:
            print("❌ Opción inválida.\n")

if __name__ == "__main__":
    menu()
