// 基于用户提供信息的工商银行买入测试程序
#include "pystock.h"
#include <iostream>
#include <windows.h>
#include <string>

using namespace std;

int main() {
    cout << "ChinaStock_TradeAPI 工商银行买入测试程序" << endl;
    cout << "========================================" << endl;
    cout << "注意：本程序需要以管理员权限运行！" << endl;
    cout << "请确保交易软件界面在操作期间不被最小化或遮挡。" << endl;
    cout << "========================================" << endl;
    
    Pystock trader;
    
    // 启动交易软件（使用用户提供的同花顺快捷方式路径）
    cout << "1. 启动同花顺交易软件..." << endl;
    string shortcutPath = "C:\\Users\\Think\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\xiadan.lnk";
    int openResult = trader.OpenTrade((char*)shortcutPath.c_str());
    
    if (openResult != 1) {
        cout << "   错误：无法启动交易软件，请检查路径是否正确。" << endl;
        cout << "   快捷方式路径：" << shortcutPath << endl;
        cout << "   按任意键退出..." << endl;
        system("pause");
        return -1;
    }
    
    cout << "   交易软件启动成功" << endl;
    cout << "   等待交易软件完全加载..." << endl;
    Sleep(3000); // 等待3秒让交易软件完全加载
    
    // 登录账户（提示用户输入，不再硬编码）
    cout << "2. 登录账户设置..." << endl;
    string account, password, commPassword;
    cout << "   请手动在交易软件中完成登录，或在此处输入账户信息：" << endl;
    cout << "   按回车键继续使用手动登录方式..." << endl;
    cin.get(); // 等待用户确认使用手动登录
    // 提示用户可以手动输入，但默认使用空字符串以便手动登录
    account = "";
    password = "";
    commPassword = "";
    
    // 由于账户信息为空，直接提示用户手动登录
    cout << "   请确保您已在交易软件中完成手动登录。" << endl;
    cout << "   如果尚未登录，请现在进行登录操作。" << endl;
    cout << "   登录完成后按回车键继续..." << endl;
    cin.get();
    
    // 预处理界面元素
    cout << "3. 预处理界面元素..." << endl;
    trader.PreHandle();
    cout << "   界面元素预处理完成" << endl;
    
    // 买入工商银行股票（股票代码601398，数量100股）
    cout << "4. 买入工商银行股票..." << endl;
    cout << "   股票代码: 601398" << endl;
    cout << "   买入价格: 按照当前价格（系统默认）" << endl;
    cout << "   买入数量: 100股" << endl;
    
    // 使用默认价格（传入空字符串表示使用当前价格）
    bool buyResult = trader.iBuy("601398", "", "100");
    
    if (buyResult) {
        cout << "   买入委托发送成功" << endl;
    } else {
        cout << "   买入委托可能存在问题，请检查交易软件确认" << endl;
    }
    
    cout << "5. 操作完成" << endl;
    cout << "   请在交易软件中确认委托是否成功提交" << endl;
    cout << "   注意：实际交易前请再次确认价格和数量是否正确！" << endl;
    
    // 等待用户查看结果
    cout << "   按回车键退出程序..." << endl;
    cin.get();
    
    return 0;
}