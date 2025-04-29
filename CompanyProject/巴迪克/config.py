# config.py
class Config:
    BASE_URL = "http://payok-test.com"
    TEST_PDF = "../data/合同.pdf"

    PAYOK_TESTDB_CONFIG = {
        'host': '192.168.0.227',
        'port': 3306,
        'user': 'WAYANGPAY',
        'password': 'Z43@Mon88'
    }
    PAYLABS_TESTDB_CONFIG = {
        'host': '192.168.0.233',
        'port': 3306,
        'user': 'paylabs_payapi',
        'password': 'SharkZ@DBA666'
    }

    TAX_TESTDB_CONFIG = {
        'host': '192.168.0.50',
        'port': 3306,
        'user': 'belitax_test',
        'password': 'VSwE8zVrfuUP#HN'
    }