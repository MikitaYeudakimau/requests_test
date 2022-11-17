from main import parse


class TestClass:
    string_right_one = "https://google.com, https://onliner.by"
    string_right_two = "http://indexofcare.org, http://apdrc.soest.hawaii.edu"
    string_uncorrect = "google.com, onliner.by"
    string_uncorrect_partially = "123213asd, https://google.com"

    def test_parse_string_right_one(self, capsys):
        parse(self.string_right_one)
        out, err = capsys.readouterr()
        assert out == "{'https://google.com': {'GET': 200, 'HEAD': 301}, " \
                      "'https://onliner.by': {'GET': 200, 'POST': 200, 'HEAD': 301}}\n"
        assert err == ""

    def test_parse_string_right_two(self, capsys):
        parse(self.string_right_two)
        out, err = capsys.readouterr()
        assert out == "{'http://indexofcare.org': {'GET': 200, 'POST': 200, 'HEAD': 200, 'OPTIONS': 200}, " \
                      "'http://apdrc.soest.hawaii.edu': {'GET': 200, 'POST': 200, 'PUT': 200, 'DELETE': 200, " \
                      "'HEAD': 200, 'PATCH': 200, 'OPTIONS': 200}}\n"
        assert err == ""

    def test_parse_string_uncorrect(self, capsys):
        parse(self.string_uncorrect)
        out, err = capsys.readouterr()
        assert out == "URL введен некорректно\nURL введен некорректно\n"
        assert err == ""

    def test_parse_string_uncorrect_partially(self, capsys):
        parse(self.string_uncorrect_partially)
        out, err = capsys.readouterr()
        assert out == "Строка 123213asd не является ссылкой\n{'https://google.com': {'GET': 200, 'HEAD': 301}}\n"
        assert err == ""
