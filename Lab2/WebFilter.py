
class WebFilter:
    def __init__(self):
        self.forbidden = []
        self.forbidden_URL_response = "http://www.ida.liu.se/~TDTS04/labs/2011/ass2/error1.html"
        self.forbidden_content_response = "http://www.ida.liu.se/~TDTS04/labs/2011/ass2/error2.html"

    def add_forbidden_word(self, word):
        self.forbidden.append(word)

    def remove_forbidden_word(self, word):
        self.forbidden.remove(word)

    def contains_forbidden_word(self, text):
        for elem in self.forbidden:
            if elem in text:
                return True

        return False

    def create_response(self, redirect, date, http_version, server):
        response = 'HTTP/1.{} 302 Found\r\n Date: {} \r\n Server: {} \
             \r\n Location: {} Content-Length: 0 \r\n Connection: close\r\n Content-Type: \
             text/html\r\n\r\n'.format(http_version, date, server, redirect)
        print(response.encode("utf-8"))
        return response.encode("utf-8")
