from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ConversationalRequest(_message.Message):
    __slots__ = ("session_uuid", "input")
    SESSION_UUID_FIELD_NUMBER: _ClassVar[int]
    INPUT_FIELD_NUMBER: _ClassVar[int]
    session_uuid: str
    input: str
    def __init__(self, session_uuid: _Optional[str] = ..., input: _Optional[str] = ...) -> None: ...

class ConversationalResponse(_message.Message):
    __slots__ = ("status", "token")
    class Status(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        UKNOWN: _ClassVar[ConversationalResponse.Status]
        LOAD_HISTORY: _ClassVar[ConversationalResponse.Status]
        BUILD_PROMPT: _ClassVar[ConversationalResponse.Status]
        GENERATE_RESPONSE: _ClassVar[ConversationalResponse.Status]
        UPDATE_MEMORY: _ClassVar[ConversationalResponse.Status]
        FINISHED: _ClassVar[ConversationalResponse.Status]
        FAILED: _ClassVar[ConversationalResponse.Status]
    UKNOWN: ConversationalResponse.Status
    LOAD_HISTORY: ConversationalResponse.Status
    BUILD_PROMPT: ConversationalResponse.Status
    GENERATE_RESPONSE: ConversationalResponse.Status
    UPDATE_MEMORY: ConversationalResponse.Status
    FINISHED: ConversationalResponse.Status
    FAILED: ConversationalResponse.Status
    STATUS_FIELD_NUMBER: _ClassVar[int]
    TOKEN_FIELD_NUMBER: _ClassVar[int]
    status: ConversationalResponse.Status
    token: str
    def __init__(self, status: _Optional[_Union[ConversationalResponse.Status, str]] = ..., token: _Optional[str] = ...) -> None: ...
