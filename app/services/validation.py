from pathlib import Path


class ValidationError(ValueError):
    pass


def detect_extension(filename: str) -> str:
    lower_name = filename.lower()
    if lower_name.endswith(".nii.gz"):
        return ".nii.gz"
    return Path(lower_name).suffix


def validate_extension(filename: str, allowed_extensions: set[str]) -> str:
    extension = detect_extension(filename)
    if not extension or extension not in allowed_extensions:
        raise ValidationError("extensión de archivo no permitida")
    return extension


def validate_upload_size(size_bytes: int, max_size_bytes: int) -> None:
    if size_bytes > max_size_bytes:
        raise ValidationError("archivo supera el tamaño máximo permitido")
