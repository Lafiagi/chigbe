# flake8: noqa
# fmt: off
# mypy: disable-error-code="no-any-return, no-untyped-call, misc, type-arg"
# This file was automatically generated by algokit-client-generator.
# DO NOT MODIFY IT BY HAND.
# requires: algokit-utils@^1.2.0
import base64
import dataclasses
import decimal
import typing
from abc import ABC, abstractmethod

import algokit_utils
import algosdk
from algosdk.v2client import models
from algosdk.atomic_transaction_composer import (
    AtomicTransactionComposer,
    AtomicTransactionResponse,
    SimulateAtomicTransactionResponse,
    TransactionSigner,
    TransactionWithSigner
)

_APP_SPEC_JSON = r"""{
    "hints": {
        "create_application(uint64,uint64,string,uint64,string,string)void": {
            "call_config": {
                "no_op": "CREATE"
            }
        },
        "authenticate_product(string)bool": {
            "call_config": {
                "no_op": "CALL"
            }
        }
    },
    "source": {
        "approval": "I3ByYWdtYSB2ZXJzaW9uIDEwCgpzbWFydF9jb250cmFjdHMuY2hpZ2JlLmNvbnRyYWN0LkNoaWdiZS5hcHByb3ZhbF9wcm9ncmFtOgogICAgaW50Y2Jsb2NrIDAgMQogICAgYnl0ZWNibG9jayAidW5pcXVlX2NvZGUiCiAgICBjYWxsc3ViIF9fcHV5YV9hcmM0X3JvdXRlcl9fCiAgICByZXR1cm4KCgovLyBzbWFydF9jb250cmFjdHMuY2hpZ2JlLmNvbnRyYWN0LkNoaWdiZS5fX3B1eWFfYXJjNF9yb3V0ZXJfXygpIC0+IHVpbnQ2NDoKX19wdXlhX2FyYzRfcm91dGVyX186CiAgICAvLyBzbWFydF9jb250cmFjdHMvY2hpZ2JlL2NvbnRyYWN0LnB5OjQKICAgIC8vIGNsYXNzIENoaWdiZShhcmM0LkFSQzRDb250cmFjdCk6CiAgICBwcm90byAwIDEKICAgIHR4biBOdW1BcHBBcmdzCiAgICBieiBfX3B1eWFfYXJjNF9yb3V0ZXJfX19hZnRlcl9pZl9lbHNlQDcKICAgIHB1c2hieXRlc3MgMHhlYjQ4MjJhNCAweGZmYTkyZDYxIC8vIG1ldGhvZCAiY3JlYXRlX2FwcGxpY2F0aW9uKHVpbnQ2NCx1aW50NjQsc3RyaW5nLHVpbnQ2NCxzdHJpbmcsc3RyaW5nKXZvaWQiLCBtZXRob2QgImF1dGhlbnRpY2F0ZV9wcm9kdWN0KHN0cmluZylib29sIgogICAgdHhuYSBBcHBsaWNhdGlvbkFyZ3MgMAogICAgbWF0Y2ggX19wdXlhX2FyYzRfcm91dGVyX19fY3JlYXRlX2FwcGxpY2F0aW9uX3JvdXRlQDIgX19wdXlhX2FyYzRfcm91dGVyX19fYXV0aGVudGljYXRlX3Byb2R1Y3Rfcm91dGVAMwogICAgaW50Y18wIC8vIDAKICAgIHJldHN1YgoKX19wdXlhX2FyYzRfcm91dGVyX19fY3JlYXRlX2FwcGxpY2F0aW9uX3JvdXRlQDI6CiAgICAvLyBzbWFydF9jb250cmFjdHMvY2hpZ2JlL2NvbnRyYWN0LnB5OjE0CiAgICAvLyBAYXJjNC5hYmltZXRob2QoYWxsb3dfYWN0aW9ucz1bIk5vT3AiXSwgY3JlYXRlPSJyZXF1aXJlIikKICAgIHR4biBPbkNvbXBsZXRpb24KICAgICEKICAgIGFzc2VydCAvLyBPbkNvbXBsZXRpb24gaXMgTm9PcAogICAgdHhuIEFwcGxpY2F0aW9uSUQKICAgICEKICAgIGFzc2VydCAvLyBpcyBjcmVhdGluZwogICAgLy8gc21hcnRfY29udHJhY3RzL2NoaWdiZS9jb250cmFjdC5weTo0CiAgICAvLyBjbGFzcyBDaGlnYmUoYXJjNC5BUkM0Q29udHJhY3QpOgogICAgdHhuYSBBcHBsaWNhdGlvbkFyZ3MgMQogICAgYnRvaQogICAgdHhuYSBBcHBsaWNhdGlvbkFyZ3MgMgogICAgYnRvaQogICAgdHhuYSBBcHBsaWNhdGlvbkFyZ3MgMwogICAgZXh0cmFjdCAyIDAKICAgIHR4bmEgQXBwbGljYXRpb25BcmdzIDQKICAgIGJ0b2kKICAgIHR4bmEgQXBwbGljYXRpb25BcmdzIDUKICAgIGV4dHJhY3QgMiAwCiAgICB0eG5hIEFwcGxpY2F0aW9uQXJncyA2CiAgICBleHRyYWN0IDIgMAogICAgLy8gc21hcnRfY29udHJhY3RzL2NoaWdiZS9jb250cmFjdC5weToxNAogICAgLy8gQGFyYzQuYWJpbWV0aG9kKGFsbG93X2FjdGlvbnM9WyJOb09wIl0sIGNyZWF0ZT0icmVxdWlyZSIpCiAgICBjYWxsc3ViIGNyZWF0ZV9hcHBsaWNhdGlvbgogICAgaW50Y18xIC8vIDEKICAgIHJldHN1YgoKX19wdXlhX2FyYzRfcm91dGVyX19fYXV0aGVudGljYXRlX3Byb2R1Y3Rfcm91dGVAMzoKICAgIC8vIHNtYXJ0X2NvbnRyYWN0cy9jaGlnYmUvY29udHJhY3QucHk6MzEKICAgIC8vIEBhcmM0LmFiaW1ldGhvZAogICAgdHhuIE9uQ29tcGxldGlvbgogICAgIQogICAgYXNzZXJ0IC8vIE9uQ29tcGxldGlvbiBpcyBOb09wCiAgICB0eG4gQXBwbGljYXRpb25JRAogICAgYXNzZXJ0IC8vIGlzIG5vdCBjcmVhdGluZwogICAgLy8gc21hcnRfY29udHJhY3RzL2NoaWdiZS9jb250cmFjdC5weTo0CiAgICAvLyBjbGFzcyBDaGlnYmUoYXJjNC5BUkM0Q29udHJhY3QpOgogICAgdHhuYSBBcHBsaWNhdGlvbkFyZ3MgMQogICAgZXh0cmFjdCAyIDAKICAgIC8vIHNtYXJ0X2NvbnRyYWN0cy9jaGlnYmUvY29udHJhY3QucHk6MzEKICAgIC8vIEBhcmM0LmFiaW1ldGhvZAogICAgY2FsbHN1YiBhdXRoZW50aWNhdGVfcHJvZHVjdAogICAgcHVzaGJ5dGVzIDB4MDAKICAgIGludGNfMCAvLyAwCiAgICB1bmNvdmVyIDIKICAgIHNldGJpdAogICAgcHVzaGJ5dGVzIDB4MTUxZjdjNzUKICAgIHN3YXAKICAgIGNvbmNhdAogICAgbG9nCiAgICBpbnRjXzEgLy8gMQogICAgcmV0c3ViCgpfX3B1eWFfYXJjNF9yb3V0ZXJfX19hZnRlcl9pZl9lbHNlQDc6CiAgICAvLyBzbWFydF9jb250cmFjdHMvY2hpZ2JlL2NvbnRyYWN0LnB5OjQKICAgIC8vIGNsYXNzIENoaWdiZShhcmM0LkFSQzRDb250cmFjdCk6CiAgICBpbnRjXzAgLy8gMAogICAgcmV0c3ViCgoKLy8gc21hcnRfY29udHJhY3RzLmNoaWdiZS5jb250cmFjdC5DaGlnYmUuY3JlYXRlX2FwcGxpY2F0aW9uKG1hbnVmYWN0dXJlX2RhdGU6IHVpbnQ2NCwgZXhwaXJ5X2RhdGU6IHVpbnQ2NCwgdW5pcXVlX2NvZGU6IGJ5dGVzLCBhc3NldF9pZDogdWludDY0LCBiYXRjaF9udW1iZXI6IGJ5dGVzLCBtYW51ZmFjdHVyZXI6IGJ5dGVzKSAtPiB2b2lkOgpjcmVhdGVfYXBwbGljYXRpb246CiAgICAvLyBzbWFydF9jb250cmFjdHMvY2hpZ2JlL2NvbnRyYWN0LnB5OjE0LTIzCiAgICAvLyBAYXJjNC5hYmltZXRob2QoYWxsb3dfYWN0aW9ucz1bIk5vT3AiXSwgY3JlYXRlPSJyZXF1aXJlIikKICAgIC8vIGRlZiBjcmVhdGVfYXBwbGljYXRpb24oCiAgICAvLyAgICAgc2VsZiwKICAgIC8vICAgICBtYW51ZmFjdHVyZV9kYXRlOiBVSW50NjQsCiAgICAvLyAgICAgZXhwaXJ5X2RhdGU6IFVJbnQ2NCwKICAgIC8vICAgICB1bmlxdWVfY29kZTogU3RyaW5nLAogICAgLy8gICAgIGFzc2V0X2lkOiBVSW50NjQsCiAgICAvLyAgICAgYmF0Y2hfbnVtYmVyOiBTdHJpbmcsCiAgICAvLyAgICAgbWFudWZhY3R1cmVyOiBTdHJpbmcsCiAgICAvLyApIC0+IE5vbmU6CiAgICBwcm90byA2IDAKICAgIC8vIHNtYXJ0X2NvbnRyYWN0cy9jaGlnYmUvY29udHJhY3QucHk6MjQKICAgIC8vIHNlbGYuYXNzZXRfaWQgPSBhc3NldF9pZAogICAgcHVzaGJ5dGVzICJhc3NldF9pZCIKICAgIGZyYW1lX2RpZyAtMwogICAgYXBwX2dsb2JhbF9wdXQKICAgIC8vIHNtYXJ0X2NvbnRyYWN0cy9jaGlnYmUvY29udHJhY3QucHk6MjUKICAgIC8vIHNlbGYuZXhwaXJ5X2RhdGUgPSBleHBpcnlfZGF0ZQogICAgcHVzaGJ5dGVzICJleHBpcnlfZGF0ZSIKICAgIGZyYW1lX2RpZyAtNQogICAgYXBwX2dsb2JhbF9wdXQKICAgIC8vIHNtYXJ0X2NvbnRyYWN0cy9jaGlnYmUvY29udHJhY3QucHk6MjYKICAgIC8vIHNlbGYudW5pcXVlX2NvZGUgPSB1bmlxdWVfY29kZQogICAgYnl0ZWNfMCAvLyAidW5pcXVlX2NvZGUiCiAgICBmcmFtZV9kaWcgLTQKICAgIGFwcF9nbG9iYWxfcHV0CiAgICAvLyBzbWFydF9jb250cmFjdHMvY2hpZ2JlL2NvbnRyYWN0LnB5OjI3CiAgICAvLyBzZWxmLm1hbnVmYWN0dXJlX2RhdGUgPSBtYW51ZmFjdHVyZV9kYXRlCiAgICBwdXNoYnl0ZXMgIm1hbnVmYWN0dXJlX2RhdGUiCiAgICBmcmFtZV9kaWcgLTYKICAgIGFwcF9nbG9iYWxfcHV0CiAgICAvLyBzbWFydF9jb250cmFjdHMvY2hpZ2JlL2NvbnRyYWN0LnB5OjI4CiAgICAvLyBzZWxmLmJhdGNoX251bWJlciA9IGJhdGNoX251bWJlcgogICAgcHVzaGJ5dGVzICJiYXRjaF9udW1iZXIiCiAgICBmcmFtZV9kaWcgLTIKICAgIGFwcF9nbG9iYWxfcHV0CiAgICAvLyBzbWFydF9jb250cmFjdHMvY2hpZ2JlL2NvbnRyYWN0LnB5OjI5CiAgICAvLyBzZWxmLm1hbnVmYWN0dXJlciA9IG1hbnVmYWN0dXJlcgogICAgcHVzaGJ5dGVzICJtYW51ZmFjdHVyZXIiCiAgICBmcmFtZV9kaWcgLTEKICAgIGFwcF9nbG9iYWxfcHV0CiAgICByZXRzdWIKCgovLyBzbWFydF9jb250cmFjdHMuY2hpZ2JlLmNvbnRyYWN0LkNoaWdiZS5hdXRoZW50aWNhdGVfcHJvZHVjdCh1bmlxdWVfY29kZTogYnl0ZXMpIC0+IHVpbnQ2NDoKYXV0aGVudGljYXRlX3Byb2R1Y3Q6CiAgICAvLyBzbWFydF9jb250cmFjdHMvY2hpZ2JlL2NvbnRyYWN0LnB5OjMxLTMyCiAgICAvLyBAYXJjNC5hYmltZXRob2QKICAgIC8vIGRlZiBhdXRoZW50aWNhdGVfcHJvZHVjdChzZWxmLCB1bmlxdWVfY29kZTogU3RyaW5nKSAtPiBib29sOgogICAgcHJvdG8gMSAxCiAgICAvLyBzbWFydF9jb250cmFjdHMvY2hpZ2JlL2NvbnRyYWN0LnB5OjMzLTM0CiAgICAvLyAjIGNoZWNrIGlmIHRoZSB1bmlxdWUgY29kZSBpcyB2YWxpZCBmb3IgdGhlIHNtYXJ0IGNvbnRyYWN0CiAgICAvLyByZXR1cm4gc2VsZi51bmlxdWVfY29kZSA9PSB1bmlxdWVfY29kZQogICAgaW50Y18wIC8vIDAKICAgIGJ5dGVjXzAgLy8gInVuaXF1ZV9jb2RlIgogICAgYXBwX2dsb2JhbF9nZXRfZXgKICAgIGFzc2VydCAvLyBjaGVjayBzZWxmLnVuaXF1ZV9jb2RlIGV4aXN0cwogICAgZnJhbWVfZGlnIC0xCiAgICA9PQogICAgcmV0c3ViCg==",
        "clear": "I3ByYWdtYSB2ZXJzaW9uIDEwCgpzbWFydF9jb250cmFjdHMuY2hpZ2JlLmNvbnRyYWN0LkNoaWdiZS5jbGVhcl9zdGF0ZV9wcm9ncmFtOgogICAgcHVzaGludCAxIC8vIDEKICAgIHJldHVybgo="
    },
    "state": {
        "global": {
            "num_byte_slices": 5,
            "num_uints": 3
        },
        "local": {
            "num_byte_slices": 0,
            "num_uints": 0
        }
    },
    "schema": {
        "global": {
            "declared": {
                "asset_id": {
                    "type": "uint64",
                    "key": "asset_id"
                },
                "batch_number": {
                    "type": "bytes",
                    "key": "batch_number"
                },
                "expiry_date": {
                    "type": "uint64",
                    "key": "expiry_date"
                },
                "manufacture_date": {
                    "type": "uint64",
                    "key": "manufacture_date"
                },
                "manufacturer": {
                    "type": "bytes",
                    "key": "manufacturer"
                },
                "name": {
                    "type": "bytes",
                    "key": "name"
                },
                "owner": {
                    "type": "bytes",
                    "key": "owner"
                },
                "unique_code": {
                    "type": "bytes",
                    "key": "unique_code"
                }
            },
            "reserved": {}
        },
        "local": {
            "declared": {},
            "reserved": {}
        }
    },
    "contract": {
        "name": "Chigbe",
        "methods": [
            {
                "name": "create_application",
                "args": [
                    {
                        "type": "uint64",
                        "name": "manufacture_date"
                    },
                    {
                        "type": "uint64",
                        "name": "expiry_date"
                    },
                    {
                        "type": "string",
                        "name": "unique_code"
                    },
                    {
                        "type": "uint64",
                        "name": "asset_id"
                    },
                    {
                        "type": "string",
                        "name": "batch_number"
                    },
                    {
                        "type": "string",
                        "name": "manufacturer"
                    }
                ],
                "returns": {
                    "type": "void"
                }
            },
            {
                "name": "authenticate_product",
                "args": [
                    {
                        "type": "string",
                        "name": "unique_code"
                    }
                ],
                "returns": {
                    "type": "bool"
                }
            }
        ],
        "networks": {}
    },
    "bare_call_config": {}
}"""
APP_SPEC = algokit_utils.ApplicationSpecification.from_json(_APP_SPEC_JSON)
_TReturn = typing.TypeVar("_TReturn")


