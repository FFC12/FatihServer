import json
import unittest
from parsers.http_parser import HttpRequestParser

case0 = """POST https://website.com/cgi-bin/process.cgi HTTP/1.1
User-Agent: Mozilla/4.0 (compatible; MSIE5.01; Windows NT)
Host: www.website.com
Content-Type: application/x-www-form-urlencoded
Content-Length: length
Accept-Language: en-us
Accept-Encoding: gzip, deflate
Connection: Keep-Alive

licenseID=string&content=string&/paramsXML=string
"""

case1 = """POST https://website.com/cgi-bin/process.cgi HTTP/1.1
User-Agent: Mozilla/4.0 (compatible; MSIE5.01; Windows NT)
Host: www.website.com
Content-Type: application/json
Content-Length: length
Accept-Language: en-us
Accept-Encoding: gzip, deflate
Connection: Keep-Alive

{"licenseID": "string", "content": "string", "/paramsXML": "string"}
"""

case2 = """POST https://website.com/cgi-bin/process.cgi HTTP/1.1
User-Agent: Mozilla/4.0 (compatible; MSIE5.01; Windows NT)
Host: www.website.com
Content-Type: application/html
Content-Length: length
Accept-Language: en-us
Accept-Encoding: gzip, deflate
Connection: Keep-Alive

<html>
    <head>
        <title>Test</title>
    </head>
    <body>
        <h1>Test</h1>
    </body>
</html>
"""

case3 = """POST https://website.com/cgi-bin/process.cgi HTTP/1.1
User-Agent: Mozilla/4.0 (compatible; MSIE5.01; Windows NT)
Host: www.website.com
Content-Type: multipart/form-data;boundary="boundary"
Content-Length: length
Accept-Language: en-us
Accept-Encoding: gzip, deflate
Connection: Keep-Alive

--boundary
Content-Disposition: form-data; name="field1"

value1
--boundary
Content-Disposition: form-data; name="field2"; filename="example.txt"

value2
--boundary--
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
        self.assertEqual(result['method'], "POST")
        self.assertEqual(result['path'], "/cgi-bin/process.cgi")
        self.assertEqual(result['version'], "HTTP/1.1")

        expected_body = "licenseID=string&content=string&/paramsXML=string"
        expected_body = expected_body.split('&')
        expected_body = [item.split('=') for item in expected_body]
        expected_body = {item[0]: item[1] for item in expected_body}
        self.assertEqual(parser.body, expected_body)

    def test_case1(self):
        """
        Test case 1
        :return:
        """
        parser = HttpRequestParser()
        result = parser.parse(case1)
        self.assertEqual(result['method'], "POST")
        self.assertEqual(result['path'], "/cgi-bin/process.cgi")
        self.assertEqual(result['version'], "HTTP/1.1")

        expected_body = '{"licenseID": "string", "content": "string", "/paramsXML": "string"}'
        self.assertDictEqual(parser.body, json.loads(expected_body))

    def test_case2(self):
        """
        Test case 2
        :return:
        """
        parser = HttpRequestParser()
        result = parser.parse(case2)
        self.assertEqual(result['method'], "POST")
        self.assertEqual(result['path'], "/cgi-bin/process.cgi")
        self.assertEqual(result['version'], "HTTP/1.1")

        expected_body = "<html>\n    <head>\n        <title>Test</title>\n    </head>\n    <body>\n        <h1>Test</h1>\n    </body>\n</html>\n"
        self.assertEqual(parser.body, expected_body)

    def test_case3(self):
        """
        Test case 3
        :return:
        """
        parser = HttpRequestParser()
        result = parser.parse(case3)
        self.assertEqual(result['method'], "POST")
        self.assertEqual(result['path'], "/cgi-bin/process.cgi")
        self.assertEqual(result['version'], "HTTP/1.1")

        # TODO: Test multipart/form-data



if __name__ == '__main__':
    unittest.main()
