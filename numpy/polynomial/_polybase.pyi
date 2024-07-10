import sys
from collections.abc import Iterator, Mapping, Sequence
from typing import (
    TYPE_CHECKING,
    Any,
    ClassVar,
    Literal,
    SupportsComplex,
    SupportsIndex,
    SupportsInt,
    TypeAlias,
    TypeGuard,
    TypeVar,
    overload,
)

import numpy as np
import numpy.typing as npt
from numpy._typing import _ArrayLikeInt_co

from ._polytypes import (
    _AnySeriesND,
    _Array1D,
    _AnyComplexSeriesND,
    _AnyObjectSeriesND,
    _AnyScalar,
    _AnySeries1D,
    _Interval,
    _CoefArray1D,
    _AnyNumberScalar,
    _SupportsLenAndGetItem,
    _Tuple2,
)

if sys.version_info >= (3, 11):
    from typing import LiteralString
elif TYPE_CHECKING:
    from typing_extensions import LiteralString
else:
    LiteralString: TypeAlias = str

__all__ = ["ABCPolyBase"]


_Self = TypeVar("_Self", bound="ABCPolyBase")
_Size = TypeVar("_Size", bound=int)

_AnyOther: TypeAlias = ABCPolyBase | _AnyScalar | _AnySeries1D
_Hundred: TypeAlias = Literal[100]

