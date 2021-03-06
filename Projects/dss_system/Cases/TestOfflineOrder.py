from unittest import skip

from Projects.dss_system.Modules.CaseMethod import CaseCode
import jsonpath
import json
from datetime import datetime
import time


class TestOfflineOrder(CaseCode):
    """ 线下订单流程测试用例集 """

    def __init__(self, *args, **kwargs):
        super(TestOfflineOrder, self).__init__(*args, **kwargs)

    def test_01_create_order(self):
        """ 新增ERP线下订单 """
        with self.setUp():
            data = self.data.get("offlineOrder")
            order_id = "test" + datetime.now().strftime('%Y%m%d%H%M%S')
            data['externalOrderCode'] = order_id
            data['orderTime'] = self.get_data_time()
            self.logger.warning("请求参数：%s" % data)

        with self.steps():
            # 请求
            resp = self.create_offline_order(data)
            resp_json = json.loads(resp.text)
            self.logger.warning("响应参数：%s" % resp_json)

            resp_code = resp_json.get("resultCode")
            resp_msg = resp_json.get("resultMsg")

        with self.verify():
            # 断言
            assert resp_code == 1000 and resp_msg == '操作成功', "错误，实际%s %s" % (resp_code, resp_msg)

        with self.save():
            # 保存订单id
            self.procedure().value.update({"order_code": order_id})

    def test_02_production_order(self):
        """ 测试订单排产 """

        with self.setUp():
            data = self.data.get("productionOrder")
            data['productionData'][0]['externalOrderCode'] = self.procedure().value.get("order_code")
            self.logger.warning("请求参数：%s" % data)
        with self.steps():
            resp = self.production_order(data=data)
            resp_json = json.loads(resp.text)
            self.logger.warning("响应参数：%s" % resp_json)
            resp_code = resp_json.get("resultCode")
            resp_msg = resp_json.get("resultMsg")
            order_status = self.select_sql(self.sql.get("find_order") % self.procedure().value.get("order_code")) \
                .get("order_status")

        with self.verify():
            assert resp_code == 1000 and resp_msg == '操作成功', \
                "错误，实际%s %s 数据库状态：%s  订单号：%s" % (
                    resp_code, resp_msg, order_status, self.procedure().value.get("order_code"))
            assert order_status == '待入库', "错误，实际数据库状态：%s  订单号：%s" % (
                order_status, self.procedure().value.get("order_code"))
    @skip
    def test_03_entering_warehouse(self):
        """ 测试订单入库 """
        with self.setUp():
            data = self.data.get("enteringWarehouse")
            data['enteringWarehouseData'][0]['externalOrderCode'] = self.procedure().value.get("order_code")

        with self.steps():
            resp = self.entering_warehouse(data=data)
            resp_json = json.loads(resp.text)
            self.logger.warning("响应参数：%s" % resp_json)
            resp_code = resp_json.get("resultCode")
            resp_msg = resp_json.get("resultMsg")
            order_status = self.select_sql(self.sql.get("find_order") % self.procedure().value.get("order_code")) \
                .get("order_status")

        with self.verify():
            time.sleep(2)
            assert resp_code == 1000 and resp_msg == '操作成功', \
                "错误，实际%s %s 数据库状态：%s  订单号：%s" % (
                    resp_code, resp_msg, order_status, self.procedure().value.get("order_code"))
            assert order_status == '待发货', "错误，实际数据库状态：%s  订单号：%s" % (
                order_status, self.procedure().value.get("order_code"))
    @skip
    def test_04_delivery_order(self):
        """ 测试订单发货 """
        with self.setUp():
            data = self.data.get("deliveryOrder")
            data['deliveryList'][0]['externalOrderCode'] = self.procedure().value.get("order_code")
            data['externalDeliveryCode'] = self.procedure().value.get("order_code")
            self.logger.warning("请求参数：%s" % data)

        with self.steps():
            resp = self.delivery_order(data=data)
            resp_json = json.loads(resp.text)
            self.logger.warning("响应参数：%s" % resp_json)
            resp_code = resp_json.get("resultCode")
            resp_msg = resp_json.get("resultMsg")
            order_status = self.select_sql(self.sql.get("find_order") % self.procedure().value.get("order_code")) \
                .get("order_status")

        with self.verify():
            assert resp_code == 1000 and resp_msg == '操作成功', \
                "错误，实际%s %s 数据库状态：%s  订单号：%s" % (
                    resp_code, resp_msg, order_status, self.procedure().value.get("order_code"))
            assert order_status == '待签收', "错误，实际数据库状态：%s  订单号：%s" % (
                order_status, self.procedure().value.get("order_code"))
    @skip
    def test_05_receipt_order(self):
        """ 测试订单签收 """
        with self.setUp():
            data = self.data.get("receiptOrder")
            data['receiptList'][0]['externalOrderCode'] = self.procedure().value.get("order_code")
            data['externalDeliveryCode'] = self.procedure().value.get("order_code")
            self.logger.warning("请求参数：%s" % data)

        with self.steps():
            resp = self.receipt_order(data=data)
            resp_json = json.loads(resp.text)
            self.logger.warning("响应参数：%s" % resp_json)
            resp_code = resp_json.get("resultCode")
            resp_msg = resp_json.get("resultMsg")
            order_status = self.select_sql(self.sql.get("find_order") % self.procedure().value.get("order_code")) \
                .get("order_status")

        with self.verify():
            assert resp_code == 1000 and resp_msg == '操作成功', \
                "错误，实际%s %s 数据库状态：%s  订单号：%s" % (
                    resp_code, resp_msg, order_status, self.procedure().value.get("order_code"))

            assert order_status == '已签收', "错误，实际数据库状态：%s  订单号：%s" % (
                order_status, self.procedure().value.get("order_code"))
    @skip
    def test_06_cancel_order(self):
        """ 测试取消线下订单 """
        with self.setUp():
            data = self.data.get("cancel_order")
            data["externalOrderCode"] = self.procedure().value.get("order_code")
            self.logger.warning("请求参数：%s" % data)

        with self.steps():
            resp = self.cancel_order(data=data)
            resp_json = json.loads(resp.text)
            self.logger.warning("响应参数：%s" % resp_json)
            resp_code = resp_json.get("resultCode")
            resp_msg = resp_json.get("resultMsg")

        with self.verify():
            assert resp_code == 1000 and resp_msg == '操作成功', "错误，实际%s %s" % (resp_code, resp_msg)
    @skip
    def test_07_end_order(self):
        """ 测试完结订单 """
        with self.setUp():
            data = self.data.get("end_order")
            data["externalOrderCode"] = self.procedure().value.get("order_code")
            self.logger.warning("请求参数：%s" % data)

        with self.steps():
            resp = self.end_order(data=data)
            resp_json = json.loads(resp.text)
            self.logger.warning("响应参数：%s" % resp_json)
            resp_code = resp_json.get("resultCode")
            resp_msg = resp_json.get("resultMsg")

        with self.verify():
            assert resp_code == 1000 and resp_msg == '操作成功', "错误，实际%s %s" % (resp_code, resp_msg)
    @skip
    def test_08_after_sale(self):
        """ 测试售后处理 """
        with self.setUp():
            data = self.data.get("after_sale")
            data['afterSaleOrderProductList'][0]["externalOrderCode"] = self.procedure().value.get("order_code")
            data['afterSaleOrderProductList'][0]["externalDeliveryCode"] = self.procedure().value.get("order_code")
            data["customerCode"] = "Y003"
            data["externalDeliveryCode"] = self.procedure().value.get("order_code")
            data["operateDate"] = self.get_data_time()
            data["refundTime"] = self.get_data_time()
            self.logger.warning("请求参数：%s" % data)

        with self.steps():
            resp = self.after_sale(data=data)
            resp_json = json.loads(resp.text)
            resp_code = resp_json.get("resultCode")
            resp_msg = resp_json.get("resultMsg")

        with self.verify():
            assert resp_code == 1000 and resp_msg == '操作成功', "错误，实际%s %s" % (resp_code, resp_msg)

    @skip
    def test_09_statement_bill(self):
        """ 测试对账单生成 """
        with self.setUp():
            data = self.data.get("statement_bill")
            self.logger.warning("请求参数：%s" % data)

        with self.steps():
            resp = self.statement_bill(data=data)
            resp_json = json.loads(resp.text)
            resp_code = resp_json.get("resultCode")
            resp_msg = resp_json.get("resultMsg")

        with self.verify():
            assert resp_code == 1000 and resp_msg == '操作成功', "错误，实际%s %s" % (resp_code, resp_msg)