class _ArgsBase(ABC, typing.Generic[_TReturn]):
    @staticmethod
    @abstractmethod
    def method() -> str:
        ...


_TArgs = typing.TypeVar("_TArgs", bound=_ArgsBase[typing.Any])


@dataclasses.dataclass(kw_only=True)
class _TArgsHolder(typing.Generic[_TArgs]):
    args: _TArgs


@dataclasses.dataclass(kw_only=True)
class DeployCreate(algokit_utils.DeployCreateCallArgs, _TArgsHolder[_TArgs], typing.Generic[_TArgs]):
    pass


def _filter_none(value: dict | typing.Any) -> dict | typing.Any:
    if isinstance(value, dict):
        return {k: _filter_none(v) for k, v in value.items() if v is not None}
    return value


def _as_dict(data: typing.Any, *, convert_all: bool = True) -> dict[str, typing.Any]:
    if data is None:
        return {}
    if not dataclasses.is_dataclass(data):
        raise TypeError(f"{data} must be a dataclass")
    if convert_all:
        result = dataclasses.asdict(data) # type: ignore[call-overload]
    else:
        result = {f.name: getattr(data, f.name) for f in dataclasses.fields(data)}
    return _filter_none(result)


def _convert_transaction_parameters(
    transaction_parameters: algokit_utils.TransactionParameters | None,
) -> algokit_utils.TransactionParametersDict:
    return typing.cast(algokit_utils.TransactionParametersDict, _as_dict(transaction_parameters))


