from Projects.dss_system.Modules.CaseMethod import CaseCode
import jsonpath
import json


class TestCustomer(CaseCode):
    """ 测试用例集 """

    def __init__(self, *args, **kwargs):
        super(TestCustomer, self).__init__(*args, **kwargs)

    def test_customer_list(self):
        """ 查询客户列表 """
        with self.setUp():
            data = self.data.get("customer_list")

        with self.steps():
            resp = self.customer_list(data)
            resp_json = json.loads(resp.text)
            resp_name = ''.join(jsonpath.jsonpath(resp_json, "$..epName"))
            sql = self.sql.get("find_customer") % data.get("searchKey")
            expect = self.select_sql(sql)[0].get("ep_name")

        with self.verify():
            assert resp_name == expect, "错误，预期%s，实际%s" % (expect, resp_name)