class ABCPolyBase:
    __hash__: ClassVar[None]  # type: ignore[assignment]
    __array_ufunc__: ClassVar[None]

    basis_name: ClassVar[None | LiteralString]
    maxpower: ClassVar[_Hundred]
    _superscript_mapping: ClassVar[Mapping[int, str]]
    _subscript_mapping: ClassVar[Mapping[int, str]]
    _use_unicode: ClassVar[bool]

    coef: _Array1D[np.number[Any]]
    domain: _Interval[Any]
    window: _Interval[Any]

    _symbol: LiteralString
    @property
    def symbol(self, /) -> LiteralString: ...

    def __init__(
        self,
        /,
        coef: _AnySeries1D,
        domain: None | _AnySeries1D = ...,
        window: None | _AnySeries1D = ...,
        symbol: str = ...,
    ) -> None: ...

    @overload
    def __call__(  # type: ignore[overload-overlap]
        self, /,
        arg: complex | np.complexfloating[Any, Any]
    ) -> np.complex128: ...
    @overload
    def __call__(
        self, /,
        arg: _AnyScalar,
    ) -> np.float64 | np.complex128: ...
    @overload
    def __call__(
        self, /,
        arg: _AnyObjectSeriesND,
    ) -> npt.NDArray[np.object_]: ...
    @overload
    def __call__(
        self, /,
        arg: _AnyComplexSeriesND,
    ) -> npt.NDArray[np.complex128 | np.object_]: ...
    @overload
    def __call__(
        self, /,
        arg: _AnySeries1D,
    ) -> npt.NDArray[np.float64 | np.complex128 | np.object_]: ...

    def __str__(self, /) -> str: ...
    def __repr__(self, /) -> str: ...
    def __format__(self, fmt_str: str, /) -> str: ...
    def __eq__(self, x: object, /) -> bool: ...
    def __ne__(self, x: object, /) -> bool: ...
    def __neg__(self: _Self, /) -> _Self: ...
    def __pos__(self: _Self, /) -> _Self: ...
    def __add__(self: _Self, x: _AnyOther, /) -> _Self: ...
    def __sub__(self: _Self, x: _AnyOther, /) -> _Self: ...
    def __mul__(self: _Self, x: _AnyOther, /) -> _Self: ...
    def __truediv__(self: _Self, x: _AnyOther, /) -> _Self: ...
    def __floordiv__(self: _Self, x: _AnyOther, /) -> _Self: ...
    def __mod__(self: _Self, x: _AnyOther, /) -> _Self: ...
    def __divmod__(self: _Self, x: _AnyOther, /) -> _Tuple2[_Self]: ...
    def __pow__(self: _Self, x: _AnyOther, /) -> _Self: ...
    def __radd__(self: _Self, x: _AnyOther, /) -> _Self: ...
    def __rsub__(self: _Self, x: _AnyOther, /) -> _Self: ...
    def __rmul__(self: _Self, x: _AnyOther, /) -> _Self: ...
    def __rdiv__(self: _Self, x: _AnyOther, /) -> _Self: ...
    def __rtruediv__(self: _Self, x: _AnyOther, /) -> _Self: ...
    def __rfloordiv__(self: _Self, x: _AnyOther, /) -> _Self: ...
    def __rmod__(self: _Self, x: _AnyOther, /) -> _Self: ...
    def __rdivmod__(self: _Self, x: _AnyOther, /) -> _Tuple2[_Self]: ...
    def __len__(self, /) -> int: ...
    def __iter__(self, /) -> Iterator[np.number[Any] | SupportsComplex]: ...
    def __getstate__(self, /) -> dict[str, Any]: ...
    def __setstate__(self, dict: dict[str, Any], /) -> None: ...

    def has_samecoef(self, /, other: ABCPolyBase) -> bool: ...
    def has_samedomain(self, /, other: ABCPolyBase) -> bool: ...
    def has_samewindow(self, /, other: ABCPolyBase) -> bool: ...
    def has_sametype(self: _Self, /, other: object) -> TypeGuard[_Self]: ...

    def copy(self: _Self, /) -> _Self: ...
    def degree(self, /) -> int: ...
    def cutdeg(self: _Self, /) -> _Self: ...
    def trim(self: _Self, /, tol: float = ...) -> _Self: ...
    def truncate(self: _Self, /, size: SupportsInt) -> _Self: ...

    @overload
    def convert(
        self,
        domain: None | _AnySeries1D,
        kind: type[_Self],
        /,
        window: None | _AnySeries1D = ...,
    ) -> _Self: ...
    @overload
    def convert(
        self,
        /,
        domain: None | _AnySeries1D = ...,
        *,
        kind: type[_Self],
        window: None | _AnySeries1D = ...,
    ) -> _Self: ...
    @overload
    def convert(
        self: _Self,
        /,
        domain: None | _AnySeries1D = ...,
        kind: type[_Self] = ...,
        window: None | _AnySeries1D = ...,
    ) -> _Self: ...

    def mapparms(self, /) -> _Tuple2[Any]: ...

    def integ(
        self: _Self,
        /,
        m: SupportsIndex = ...,
        k: _AnyNumberScalar | _SupportsLenAndGetItem[_AnyNumberScalar] = ...,
        lbnd: None | _AnyNumberScalar = ...,
    ) -> _Self: ...

    def deriv(self: _Self, /, m: SupportsIndex = ...) -> _Self: ...

    def roots(self, /) -> _CoefArray1D: ...

    @overload
    def linspace(
        self,
        /,
        n: _Size,
        domain: None | _AnySeries1D = ...,
    ) -> tuple[
        np.ndarray[tuple[_Size], np.dtype[np.float64]],
        np.ndarray[tuple[_Size], np.dtype[np.float64 | np.complex128]],
    ]: ...
    @overload
    def linspace(
        self,
        /,
        n: _Hundred = ...,
        domain: None | _AnySeries1D = ...,
    ) -> tuple[
        np.ndarray[tuple[_Hundred], np.dtype[np.float64]],
        np.ndarray[tuple[_Hundred], np.dtype[np.float64 | np.complex128]],
    ]: ...

    @overload
    @classmethod
    def fit(
        cls: type[_Self],
        /,
        x: _AnySeries1D,
        y: _AnySeries1D,
        deg: _ArrayLikeInt_co,
        domain: None | _AnySeries1D = ...,
        rcond: float = ...,
        full: Literal[False] = ...,
        w: None | _AnySeries1D = ...,
        window: None | _AnySeries1D = ...,
        symbol: str = ...,
    ) -> _Self: ...
    @overload
    @classmethod
    def fit(
        cls: type[_Self], /,
        x: _AnySeries1D,
        y: _AnySeries1D,
        deg: _ArrayLikeInt_co,
        domain: None | _AnySeries1D = ...,
        rcond: float = ...,
        *,
        full: Literal[True],
        w: None | _AnySeries1D = ...,
        window: None | _AnySeries1D = ...,
        symbol: str = ...,
    ) -> tuple[_Self, Sequence[np.inexact[Any] | np.int32]]: ...
    @overload
    @classmethod
    def fit(
        cls: type[_Self],
        x: _AnySeries1D,
        y: _AnySeries1D,
        deg: _ArrayLikeInt_co,
        domain: None | _AnySeries1D,
        rcond: float,
        full: Literal[True],
        /,
        w: None | _AnySeries1D = ...,
        window: None | _AnySeries1D = ...,
        symbol: str = ...,
    ) -> tuple[_Self, Sequence[np.inexact[Any] | np.int32]]: ...

    @classmethod
    def fromroots(
        cls: type[_Self],
        /,
        roots: _AnySeriesND,
        domain: None | _AnySeries1D = ...,
        window: None | _AnySeries1D = ...,
    ) -> _Self: ...

    @classmethod
    def identity(
        cls: type[_Self],
        /,
        domain: None | _AnySeries1D = ...,
        window: None | _AnySeries1D = ...,
    ) -> _Self: ...

    @classmethod
    def basis(
        cls: type[_Self],
        /,
        deg: int,
        domain: None | _AnySeries1D = ...,
        window: None | _AnySeries1D = ...,
    ) -> _Self: ...

    @classmethod
    def cast(
        cls: type[_Self],
        /,
        series: ABCPolyBase,
        domain: None | _AnySeries1D = ...,
        window: None | _AnySeries1D = ...,
    ) -> _Self: ...

    @classmethod
    def _str_term_unicode(cls, i: str, arg_str: str) -> str: ...
    @staticmethod
    def _str_term_ascii(i: str, arg_str: str) -> str: ...
    @staticmethod
    def _repr_latex_term(i: str, arg_str: str, needs_parens: bool) -> str: ...
