from django.test import TestCase
from django.urls import reverse

from unittest.mock import patch

# Create your tests here.
class AutoTestViewTests(TestCase):
    def test_post_request_returns_success(self):
        response = self.client.post(reverse('code_converter:auto_test'), {'code': 'print("Hello, World!")'})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'code_converter/auto_test.html')

    def test_get_request_returns_success(self):
        response = self.client.get(reverse('code_converter:auto_test'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'code_converter/auto_test.html')

    def test_indexview(self):
        response = self.client.get(reverse('code_converter:index'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'code_converter/index.html')


class ConvertCodeTestCase(TestCase):

    @patch('code_converter.views.extract_backtick_sections')
    @patch('code_converter.views.convert_c_to_rust')
    def test_convert_code_post(self, mock_extract_backtick_sections, mock_convert_c_to_rust):
        input_data = {
            'inputLanguage': 'Python',
            'code': 'print("Hello, world!")',
            'outputLanguage': 'JavaScript'
        }
        mock_convert_c_to_rust.return_value = 'console.log("Hello, world!");'
        mock_extract_backtick_sections.return_value = ['console.log("Hello, world!");'], []
        
        response = self.client.post(reverse('code_converter:convert_code'), input_data)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'code_converter/code_convert.html')
        self.assertEqual(response.context['totalOutput'], 'console.log("Hello, world!");')
        self.assertEqual(response.context['extractedCode'], 'console.log("Hello, world!");')

        mock_convert_c_to_rust.assert_called_once()
        mock_extract_backtick_sections.assert_called_once()

    def test_convert_code_get(self):
        response = self.client.get(reverse('code_converter:convert_code'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'code_converter/code_convert.html')
        self.assertEqual(response.context['totalOutput'], '')
        self.assertEqual(response.context['extractedCode'], '')
