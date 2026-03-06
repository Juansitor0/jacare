import pandas as pd


def _normalize_colname(name: str) -> str:
    """Normaliza um nome de coluna: remove caracteres não-alfanuméricos e converte para lowercase."""
    return ''.join(ch for ch in str(name).lower() if ch.isalnum())


def _find_column(df: pd.DataFrame, target: str) -> str:
    """Retorna o nome exato da coluna no DataFrame que case-insensitive corresponde a target."""
    target_norm = _normalize_colname(target)
    for c in df.columns:
        if _normalize_colname(c) == target_norm:
            return c
    raise KeyError(f"A coluna '{target}' não existe no DataFrame fornecido.")


def filter_creditable(df: pd.DataFrame) -> pd.DataFrame:
    """
    Filtra o DataFrame para incluir apenas linhas onde a coluna 'creditable' (case-insensitive)
    é igual a 'yes' (case-insensitive).
    """
    col = _find_column(df, 'creditable')

    # Ensure comparison is case-insensitive and handle NaNs
    filtered_df = df[df[col].astype(str).str.lower() == 'yes']
    return filtered_df


def filter_board_name(df: pd.DataFrame, board_names: list = ["UBBP", "AIRU"]) -> pd.DataFrame:
    """
    Filtra o DataFrame para incluir apenas linhas onde a coluna 'board_name' (case-insensitive)
    corresponde a um dos valores fornecidos na lista.
    """
    col = _find_column(df, 'board_name')

    filtered_df = df[df[col].astype(str).isin(board_names)]
    return filtered_df
