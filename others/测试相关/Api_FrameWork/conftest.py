
# 所有测试用例执行完成后统计终端测试结果
def pytest_terminal_summary(terminalreporter):
    total = terminalreporter._numcollected
    passed = len([i for i in terminalreporter.stats.get('passed', []) if i.when != 'teardown'])
    failed = len([i for i in terminalreporter.stats.get('failed', []) if i.when != 'teardown'])
    skipped = len([i for i in terminalreporter.stats.get('skipped', []) if i.when != 'teardown'])
    with open('temp/statistics.txt', 'w', encoding='utf8') as fp:
        fp.write(f'''>用例总数：<font color="comment">{total}</font>
        >通过数：<font color="comment">{passed}</font>
        >失败数：<font color="comment">{failed}</font>
        >跳过数：<font color="comment">{skipped}</font>)''')
# 每条测试用例执行后存储执行失败的用例
def pytest_runtest_logreport(report):
    if report.when == "call":
        if report.failed:
            failed_nodeid = report.nodeid
            failed_case = failed_nodeid.split('::')[-1]
            with open('temp/failed_cases.yaml', 'w', encoding='utf8') as fp:
                fp.write(failed_case)