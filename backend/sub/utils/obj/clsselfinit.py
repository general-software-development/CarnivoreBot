class SelfInitClsMeta(type):
    def __new__(mcls, name, bases, namespace: dict):
        cls = super().__new__(mcls, name, bases, namespace)

        if namespace.get("__args__", {}).get("SelfInitClsMeta", {}).get("__no_selfinit", False) == True:
            new_args = namespace["__args__"]
            new_args['SelfInitClsMeta'].pop('__no_selfinit')
            setattr(cls, "__args__", new_args)
            return cls

        return cls()

class SelfInitCls(metaclass=SelfInitClsMeta):
    __args__ = {
        "SelfInitClsMeta": {
            "__no_selfinit": True
        }
    }

    ...
