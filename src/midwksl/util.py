import os
from functools import cache

from dotenv import load_dotenv, find_dotenv

import avesterra.registries as av_registries
from avesterra import AvEntity, AvAuthorization, ApplicationError, AvContext, AvClass, AvCategory
import avesterra.objects as objects
import avesterra.registries as registries
import avesterra.avial as av

READ_AUTH = AvAuthorization("00000000-0000-0000-0000-000000000001")

_auth: AvAuthorization | None = None

def init_sess_auth(a: AvAuthorization):
    global _auth
    _auth = a

def auth(a: AvAuthorization | None = None) -> AvAuthorization:
    global _auth
    if a is None:
        if _auth is None:
            _auth = AvAuthorization(env("AVT_AUTH"))
        return _auth
    else:
        return a

def env(key: str, default: str | None = None) -> str:
    value = os.environ.get(key)
    if value is None:
        if default is not None:
            return default
        else:
            raise ValueError(f"Missing environment variable {key}")
    else:
        return value

@cache
def origin():
    return av_registries.lookup_registry(
        registry=AvEntity(0,0,1),
        key="MIDWKSL",
        authorization=READ_AUTH
    )

@cache
def regs():
    return av_registries.lookup_registry(
        registry=origin(),
        key="Registries",
        authorization=READ_AUTH
    )

@cache
def outlets():
    return av_registries.lookup_registry(
        registry=origin(),
        key="Outlets",
        authorization=READ_AUTH
    )

def registry_exists(key: str):
    try:
        av_registries.lookup_registry(
            registry=regs(),
            key=key,
            authorization=READ_AUTH
        )
        return True
    except ApplicationError:
        return False

def outlet_exists(key: str):
    try:
        av_registries.lookup_registry(
            registry=outlets(),
            key=key,
            authorization=READ_AUTH
        )
        return True
    except ApplicationError:
        return False

@cache
def find_registry(key: str):
    return av_registries.lookup_registry(
        registry=regs(),
        key=key,
        authorization=READ_AUTH
    )

@cache
def find_outlet(key: str):
    return av_registries.lookup_registry(
        registry=outlets(),
        key=key,
        authorization=READ_AUTH
    )

@cache
def outlet(name: str, a: AvAuthorization | None = None) -> AvEntity:
    key = name.lower().replace(" ", "_")
    if outlet_exists(key):
        e = find_outlet(key)
    else:
        # Create outlet object
        e = objects.create_object(
            name=name,
            key=key,
            context=AvContext.NULL,
            klass=AvClass.AVESTERRA,
            category=AvCategory.AVESTERRA,
            authorization=auth(a=a)
        )

        # Self connect outlet on presence level 1
        av.connect_method(
            entity=e,
            outlet=e,
            presence=1,
            authorization=auth(a)
        )

        # Activate object to make outlet
        av.activate_entity(
            outlet=e,
            authorization=auth(a)
        )

        registries.register_entity(
            registry=outlets(),
            name=name,
            key=key,
            entity=e,
            authorization=auth(a)
        )

    return e


@cache
def resolve_registry(name: str, a: AvAuthorization | None = None) -> AvEntity:
    key = name.lower().replace(" ", "_")
    if registry_exists(key):
        e = find_registry(key)
    else:
        # Create registry
        e = registries.create_registry(
            name=name,
            key=key,
            authorization=auth(a=a)
        )

        registries.register_entity(
            registry=regs(),
            name=name,
            key=key,
            entity=e,
            authorization=auth(a)
        )

    return e

def env_avt_auth() -> AvAuthorization:

    load_dotenv(find_dotenv())

    a = AvAuthorization(env("AVT_AUTH", "NONE"))
    if a == "NONE":
        # Try loading from /AvesTerra/Data...
        _def_authorities_path = os.path.join(os.path.abspath(os.sep), "AvesTerra", "Data", "Authorities.txt")
        if os.path.exists(_def_authorities_path):
            with open(_def_authorities_path, "r") as f:
                a = AvAuthorization(f.read().strip())
        else:
            raise ValueError("No Authorities file found")
    return a

def env_avt_host() -> str:
    return env("AVT_HOST", "127.0.0.1")

def env_avt_verify_chain_dir() -> str:
    return env("AVT_VERIFY_CHAIN_DIR", default=os.path.join(os.path.abspath(os.sep), "AvesTerra", "Certificates"))

def avtc_init(
    avt_host: str | None = None,
    avt_verify_chain_dir: str | None = None,
    avt_auth: AvAuthorization | None = None,
    max_socket_count: int = 2
):
    global _auth

    if avt_host is None:
        avt_host = env_avt_host()
    print(f"Info: Loaded avt_host as `{avt_host}`")

    if avt_verify_chain_dir is None:
        avt_verify_chain_dir = env_avt_verify_chain_dir()
    print(f"Info: Loaded avt_verify_chain_dir as `{avt_verify_chain_dir}`")

    if avt_auth is None:
        avt_auth = env_avt_auth()
    _auth = avt_auth
    print(f"Info: Loaded auth as `{avt_auth}`")

    av.initialize(
        server=avt_host,
        directory=avt_verify_chain_dir,
        socket_count=max_socket_count,
    )

    # Test server connectivity
    av.server_version(
        server=AvEntity(0,0,0)
    )

def avtc_fin():
    av.finalize()