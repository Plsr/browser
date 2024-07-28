import socket
import ssl

class URL:
  def __init__(self, url):
    
    if url.split(":")[0] == "data":
      print("data scheme")
      self.scheme, url = url.split(":", 1)
      self.data_type, url = url.split(",", 1)
      self.data = url
      return

    self.scheme, url = url.split("://", 1)
    assert self.scheme in ["http", "https", "file"]

    if self.scheme == "http":
      self.port = 80
    elif self.scheme == "https":
      self.port = 443


    if "/" not in url:
      url = url + "/"
    self.host, url = url.split("/", 1)

    if ":" in self.host:
      self.host, port = self.host.split(":", 1)
      self.port = int(port)

    self.path = "/" + url

  def request(self):
    if self.scheme == "file":
      f = open(self.path, 'r')
      return f.read()
    elif self.scheme == "data":
      return self.data

    s = socket.socket(
      family=socket.AF_INET,
      type=socket.SOCK_STREAM,
      proto=socket.IPPROTO_TCP,
    )

    s.connect((self.host, self.port))

    if self.scheme == "https":
      ctx = ssl.create_default_context()
      s = ctx.wrap_socket(s, server_hostname=self.host)

    request = "GET {} HTTP/1.0\r\n".format(self.path)
    request += "Host: {}\r\n".format(self.host)
    request += "Connection: close\r\n"
    request += "User Agent: Plsr/1.0 Urethane Alpha 0.1\r\n"
    request += "\r\n"

    s.send(request.encode("utf8"))

    response = s.makefile("r", encoding="utf8", newline="\r\n")
    statusline = response.readline()
    version, status, explanation = statusline.split(" ", 2)

    response_headers = {}
    while True:
      line = response.readline()
      if line == "\r\n": break
      header, value = line.split(":", 1)
      response_headers[header.casefold()] = value.strip()

    assert "transfer-encoding" not in response_headers
    assert "content-encoding" not in response_headers

    content = response.read()
    s.close()
    return content

  def lex(self, body):
    text = ""
    in_tag = False
    index = 0 
    while index < len(body):
      c = body[index]
      if c == "<":
        in_tag = True
      if c == ">":
        in_tag = False
      if c == "&":
        entity = ""
        original_index = index

        # TODO:: This won't scale
        while index < len(body) and body[index] != ";":
          index += 1
          if body[index] == ';':
            if entity == "lt":
              text += "<"
            elif entity == "gt":
              text += ">"
            else:
              index = original_index
            break
            
          entity += body[index]
      elif not in_tag:
        text += c
      
      index += 1

    return text

  def load(self):
    body = self.request()
    return self.lex(body)

if __name__ == "__main__":
    import sys
    URL.load(URL(sys.argv[1]))
