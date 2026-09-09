import os
from dotenv import load_dotenv
from modeling.records import IndicatorRecord
from pyoti.multis import VirusTotalV3
from pyoti.multis import OTX

load_dotenv()

class PyOTIEnricher:

    def __init__(self):
        self.vt_api_key = os.getenv("VT_KEY")
        self.otx_key = os.getenv("OTX_KEY")

        if not self.vt_api_key:
            raise RuntimeError("VT_API_KEY is not set")

        if not self.otx_key:
            raise RuntimeError("OTX_API_KEY is not set")
        
        self.vt = VirusTotalV3(api_key=self.vt_api_key)
        self.otx = OTX(api_key=self.otx_key)

    def enrich(self,record: IndicatorRecord) -> IndicatorRecord:

            indicator = record.indicator
            value = indicator.value
            indicator_type = indicator.indicator_type

            results = {}

            # -------------------------
            # VirusTotal
            # -------------------------
            try:
                results["virustotal"] = (self._query_virustotal(value,indicator_type))
            except Exception as error:
                results["virustotal"] = {
                    "status": "error", 
                    "error": str(error)
                }

            # -------------------------
            # OTX
            # -------------------------
            try:
                results["otx"] = (self._query_otx(value, indicator_type))
            except Exception as error:
                results["otx"] = {
                    "status": "error",
                    "error": str(error)
                }

            record.enrichment = results
            record.enrichment_status = "completed"
            return record

    # =====================================================
    # VirusTotal
    # =====================================================
    def _query_virustotal(self, value: str, indicator_type: str):

        if indicator_type == "domain":
            self.vt.domain = value
            return self.vt.check_domain()
        elif indicator_type == "sha_256":
            self.vt.file_hash = value
            return self.vt.check_hash()
        elif indicator_type == "ipv4":
            self.vt.ip = value
            return self.vt.check_ip()
        elif indicator_type == "url":
            self.vt.url = value
            return self.vt.check_url()
        return {
            "status": "unsupported",
            "indicator_type": indicator_type
        }

    # =====================================================
    # OTX
    # =====================================================
    def _query_otx(self, value: str, indicator_type: str):

        if indicator_type == "domain":
            self.otx.domain = value
            return self.otx.check_domain()
        elif indicator_type == "sha_256":
            self.otx.file_hash = value
            return self.otx.check_hash()
        elif indicator_type == "ipv4":
            self.otx.ip = value
            return self.otx.check_ip()
        elif indicator_type == "url":
            self.otx.url = value
            return self.otx.check_url()

        return {
            "status": "unsupported",
            "indicator_type": indicator_type
        }