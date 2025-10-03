import json
import os
from functools import cache
from dotenv import load_dotenv, find_dotenv
import avesterra.registries as av_registries
from avesterra import AvEntity, ApplicationError, AvContext, AvClass, AvCategory
import avesterra.objects as objects
import avesterra.registries as registries
import avesterra.avial as av
from typing import List
from avesterra.avial import AvAuthorization
import midwksl.mac as mac
from midwksl.mac import aca


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
@aca()
def origin(auth: AvAuthorization):
    try:
        return av_registries.lookup_registry(
            registry=AvEntity(0, 0, 1),
            key="MIDWKSL",
            authorization=auth
        )
    except ApplicationError:
        e = registries.create_registry(
            name="MIDWKSL",
            key="MIDWKSL",
            authorization=auth
        )
        registries.register_entity(
            registry=AvEntity(0, 0, 1),
            name="MIDWKSL",
            key="MIDWKSL",
            entity=e,
            authorization=auth
        )
        return e


@cache
@aca()
def regs(auth: AvAuthorization):
    try:
        return av_registries.lookup_registry(
            registry=origin(),
            key="registries",
            authorization=auth
        )
    except ApplicationError:
        e = registries.create_registry(
            name="Registries",
            key="registries",
            authorization=auth
        )

        registries.register_entity(
            registry=origin(),
            name="Registries",
            key="registries",
            entity=e,
            authorization=auth
        )
        return e

@cache
@aca()
def outlets(auth: AvAuthorization):
    try:
        return av_registries.lookup_registry(
            registry=origin(),
            key="outlets",
            authorization=auth
        )
    except ApplicationError:
        e = registries.create_registry(
            name="Outlets",
            key="outlets",
            authorization=auth
        )

        registries.register_entity(
            registry=origin(),
            name="Outlets",
            key="outlets",
            entity=e,
            authorization=auth
        )
        return e

def init_midwksl_ks():
    origin()
    regs()
    outlets()

@aca()
def registry_exists(key: str, auth: AvAuthorization):
    try:
        av_registries.lookup_registry(
            registry=regs(),
            key=key,
            authorization=auth
        )
        return True
    except ApplicationError:
        return False

@aca()
def outlet_exists(key: str, auth: AvAuthorization):
    try:
        av_registries.lookup_registry(
            registry=outlets(),
            key=key,
            authorization=auth
        )
        return True
    except ApplicationError:
        return False

@cache
@aca()
def find_registry(key: str, auth: AvAuthorization):
    return av_registries.lookup_registry(
        registry=regs(),
        key=key,
        authorization=auth
    )

@cache
@aca()
def find_outlet(key: str, auth: AvAuthorization):
    return av_registries.lookup_registry(
        registry=outlets(),
        key=key,
        authorization=auth
    )

@cache
@aca()
def outlet(name: str, auth: AvAuthorization, self_subscribe: bool = False, self_connect: bool = False) -> AvEntity:
    key = name.lower().replace(" ", "_")
    if outlet_exists(key=key):
        e = find_outlet(key=key)
    else:
        # Create outlet object
        e = objects.create_object(
            name=name,
            key=key,
            context=AvContext.NULL,
            klass=AvClass.AVESTERRA,
            category=AvCategory.AVESTERRA,
            authorization=auth
        )

        if self_connect:
            # Self connect outlet on presence level 1
            av.connect_method(
                entity=e,
                outlet=e,
                presence=1,
                authorization=auth
            )

        if self_subscribe:
            # Self subscribe to all events published directly outlet
            av.subscribe_event(
                entity=e,
                outlet=e,
                authorization=auth
            )

        # Activate object to make outlet
        av.activate_entity(
            outlet=e,
            authorization=auth
        )

        registries.register_entity(
            registry=outlets(),
            name=name,
            key=key,
            entity=e,
            authorization=auth
        )

    return e


@cache
@aca()
def resolve_registry(name: str, auth: AvAuthorization) -> AvEntity:
    key = name.lower().replace(" ", "_")
    if registry_exists(key=key):
        e = find_registry(key=key)
    else:
        # Create registry
        e = registries.create_registry(
            name=name,
            key=key,
            authorization=auth
        )

        registries.register_entity(
            registry=regs(),
            name=name,
            key=key,
            entity=e,
            authorization=auth
        )

    return e

def env_avt_tokens() -> List[AvAuthorization]:
    tokens: List[AvAuthorization] = []
    tokens_str = env("AVT_TOKENS", "NONE")
    if tokens_str == "NONE":
        # Try loading from /AvesTerra/Data...
        _def_authorities_path = os.path.join(os.path.abspath(os.sep), "AvesTerra", "Data", "Authorities.txt")
        if os.path.exists(_def_authorities_path):
            with open(_def_authorities_path, "r") as f:
                tokens.append(AvAuthorization(f.read().strip()))
        else:
            raise ValueError("No Authorities file found")
    else:
        split_tokens: List[str] = json.loads(tokens_str)
        for token_str in split_tokens:
            tokens.append(AvAuthorization(token_str))
    return tokens

def env_avt_host() -> str:
    return env("AVT_HOST", "127.0.0.1")

def env_avt_verify_chain_dir() -> str:
    return env("AVT_VERIFY_CHAIN_DIR", default=os.path.join(os.path.abspath(os.sep), "AvesTerra", "Certificates"))

def avtc_init(
    max_socket_count: int = 2
):
    load_dotenv(find_dotenv())

    avt_host = env_avt_host()
    print(f"Info: Loaded avt_host as `{avt_host}`")

    avt_verify_chain_dir = env_avt_verify_chain_dir()
    print(f"Info: Loaded avt_verify_chain_dir as `{avt_verify_chain_dir}`")

    avt_tokens = env_avt_tokens()
    avt_tokens.append(AvAuthorization("00000000-0000-0000-0000-000000000001"))
    avt_tokens.append(AvAuthorization("00000000-0000-0000-0000-000000000002"))
    for token in avt_tokens:
        mac.include_auth_to_chain(authorization=token)
    print(f"Info: Loaded tokens `{avt_tokens}`")

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