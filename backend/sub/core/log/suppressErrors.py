class SuppressErrors:
    def __init__(self) -> None:
        pass

    def __enter__(self) -> None:
        return

    def __exit__(self, exc_type, exc_value, traceback):
        return True
