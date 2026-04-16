import sys
import json
import io
from pdf_service import fill_pdf

def main():
    """
    CLI Entry point.
    Usage: python3 cli.py <output_path.pdf>
    Input: Expects JSON via stdin.
    """
    try:
        # 1. Leer JSON desde la entrada estándar (stdin)
        input_data = sys.stdin.read()
        if not input_data:
            print("Error: No se recibió JSON por stdin", file=sys.stderr)
            sys.exit(1)
            
        data = json.loads(input_data)
        
        # 2. Generar el PDF usando el motor existente
        pdf_bytes = fill_pdf(data)
        
        # 3. Determinar ruta de salida
        output_path = sys.argv[1] if len(sys.argv) > 1 else "output.pdf"
        
        # 4. Guardar archivo
        with open(output_path, "wb") as f:
            f.write(pdf_bytes)
            
        print(f"Éxito: PDF generado en {output_path}")
        
    except json.JSONDecodeError:
        print("Error: El JSON enviado no es válido", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        import traceback
        print(f"Error Fatal: {str(e)}", file=sys.stderr)
        traceback.print_exc(file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
