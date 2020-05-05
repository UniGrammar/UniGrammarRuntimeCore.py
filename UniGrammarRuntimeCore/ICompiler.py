import typing
from abc import ABC, abstractmethod
from pathlib import Path


class ICompiler(ABC):
	"""Just a base class for compilers compiling grammars DSLs into objects."""

	__slots__ = ()

	@abstractmethod
	def compileStr(self, grammarText: str, target: typing.Any = None, fileName: typing.Optional[typing.Union[Path, str]] = None):
		"""Parses the DSL string and generates internal object from it. `fileName` must not be used for retrieving source, instead it must provide hints, useful for caching or more meaningful error messages and may be just ignored if the backend doesn't support its usage this way."""
		raise NotImplementedError

	def compileFile(self, grammarFile: Path, target: typing.Any = None):
		"""Parses the DSL file and generates internal object from it. May be better because of caching, lower memory overhead and more meaningful error messages."""
		return self.compileStr(grammarFile.read_text(encoding="utf-8"), target, fileName=grammarFile)

	def compile(self, grammar: typing.Union[Path, str], target: typing.Any = None, fileName: typing.Optional[typing.Union[Path, str]] = None):
		"""Just a convenience method dispatching between `compileStr` and `compileFile`"""
		if isinstance(grammar, Path):
			assert fileName is None
			return self.compileFile(grammar, target)
		return self.compileStr(grammar, target, grammar)


class DummyCompiler(ICompiler):
	"""Returns text as a string"""
	__slots__ = ()

	def compileStr(self, grammarText: str, target: typing.Any = None, fileName: typing.Optional[typing.Union[Path, str]] = None):
		return grammarText
