import sys

from core.loader import load_csv_from_zip
from core.filters import filter_creditable, filter_board_name
from core.transformer import transform_inventory
from core.exporter import export_to_csv


def main():
    if len(sys.argv) != 3:
        print("Uso correto:")
        print("  python -m cli.run <arquivo_entrada.zip> <arquivo_saida.csv>")
        sys.exit(1)

    input_zip = sys.argv[1]
    output_csv = sys.argv[2]

    try:
        print(" Carregando dados...")
        df = load_csv_from_zip(input_zip)

        print(" Aplicando filtros...")
        df = filter_creditable(df)
        df = filter_board_name(df)

        print(" Transformando inventário...")
        df_final = transform_inventory(df)

        print("Exportando resultado...")
        export_to_csv(df_final, output_csv)

        print(" Processo concluído com sucesso!")

    except Exception as e:
        print(" Erro durante o processamento:")
        print(str(e))
        sys.exit(1)


if __name__ == "__main__":
    main()