def _convert_call_transaction_parameters(
    transaction_parameters: algokit_utils.TransactionParameters | None,
) -> algokit_utils.OnCompleteCallParametersDict:
    return typing.cast(algokit_utils.OnCompleteCallParametersDict, _as_dict(transaction_parameters))


def _convert_create_transaction_parameters(
    transaction_parameters: algokit_utils.TransactionParameters | None,
    on_complete: algokit_utils.OnCompleteActionName,
) -> algokit_utils.CreateCallParametersDict:
    result = typing.cast(algokit_utils.CreateCallParametersDict, _as_dict(transaction_parameters))
    on_complete_enum = on_complete.replace("_", " ").title().replace(" ", "") + "OC"
    result["on_complete"] = getattr(algosdk.transaction.OnComplete, on_complete_enum)
    return result


def _convert_deploy_args(
    deploy_args: algokit_utils.DeployCallArgs | None,
) -> algokit_utils.ABICreateCallArgsDict | None:
    if deploy_args is None:
        return None

    deploy_args_dict = typing.cast(algokit_utils.ABICreateCallArgsDict, _as_dict(deploy_args))
    if isinstance(deploy_args, _TArgsHolder):
        deploy_args_dict["args"] = _as_dict(deploy_args.args)
        deploy_args_dict["method"] = deploy_args.args.method()

    return deploy_args_dict


