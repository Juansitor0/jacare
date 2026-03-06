import pandas as pd

SLOTS = ["00", "01", "02", "03", "04", "05"]


def transform_inventory(df: pd.DataFrame) -> pd.DataFrame:
    """
    Transforma o inventário em uma linha por site com colunas de slot: 'Slot 00'..'Slot 05'.

    Espera colunas: 'NEName', 'Board Type', 'Inventory Unit ID'.
    """
    required = ["NEName", "Board Type", "Inventory Unit ID"]
    for c in required:
        if c not in df.columns:
            raise KeyError(f"A coluna '{c}' não existe no DataFrame fornecido.")

    resultado = {}

    for _, row in df.iterrows():
        site = str(row["NEName"]).strip()
        board_type_raw = row["Board Type"]
        board_type = board_type_raw[4:] if board_type_raw and len(board_type_raw) > 4 else ""

        # Limpa a coluna Manufacturer Data para pegar apenas o primeiro valor (antes da vírgula)
        manufacturer_raw = str(row.get("Manufacturer Data", "")).strip()
        manufacturer = manufacturer_raw.split(',')[0] if manufacturer_raw else ""

        inventory_id = str(row["Inventory Unit ID"]).zfill(2)

        if site not in resultado:
            resultado[site] = {
                "site": site,
                "Manufacturer": manufacturer,
                **{f"Slot {s}": "" for s in SLOTS}
            }

        if inventory_id in SLOTS:
            resultado[site][f"Slot {inventory_id}"] = board_type

    return pd.DataFrame(resultado.values())


# Backwards compatibility alias (if older code used Portuguese name)
transformar_slot = transform_inventory