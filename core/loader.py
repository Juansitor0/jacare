import pandas as pd
import zipfile 


def _detect_separator_from_file_like(file_like) -> str:
    sample = file_like.read(4096)
    try:
        sample = sample.decode('utf-8')
    except Exception:
        try:
            sample = sample.decode('latin-1')
        except Exception:
            sample = str(sample)

    # simple heuristic: prefer comma if it appears more than semicolon
    if sample.count(',') >= sample.count(';'):
        return ','
    return ';'


def load_csv_from_zip(zip_path: str, separator: str = None) -> pd.DataFrame:
    """
    Carrega um arquivo CSV compactado em um arquivo ZIP e retorna um DataFrame do pandas.

    Parâmetros:
    zip_path (str): Caminho para o arquivo ZIP que contém o CSV.
    separator (str|None): Separador usado no arquivo CSV. Se None, será detectado automaticamente.

    Retorna:
    pd.DataFrame: DataFrame contendo os dados do CSV.
    """
    if not zipfile.is_zipfile(zip_path):
        raise ValueError(f"O arquivo em {zip_path} não é um arquivo ZIP válido.")

    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        csv_files = [f for f in zip_ref.namelist() if f.lower().endswith('.csv')]

        if not csv_files:
            raise FileNotFoundError("Nenhum arquivo CSV encontrado no arquivo ZIP.")

        csv_name = csv_files[0]  # Pega o primeiro arquivo CSV encontrado
        with zip_ref.open(csv_name) as csv_file:
            # detect separator if not provided
            if separator is None:
                sep = _detect_separator_from_file_like(csv_file)
                csv_file.seek(0)
            else:
                sep = separator

            df = pd.read_csv(csv_file, sep=sep, dtype=str)

    # normalize column names (trim whitespace)
    df.columns = [c.strip() for c in df.columns]

    return df