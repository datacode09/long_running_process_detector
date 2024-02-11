import unittest
from unittest.mock import patch, MagicMock
from your_script import send_email, long_running_process_monitor, main

class TestScript(unittest.TestCase):
    @patch('your_script.sendErrorEmail')
    def test_send_email(self, mock_sendErrorEmail):
        send_email("Test Subject", "Test Message", True)
        self.assertFalse(mock_sendErrorEmail.called)
        send_email("Test Subject", "Test Message", False)
        mock_sendErrorEmail.assert_called_with(['abul.fahad@rbc.com'], "Test Subject", "Test Message")

    @patch('your_script.psutil.process_iter', return_value=iter([MagicMock(info={'pid': 1234, 'name': 'test', 'create_time': 1234567890})]))
    @patch('your_script.time.time', return_value=1234567890 + 30*60 + 1)
    def test_long_running_process_monitor(self, mock_time, mock_process_iter):
        result = long_running_process_monitor()
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]['pid'], 1234)

    @patch('your_script.long_running_process_monitor', return_value=[{'pid': 1234, 'name': 'test', 'create_time': 1234567890}])
    @patch('your_script.send_email')
    def test_main(self, mock_send_email, mock_long_running_process_monitor):
        main()
        mock_long_running_process_monitor.assert_called()
        mock_send_email.assert_called_with("Long Running Process Alert", "Long running processes detected:\n\ntest (PID: 1234)", False)

if __name__ == '__main__':
    unittest.main()
