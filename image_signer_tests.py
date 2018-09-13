import unittest, datetime
from lambda_function import get_signature, extract_signable_path, add_signature, get_source, generate_iguim_url, add_quality_parameter

class TestImageFunctions(unittest.TestCase):

    def setUp(self):
        self.validUrl = "http://media.guim.co.uk/67222cbde87dc147dd34041c2e8692b81f24f546/0_0_1204_1181/500.jpg"
        self.validUrlQs = "http://media.guim.co.uk/67222cbde87dc147dd34041c2e8692b81f24f546/0_0_1204_1181/500.jpg?width=300"

    def test_get_signature(self):
        self.assertEqual(get_signature("teststring", "testsalt"), "a3d07d9dc9ab9da4a88cad2694ee1184")

    def test_extract_signable_path(self):
        path = extract_signable_path(self.validUrl)
        self.assertEqual(path, "/67222cbde87dc147dd34041c2e8692b81f24f546/0_0_1204_1181/500.jpg")
        path = extract_signable_path(self.validUrlQs)
        self.assertEqual(path, "/67222cbde87dc147dd34041c2e8692b81f24f546/0_0_1204_1181/500.jpg?width=300")

    def test_add_signature(self):
        signed_url = add_signature("hehe", "secret")
        self.assertEqual(signed_url, "hehe?s=secret")
        signed_url = add_signature("hehe?lol=haha", "secret")
        self.assertEqual(signed_url, "hehe?lol=haha&s=secret")

    def test_get_source(self):
        source = get_source("//uploads.guim.co.uk")
        self.assertEqual(source, "uploads")
        source = get_source("//lol.guim.co.uk")
        self.assertEqual(source, "media")

    def test_generate_iguim_url(self):
        signed_path = "/haha/lol?s=secret"
        generated_url = generate_iguim_url(signed_path, "media")
        self.assertEqual(generated_url, "https://i.guim.co.uk/img/media/haha/lol?s=secret")

    def test_add_quality_parameter(self):
        withq = add_quality_parameter("/lol/haha?quality=20")
        self.assertEqual(withq, withq)
        noq = add_quality_parameter("/lol/haha")
        self.assertEqual(noq, "/lol/haha?quality=85")





if __name__ == '__main__':
    unittest.main()