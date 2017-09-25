from datetime import date


class WebFilter:
    def __init__(self):
        self.forbidden = []
        self.forbidden_URL_response = "/~TDTS04/labs/2011/ass2/error1.html"
        self.forbidden_URL_host = "http://www.ida.liu.se"
        self.forbidden_content_response = "~TDTS04/labs/2011/ass2/error2.html"
        self.forbidden_content_host = "http://www.ida.liu.se/"

    def add_forbidden_word(self, word):
        self.forbidden.append(word)

    def remove_forbidden_word(self, word):
        self.forbidden.remove(word)

    def contains_forbidden_word(self, text):
        for elem in self.forbidden:
            if elem.lower() in text.lower():
                return True

        return False

    def create_response(self, is_url, header):
        if is_url:
            host = self.forbidden_URL_host
            response = self.forbidden_URL_response
        else:
            host = self.forbidden_content_host
            response = self.forbidden_content_response

        body = '<!DOCTYPE HTML PUBLIC "-//IETF//DTD HTML 2.0//EN">\n<html><head>\n<title>302 Found</title>\n' \
               '</head><body>\n <h1>Found</h1>\n' \
               ' <p>The document has moved <a href="{}{}">here</a>.</p>\n' \
               '</body></html>\n'.format(host, response)
        #print(body)
        bodylength = len(body)

        response = '{} 302 Found\r\nLocation: {}{}\r\nContent-Length: {}\r\nConnection: close\r\nConnection-Type: text/html; charset=iso-8859-1\r\n\r\n{}'.format(header.http_version, host, response, bodylength, body)

        #print("Resposne: ", response)
        return response.encode("utf-8")
