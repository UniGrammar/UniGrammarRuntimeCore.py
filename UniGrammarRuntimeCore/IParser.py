import typing
from abc import ABC, abstractmethod
from pathlib import Path

from .ICompiler import ICompiler


class IParser(ABC):
	"""Just initializes the parser and parses a string into a parse tree specific to backend"""

	__slots__ = ()

	NAME = None  # Must match the name of the backend used in `META.name` in the backend in `UniGrammar.backends`

	@abstractmethod
	def __call__(self, s: str):
		"""parses the stuff"""
		raise NotImplementedError


class IParserFactory(ABC):
	"""Produces instances of `IParser` classes and carries a common state. Should be a singleton."""

	__slots__ = ()
	PARSER_CLASS = None

	def fromInternal(self, internalRepr: typing.Any, target: str = None) -> typing.Any:
		return self.__class__.PARSER_CLASS(internalRepr)


class IParserFactoryFromSource(IParserFactory, ICompiler):  # pylint: disable=abstract-method
	"""A parser that is constructed from a text string representing a grammar in DSL rather than a precompiled file. This class has additional metods for DRY"""

	__slots__ = ()

	def fromStr(self, grammarText: str, target: typing.Any = None, fileName: typing.Optional[typing.Union[Path, str]] = None):
		"""Constructs a parser from a `str` with parser-specific DSL"""
		return self.fromInternal(self.compileStr(grammarText, target, fileName))

	def fromFile(self, grammarFile: Path, target: typing.Any = None):
		"""Constructs a parser from a file with parser-specific DSL"""
		return self.fromInternal(self.compileFile(grammarText, target, fileName))


class IParserFactoryFromPrecompiled(IParserFactory):
	"""A parser that is constructed from a python file. This class has additional metods for DRY"""

	__slots__ = ()

	@abstractmethod
	def processEvaledGlobals(self, globalz: dict, grammarName: str):
		"""
		1. returns the ctor
		2. does other stuff
		"""
		raise NotImplementedError

	def compile(self, sourceOrAST: typing.Union[str, "ast.Module"], grammarName):
		compiled = compile(sourceOrAST, grammarName + ".py", "exec", optimize=2)
		globalz = {}
		eval(compiled, globalz)
		return self.processEvaledGlobals(globalz, grammarName)