@dataclasses.dataclass(kw_only=True)
class AuthenticateProductArgs(_ArgsBase[bool]):
    unique_code: str

    @staticmethod
    def method() -> str:
        return "authenticate_product(string)bool"


@dataclasses.dataclass(kw_only=True)
class CreateApplicationArgs(_ArgsBase[None]):
    manufacture_date: int
    expiry_date: int
    unique_code: str
    asset_id: int
    batch_number: str
    manufacturer: str

    @staticmethod
    def method() -> str:
        return "create_application(uint64,uint64,string,uint64,string,string)void"


class ByteReader:
    def __init__(self, data: bytes):
        self._data = data

    @property
    def as_bytes(self) -> bytes:
        return self._data

    @property
    def as_str(self) -> str:
        return self._data.decode("utf8")

    @property
    def as_base64(self) -> str:
        return base64.b64encode(self._data).decode("utf8")

    @property
    def as_hex(self) -> str:
        return self._data.hex()


class GlobalState:
    def __init__(self, data: dict[bytes, bytes | int]):
        self.asset_id = typing.cast(int, data.get(b"asset_id"))
        self.batch_number = ByteReader(typing.cast(bytes, data.get(b"batch_number")))
        self.expiry_date = typing.cast(int, data.get(b"expiry_date"))
        self.manufacture_date = typing.cast(int, data.get(b"manufacture_date"))
        self.manufacturer = ByteReader(typing.cast(bytes, data.get(b"manufacturer")))
        self.name = ByteReader(typing.cast(bytes, data.get(b"name")))
        self.owner = ByteReader(typing.cast(bytes, data.get(b"owner")))
        self.unique_code = ByteReader(typing.cast(bytes, data.get(b"unique_code")))


