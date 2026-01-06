import pandas as pd


def exportar_csv(df: pd.DataFrame, output_path: str, separator=",") -> None:
    """
    Exporta um DataFrame do pandas para um arquivo CSV.

    Parâmetros:
    df (pd.DataFrame): DataFrame a ser exportado.
    output_path (str): Caminho onde o arquivo CSV será salvo.
    separator (str): Separador a ser usado no arquivo CSV. Padrão é vírgula (,).

    Retorna:
    None
    """
    df.to_csv(output_path, sep=separator, index=False)


def export_to_csv(df: pd.DataFrame, output_path: str, separator=",") -> None:
    """
    Wrapper em inglês para compatibilidade com a CLI: exporta um DataFrame para CSV.
    """
    exportar_csv(df, output_path, separator=separator)
