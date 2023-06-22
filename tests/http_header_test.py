import unittest
from parsers.http_parser import HttpRequestParser

case0 = """POST https://website.com/cgi-bin/process.cgi HTTP/1.1
User-Agent: Mozilla/4.0 (compatible; MSIE5.01; Windows NT)
Host: www.website.com
Content-Type: application/y-www-form-urlencoded
Content-Length: length
Accept-Language: en-us
Accept-Encoding: gzip, deflate
Connection: Keep-Alive

licenseID=string&content=string&/paramsXML=string
"""

case1 = """POST /cgi-bin/process.cgi HTTP/1.1
User-Agent: Mozilla/4.0 (compatible; MSIE5.01; Windows NT)
Host: www.website.com
Content-Type: application/y-www-form-urlencoded
Content-Length: length
Accept-Language: en-us
Accept-Encoding: gzip, deflate
Connection: Keep-Alive

licenseID=string&content=string&/paramsXML=string
"""


class Test(unittest.TestCase):
    """
    Test class for HttpParser
    """

    def test_case0(self):
        """
        Test case 0
        :return:
        """
        parser = HttpRequestParser()
        result = parser.parse(case0)

        headers = result['headers']
        self.assertEqual(result['method'], "POST")
        self.assertEqual(result['path'], "/cgi-bin/process.cgi")
        self.assertEqual(result['version'], "HTTP/1.1")
        self.assertEqual(headers['User-Agent'], "Mozilla/4.0 (compatible; MSIE5.01; Windows NT)")
        self.assertEqual(headers['Host'], "www.website.com")
        self.assertEqual(headers['Content-Type'], "application/y-www-form-urlencoded")
        self.assertEqual(headers['Content-Length'], "length")
        self.assertEqual(headers['Accept-Language'], "en-us")
        self.assertEqual(headers['Accept-Encoding'], "gzip, deflate")
        self.assertEqual(headers['Connection'], "Keep-Alive")

    def test_case1(self):
        """
        Test case 1
        :return:
        """
        parser = HttpRequestParser()
        result = parser.parse(case1)

        headers = result['headers']
        self.assertEqual(result['method'], "POST")
        self.assertEqual(result['path'], "/cgi-bin/process.cgi")
        self.assertEqual(result['version'], "HTTP/1.1")
        self.assertEqual(headers['User-Agent'], "Mozilla/4.0 (compatible; MSIE5.01; Windows NT)")
        self.assertEqual(headers['Host'], "www.website.com")
        self.assertEqual(headers['Content-Type'], "application/y-www-form-urlencoded")
        self.assertEqual(headers['Content-Length'], "length")
        self.assertEqual(headers['Accept-Language'], "en-us")
        self.assertEqual(headers['Accept-Encoding'], "gzip, deflate")
        self.assertEqual(headers['Connection'], "Keep-Alive")


if __name__ == '__main__':
    unittest.main()
