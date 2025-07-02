from modelos.categoria import Categoria, TipoCategoria

class CategoriaFactory:
    @staticmethod
    def crear_categoria(cuenta_id, nombre, tipo):
        if isinstance(tipo, str):
            tipo = tipo.lower().strip()
            print(f"DEBUG tipo después de lower/strip: '{tipo}'")

            if tipo == "ingreso":
                tipo_enum = TipoCategoria.INGRESO
            elif tipo == "gasto":
                tipo_enum = TipoCategoria.GASTO
            else:
                raise ValueError("Tipo de categoría inválido")
        elif isinstance(tipo, TipoCategoria):
            tipo_enum = tipo
        else:
            print(f"DEBUG tipo_enum creado: {tipo_enum} (type={type(tipo_enum)})")
            raise ValueError("Tipo de categoría inválido")
        
        print(f"DEBUG tipo_enum creado: {tipo_enum} (type={type(tipo_enum)})")
        return Categoria(nombre=nombre, tipo=tipo_enum, cuenta_id=cuenta_id)