@dataclasses.dataclass(kw_only=True)
class SimulateOptions:
    allow_more_logs: bool = dataclasses.field(default=False)
    allow_empty_signatures: bool = dataclasses.field(default=False)
    extra_opcode_budget: int = dataclasses.field(default=0)
    exec_trace_config: models.SimulateTraceConfig | None         = dataclasses.field(default=None)


class Composer:

    def __init__(self, app_client: algokit_utils.ApplicationClient, atc: AtomicTransactionComposer):
        self.app_client = app_client
        self.atc = atc

    def build(self) -> AtomicTransactionComposer:
        return self.atc

    def simulate(self, options: SimulateOptions | None = None) -> SimulateAtomicTransactionResponse:
        request = models.SimulateRequest(
            allow_more_logs=options.allow_more_logs,
            allow_empty_signatures=options.allow_empty_signatures,
            extra_opcode_budget=options.extra_opcode_budget,
            exec_trace_config=options.exec_trace_config,
            txn_groups=[]
        ) if options else None
        result = self.atc.simulate(self.app_client.algod_client, request)
        return result

    def execute(self) -> AtomicTransactionResponse:
        return self.app_client.execute_atc(self.atc)

    def authenticate_product(
        self,
        *,
        unique_code: str,
        transaction_parameters: algokit_utils.TransactionParameters | None = None,
    ) -> "Composer":
        """Adds a call to `authenticate_product(string)bool` ABI method
        
        :param str unique_code: The `unique_code` ABI parameter
        :param algokit_utils.TransactionParameters transaction_parameters: (optional) Additional transaction parameters
        :returns Composer: This Composer instance"""

        args = AuthenticateProductArgs(
            unique_code=unique_code,
        )
        self.app_client.compose_call(
            self.atc,
            call_abi_method=args.method(),
            transaction_parameters=_convert_call_transaction_parameters(transaction_parameters),
            **_as_dict(args, convert_all=True),
        )
        return self

    def create_create_application(
        self,
        *,
        manufacture_date: int,
        expiry_date: int,
        unique_code: str,
        asset_id: int,
        batch_number: str,
        manufacturer: str,
        on_complete: typing.Literal["no_op"] = "no_op",
        transaction_parameters: algokit_utils.CreateTransactionParameters | None = None,
    ) -> "Composer":
        """Adds a call to `create_application(uint64,uint64,string,uint64,string,string)void` ABI method
        
        :param int manufacture_date: The `manufacture_date` ABI parameter
        :param int expiry_date: The `expiry_date` ABI parameter
        :param str unique_code: The `unique_code` ABI parameter
        :param int asset_id: The `asset_id` ABI parameter
        :param str batch_number: The `batch_number` ABI parameter
        :param str manufacturer: The `manufacturer` ABI parameter
        :param typing.Literal[no_op] on_complete: On completion type to use
        :param algokit_utils.CreateTransactionParameters transaction_parameters: (optional) Additional transaction parameters
        :returns Composer: This Composer instance"""

        args = CreateApplicationArgs(
            manufacture_date=manufacture_date,
            expiry_date=expiry_date,
            unique_code=unique_code,
            asset_id=asset_id,
            batch_number=batch_number,
            manufacturer=manufacturer,
        )
        self.app_client.compose_create(
            self.atc,
            call_abi_method=args.method(),
            transaction_parameters=_convert_create_transaction_parameters(transaction_parameters, on_complete),
            **_as_dict(args, convert_all=True),
        )
        return self

    def clear_state(
        self,
        transaction_parameters: algokit_utils.TransactionParameters | None = None,
        app_args: list[bytes] | None = None,
    ) -> "Composer":
        """Adds a call to the application with on completion set to ClearState
    
        :param algokit_utils.TransactionParameters transaction_parameters: (optional) Additional transaction parameters
        :param list[bytes] | None app_args: (optional) Application args to pass"""
    
        self.app_client.compose_clear_state(self.atc, _convert_transaction_parameters(transaction_parameters), app_args)
        return self


