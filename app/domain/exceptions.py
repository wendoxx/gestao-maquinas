class DomainError(Exception):
    """Base class for business rule errors."""


class AssetNotFound(DomainError):
    def __init__(self, asset_id: int):
        super().__init__(f"Ativo {asset_id} não encontrado")


class DuplicateCode(DomainError):
    def __init__(self, code: str):
        super().__init__(f"Já existe um ativo com o código '{code}'")


class ValidationError(DomainError):
    pass