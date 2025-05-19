# agent_workflow.py
import asyncio
import os

from CompanyProject.巴迪克.Tax.Api.cancel import CancelOrderAPI
from CompanyProject.巴迪克.Tax.UI.logic.tax_agent_register import agent_register
from CompanyProject.巴迪克.Tax.Api.create import CreateOrderAPI
from CompanyProject.巴迪克.Tax.UI.logic.tax_platform_audit import platform_login, audit_agent, \
    audit_merchant
from tax_agent import agent_login, create_merchant


async def run_full_flow(login_email: str):
    """
    全流程：注册agent，platform审核agent，agent登录后创建merchant，platform审核merchant，agent申报商户收入，agent撤销申报
    """
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    DATA_DIR = os.path.join(BASE_DIR, '../../../common', 'data')
    pdf_file_path = os.path.join(DATA_DIR, "合同.pdf")

    agent_register_email = "tax_agent0011@linshiyou.com"

    # 注册agent
    agent_register(agent_register_email)

    # 审核agent
    login_email = "tax_operator@test.com"
    platform_login(login_email)
    audit_agent()

    # 注册merchant
    agent_login()
    create_merchant(pdf_file_path)

    # 审核merchant
    platform_login(login_email)
    audit_merchant()

    # 申报收入
    creat_api = CreateOrderAPI()
    creat_api.create_order()

    #  撤销申报
    cancel_api = CancelOrderAPI()
    cancel_api.cancel_order()



if __name__ == '__main__':
    asyncio.run(run_full_flow())
