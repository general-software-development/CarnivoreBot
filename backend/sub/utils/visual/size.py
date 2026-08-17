from sub.core.runtime.typeCheck import typecheck_simple

@typecheck_simple
def toHumanReadable(no_bytes: int) -> str:
    units = ("B", "KiB", "MiB", "GiB", "TiB", "PiB")

    def do_round(size: float) -> float:
        tmpsize = size
        while tmpsize >= 1000:
            tmpsize = tmpsize / 1000

        if tmpsize <= 10 and no_bytes <= 64 * 1024 * 1024:  # 64MB
            return round(tmpsize, 2)

        if tmpsize <= 10:
            return round(tmpsize, 1)

        return int(tmpsize)

    size = float(no_bytes)
    for unit in units:
        if abs(size) < 1024:
            return f"{do_round(size):,} {unit}"
        size /= 1024

    return f"{do_round(size):,} EiB"
