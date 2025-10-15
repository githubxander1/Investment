// 测试买入工商银行股票的示例代码
#include "pystock.h"
#include <iostream>
#include <windows.h>

using namespace std;

int main() {
    cout << "ChinaStock_TradeAPI 工商银行买入测试" << endl;
    cout << "==================================" << endl;
    
    Pystock trader;
    
    // 启动交易软件
    cout << "1. 启动川财证券交易软件..." << endl;
    int openResult = trader.OpenTrade("D:\\Xander\\Applications\\THS\\同花顺\\xiadan.exe");
    
    if (openResult != 1) {
        cout << "   错误：无法启动交易软件，请检查路径是否正确。" << endl;
        return -1;
    }
    
    cout << "   交易软件启动成功" << endl;
    
    // 等待用户确认登录完成
    cout << "2. 请在交易软件中手动完成登录，完成后按回车键继续..." << endl;
    cin.get();
    
    // 如果需要自动登录，可以取消下面的注释并修改参数
    // cout << "2. 自动登录账户..." << endl;
    // int loginResult = trader.LoginTrade("8526331", "170212", "communications_password");
    // if (loginResult != 1) {
    //     cout << "   错误：登录失败，请检查账户信息。" << endl;
    //     return -1;
    // }
    // cout << "   账户登录成功" << endl;
    
    // 预处理界面元素
    cout << "3. 预处理界面元素..." << endl;
    trader.PreHandle();
    cout << "   界面元素预处理完成" << endl;
    
    // 买入工商银行股票
    cout << "4. 买入工商银行股票..." << endl;
    cout << "   股票代码: 601398" << endl;
    cout << "   买入价格: 请根据实际行情填写" << endl;
    cout << "   买入数量: 100股" << endl;
    
    // 注意：请根据实际行情价格修改买入价格
    bool buyResult = trader.iBuy("601398", "5.00", "100");
    
    if (buyResult) {
        cout << "   买入委托发送成功" << endl;
    } else {
        cout << "   买入委托可能存在问题，请检查交易软件确认" << endl;
    }
    
    cout << "5. 测试完成" << endl;
    cout << "   请在交易软件中确认委托是否成功提交" << endl;
    
    // 等待用户查看结果
    cout << "   按回车键退出程序..." << endl;
    cin.get();
    
    return 0;
}