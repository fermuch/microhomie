import typing

def block_sleep(time_seconds: int) -> None:
  pass

def gmtime(unixtimestamp: typing.Optional[float]) -> typing.Tuple[int]:
  pass

def localtime(unixtimestamp: typing.Optional[float]) -> float:
  pass

def mktime(time: typing.Union[typing.List[float, int], typing.Tuple[float, int]]) -> float:
  pass

def sleep(time: typing.Union[int, float]) -> None:
  pass

def sleep_ms(time: typing.Union[int, float]) -> None:
  pass

def sleep_us(time: typing.Union[int, float]) -> None:
  pass

def strftime(template: str) -> str:
  pass

def ticks_add(ticks: int, delta: int) -> int:
  """
  Offset ticks value by a given number, which can be either positive or negative.
  Given a ticks value, this function allows to calculate ticks value delta ticks before or after it,
  following modular-arithmetic definition of tick values (see ticks_ms() above).
  ticks parameter must be a direct result of call to ticks_ms(), ticks_us(), or ticks_cpu()
  functions (or from previous call to ticks_add()).
  
  However, delta can be an arbitrary integer number or numeric expression. ticks_add()
  is useful for calculating deadlines for events/tasks.
  
  (Note: you must use ticks_diff() function to work with deadlines.)
  """
  pass

def ticks_base() -> int:
  pass

def ticks_cpu() -> int:
  pass

def ticks_diff(tick_A: int, tick_B: int) -> int:
  pass

def ticks_ms() -> int:
  pass

def ticks_us() -> int:
  pass

def tickscpu_diff() -> int:
  pass

def utime() -> float:
  pass