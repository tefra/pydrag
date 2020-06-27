from unittest import TestCase

from pydrag.utils import md5
from pydrag.utils import to_camel_case


class UtilTests(TestCase):
    def test_md5(self):
        self.assertEqual("3858f62230ac3c915f300c664312c63f", md5("foobar"))
        self.assertRegex(md5("foobar"), "^[a-z0-9]{32}$")
        self.assertEqual("", md5(""))
        self.assertIsNone(md5(None))

    def test_to_camel_case(self):
        self.assertEqual("aaBb", to_camel_case("aa_bb"))
        self.assertEqual("aaBb", to_camel_case("aA_bB"))
        self.assertEqual("aaBb", to_camel_case("AA_BB"))
        self.assertEqual("aa", to_camel_case("aa"))
        self.assertEqual("aa", to_camel_case("Aa"))