class ChigbeClient:
    """A class for interacting with the Chigbe app providing high productivity and
    strongly typed methods to deploy and call the app"""

    @typing.overload
    def __init__(
        self,
        algod_client: algosdk.v2client.algod.AlgodClient,
        *,
        app_id: int = 0,
        signer: TransactionSigner | algokit_utils.Account | None = None,
        sender: str | None = None,
        suggested_params: algosdk.transaction.SuggestedParams | None = None,
        template_values: algokit_utils.TemplateValueMapping | None = None,
        app_name: str | None = None,
    ) -> None:
        ...

    @typing.overload
    def __init__(
        self,
        algod_client: algosdk.v2client.algod.AlgodClient,
        *,
        creator: str | algokit_utils.Account,
        indexer_client: algosdk.v2client.indexer.IndexerClient | None = None,
        existing_deployments: algokit_utils.AppLookup | None = None,
        signer: TransactionSigner | algokit_utils.Account | None = None,
        sender: str | None = None,
        suggested_params: algosdk.transaction.SuggestedParams | None = None,
        template_values: algokit_utils.TemplateValueMapping | None = None,
        app_name: str | None = None,
    ) -> None:
        ...

    def __init__(
        self,
        algod_client: algosdk.v2client.algod.AlgodClient,
        *,
        creator: str | algokit_utils.Account | None = None,
        indexer_client: algosdk.v2client.indexer.IndexerClient | None = None,
        existing_deployments: algokit_utils.AppLookup | None = None,
        app_id: int = 0,
        signer: TransactionSigner | algokit_utils.Account | None = None,
        sender: str | None = None,
        suggested_params: algosdk.transaction.SuggestedParams | None = None,
        template_values: algokit_utils.TemplateValueMapping | None = None,
        app_name: str | None = None,
    ) -> None:
        """
        ChigbeClient can be created with an app_id to interact with an existing application, alternatively
        it can be created with a creator and indexer_client specified to find existing applications by name and creator.
        
        :param AlgodClient algod_client: AlgoSDK algod client
        :param int app_id: The app_id of an existing application, to instead find the application by creator and name
        use the creator and indexer_client parameters
        :param str | Account creator: The address or Account of the app creator to resolve the app_id
        :param IndexerClient indexer_client: AlgoSDK indexer client, only required if deploying or finding app_id by
        creator and app name
        :param AppLookup existing_deployments:
        :param TransactionSigner | Account signer: Account or signer to use to sign transactions, if not specified and
        creator was passed as an Account will use that.
        :param str sender: Address to use as the sender for all transactions, will use the address associated with the
        signer if not specified.
        :param TemplateValueMapping template_values: Values to use for TMPL_* template variables, dictionary keys should
        *NOT* include the TMPL_ prefix
        :param str | None app_name: Name of application to use when deploying, defaults to name defined on the
        Application Specification
            """

        self.app_spec = APP_SPEC
        
        # calling full __init__ signature, so ignoring mypy warning about overloads
        self.app_client = algokit_utils.ApplicationClient(  # type: ignore[call-overload, misc]
            algod_client=algod_client,
            app_spec=self.app_spec,
            app_id=app_id,
            creator=creator,
            indexer_client=indexer_client,
            existing_deployments=existing_deployments,
            signer=signer,
            sender=sender,
            suggested_params=suggested_params,
            template_values=template_values,
            app_name=app_name,
        )

    @property
    def algod_client(self) -> algosdk.v2client.algod.AlgodClient:
        return self.app_client.algod_client

    @property
    def app_id(self) -> int:
        return self.app_client.app_id

    @app_id.setter
    def app_id(self, value: int) -> None:
        self.app_client.app_id = value

    @property
    def app_address(self) -> str:
        return self.app_client.app_address

    @property
    def sender(self) -> str | None:
        return self.app_client.sender

    @sender.setter
    def sender(self, value: str) -> None:
        self.app_client.sender = value

    @property
    def signer(self) -> TransactionSigner | None:
        return self.app_client.signer

    @signer.setter
    def signer(self, value: TransactionSigner) -> None:
        self.app_client.signer = value

    @property
    def suggested_params(self) -> algosdk.transaction.SuggestedParams | None:
        return self.app_client.suggested_params

    @suggested_params.setter
    def suggested_params(self, value: algosdk.transaction.SuggestedParams | None) -> None:
        self.app_client.suggested_params = value

    def get_global_state(self) -> GlobalState:
        """Returns the application's global state wrapped in a strongly typed class with options to format the stored value"""

        state = typing.cast(dict[bytes, bytes | int], self.app_client.get_global_state(raw=True))
        return GlobalState(state)

    def authenticate_product(
        self,
        *,
        unique_code: str,
        transaction_parameters: algokit_utils.TransactionParameters | None = None,
    ) -> algokit_utils.ABITransactionResponse[bool]:
        """Calls `authenticate_product(string)bool` ABI method
        
        :param str unique_code: The `unique_code` ABI parameter
        :param algokit_utils.TransactionParameters transaction_parameters: (optional) Additional transaction parameters
        :returns algokit_utils.ABITransactionResponse[bool]: The result of the transaction"""

        args = AuthenticateProductArgs(
            unique_code=unique_code,
        )
        result = self.app_client.call(
            call_abi_method=args.method(),
            transaction_parameters=_convert_call_transaction_parameters(transaction_parameters),
            **_as_dict(args, convert_all=True),
        )
        return result

    def create_create_application(
        self,
        *,
        manufacture_date: int,
        expiry_date: int,
        unique_code: str,
        asset_id: int,
        batch_number: str,
        manufacturer: str,
        on_complete: typing.Literal["no_op"] = "no_op",
        transaction_parameters: algokit_utils.CreateTransactionParameters | None = None,
    ) -> algokit_utils.ABITransactionResponse[None]:
        """Calls `create_application(uint64,uint64,string,uint64,string,string)void` ABI method
        
        :param int manufacture_date: The `manufacture_date` ABI parameter
        :param int expiry_date: The `expiry_date` ABI parameter
        :param str unique_code: The `unique_code` ABI parameter
        :param int asset_id: The `asset_id` ABI parameter
        :param str batch_number: The `batch_number` ABI parameter
        :param str manufacturer: The `manufacturer` ABI parameter
        :param typing.Literal[no_op] on_complete: On completion type to use
        :param algokit_utils.CreateTransactionParameters transaction_parameters: (optional) Additional transaction parameters
        :returns algokit_utils.ABITransactionResponse[None]: The result of the transaction"""

        args = CreateApplicationArgs(
            manufacture_date=manufacture_date,
            expiry_date=expiry_date,
            unique_code=unique_code,
            asset_id=asset_id,
            batch_number=batch_number,
            manufacturer=manufacturer,
        )
        result = self.app_client.create(
            call_abi_method=args.method(),
            transaction_parameters=_convert_create_transaction_parameters(transaction_parameters, on_complete),
            **_as_dict(args, convert_all=True),
        )
        return result

    def clear_state(
        self,
        transaction_parameters: algokit_utils.TransactionParameters | None = None,
        app_args: list[bytes] | None = None,
    ) -> algokit_utils.TransactionResponse:
        """Calls the application with on completion set to ClearState
    
        :param algokit_utils.TransactionParameters transaction_parameters: (optional) Additional transaction parameters
        :param list[bytes] | None app_args: (optional) Application args to pass
        :returns algokit_utils.TransactionResponse: The result of the transaction"""
    
        return self.app_client.clear_state(_convert_transaction_parameters(transaction_parameters), app_args)

    def deploy(
        self,
        version: str | None = None,
        *,
        signer: TransactionSigner | None = None,
        sender: str | None = None,
        allow_update: bool | None = None,
        allow_delete: bool | None = None,
        on_update: algokit_utils.OnUpdate = algokit_utils.OnUpdate.Fail,
        on_schema_break: algokit_utils.OnSchemaBreak = algokit_utils.OnSchemaBreak.Fail,
        template_values: algokit_utils.TemplateValueMapping | None = None,
        create_args: DeployCreate[CreateApplicationArgs],
        update_args: algokit_utils.DeployCallArgs | None = None,
        delete_args: algokit_utils.DeployCallArgs | None = None,
    ) -> algokit_utils.DeployResponse:
        """Deploy an application and update client to reference it.
        
        Idempotently deploy (create, update/delete if changed) an app against the given name via the given creator
        account, including deploy-time template placeholder substitutions.
        To understand the architecture decisions behind this functionality please see
        <https://github.com/algorandfoundation/algokit-cli/blob/main/docs/architecture-decisions/2023-01-12_smart-contract-deployment.md>
        
        ```{note}
        If there is a breaking state schema change to an existing app (and `on_schema_break` is set to
        'ReplaceApp' the existing app will be deleted and re-created.
        ```
        
        ```{note}
        If there is an update (different TEAL code) to an existing app (and `on_update` is set to 'ReplaceApp')
        the existing app will be deleted and re-created.
        ```
        
        :param str version: version to use when creating or updating app, if None version will be auto incremented
        :param algosdk.atomic_transaction_composer.TransactionSigner signer: signer to use when deploying app
        , if None uses self.signer
        :param str sender: sender address to use when deploying app, if None uses self.sender
        :param bool allow_delete: Used to set the `TMPL_DELETABLE` template variable to conditionally control if an app
        can be deleted
        :param bool allow_update: Used to set the `TMPL_UPDATABLE` template variable to conditionally control if an app
        can be updated
        :param OnUpdate on_update: Determines what action to take if an application update is required
        :param OnSchemaBreak on_schema_break: Determines what action to take if an application schema requirements
        has increased beyond the current allocation
        :param dict[str, int|str|bytes] template_values: Values to use for `TMPL_*` template variables, dictionary keys
        should *NOT* include the TMPL_ prefix
        :param DeployCreate[CreateApplicationArgs] create_args: Arguments used when creating an application
        :param algokit_utils.DeployCallArgs | None update_args: Arguments used when updating an application
        :param algokit_utils.DeployCallArgs | None delete_args: Arguments used when deleting an application
        :return DeployResponse: details action taken and relevant transactions
        :raises DeploymentError: If the deployment failed"""

        return self.app_client.deploy(
            version,
            signer=signer,
            sender=sender,
            allow_update=allow_update,
            allow_delete=allow_delete,
            on_update=on_update,
            on_schema_break=on_schema_break,
            template_values=template_values,
            create_args=_convert_deploy_args(create_args),
            update_args=_convert_deploy_args(update_args),
            delete_args=_convert_deploy_args(delete_args),
        )

    def compose(self, atc: AtomicTransactionComposer | None = None) -> Composer:
        return Composer(self.app_client, atc or AtomicTransactionComposer())