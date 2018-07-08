import Optional, Callable, Tuple from typing

class Mqtt:
  def __init__(
    self,
    name: str,
    server: str,
    user: Optional[str],
    password: Optional[str],
    port: Optional[int],
    autoreconnect: Optional[bool],
    clientid: Optional[str],
    cleansession: Optional[bool],
    keepalive: Optional[int],
    lwt_topic: Optional[str],
    lwt_msg: Optional[str],
    lwt_retain: Optional[bool],
    lwt_qos: Optional[0, 1, 2],
    cert: Optional[str],
    connected_cb: Optional[Callable[[str], None]],
    disconnected_cb: Optional[Callable[[str], None]],
    subscribed_cb: Optional[Callable[[str, str], None]],
    unsubscribed_cb: Optional[Callable[[str, str], None]],
    published_cb: Optional[Callable[[str, bool], None]],
    data_cb: Optional[Callable[[str, int, [str, bytes]], None]]
  ):
    pass
  
  def config(
    self,
    user: Optional[str],
    password: Optional[str],
    port: Optional[int],
    autoreconnect: Optional[bool],
    clientid: Optional[str],
    cleansession: Optional[bool],
    keepalive: Optional[int],
    lwt_topic: Optional[str],
    lwt_msg: Optional[str],
    lwt_retain: Optional[bool],
    lwt_qos: Optional[0, 1, 2],
    cert: Optional[str],
    connected_cb: Optional[Callable[[str], None]],
    disconnected_cb: Optional[Callable[[str], None]],
    subscribed_cb: Optional[Callable[[str, str], None]],
    unsubscribed_cb: Optional[Callable[[str, str], None]],
    published_cb: Optional[Callable[[str, bool], None]],
    data_cb: Optional[Callable[[str, int, [str, bytes]], None]]
  ) -> None:
    pass

  def status(self) -> Tuple[[int, str]]:
    pass
  
  def subscribe(
    self,
    topic: str,
    qos: Optional[0, 1, 2]
  ) -> bool:
    pass
  
  def unsubscribe(self, topic: str) -> bool:
    pass
  
  def publish(self, topic: str, msg: [str, bytes], qos: [0, 1, 2]) -> bool:
    pass
  
  def stop(self) -> None:
    pass
  
  def start(self) -> None:
    pass
  
  def free(self) -> None:
    pass
  