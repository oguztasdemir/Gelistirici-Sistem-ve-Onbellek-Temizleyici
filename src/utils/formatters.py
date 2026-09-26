def format_bytes(bytes_count: int | float) -> str:
    """Bayt miktarını okunabilir formata (B, KB, MB, GB, TB) dönüştürür."""
    if not bytes_count or bytes_count <= 0:
        return "0.00 B"
    
    units = ["B", "KB", "MB", "GB", "TB"]
    unit_index = 0
    val = float(bytes_count)
    
    while val >= 1024.0 and unit_index < len(units) - 1:
        val /= 1024.0
        unit_index += 1
        
    if unit_index == 0:
        return f"{int(val)} B"
    return f"{val:.2f} {units[unit_index]}"


def format_duration(seconds: float) -> str:
    """Süreyi okunabilir saniye veya dakika formatına dönüştürür."""
    if seconds < 1:
        return f"{seconds * 1000:.0f} ms"
    if seconds < 60:
        return f"{seconds:.1f} sn"
    minutes = int(seconds // 60)
    secs = int(seconds % 60)
    return f"{minutes} dk {secs} sn"
