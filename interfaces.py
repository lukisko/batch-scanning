import requests

class printer_interface:
    def make_scan_job() -> str:
        '''make scan job for scanning and then return the scan job'''
        pass
    def wait_and_get_scan(job_id) -> requests.Response:
        '''wait for the scan to finish and get the response which should have body of pdf'''
        pass