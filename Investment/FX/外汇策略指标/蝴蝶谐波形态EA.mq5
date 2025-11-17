//+------------------------------------------------------------------+
//|                          Copyright 2025, Forex Algo-Trader, Allan |
//|                                  "https://t.me/Forex_Algo_Trader" |
//+------------------------------------------------------------------+
#property copyright "Forex Algo-Trader, Allan"
#property link      "https://t.me/Forex_Algo_Trader"
#property version   "1.00"
#property description "基于蝴蝶谐波形态的智能交易系统（修复版）"
#property strict

// 引入交易库以执行订单
#include <Trade\Trade.mqh>
CTrade obj_Trade;

// 输入参数（可在MT5中直接调整）
input int    PivotLeft    = 5;      // 左侧转折点检测的K线数量
input int    PivotRight   = 5;      // 右侧转折点检测的K线数量
input double Tolerance    = 0.10;   // 谐波比率的容差（建议0.05-0.2，数值越大信号越多）
input double LotSize      = 0.01;   // 交易手数
input bool   AllowTrading = true;   // 是否允许自动交易

// 转折点结构体：存储时间、价格、是否为高点
struct Pivot {
   datetime time;
   double   price;
   bool     isHigh;
};

// 全局变量：存储转折点、形态锁定信息
Pivot pivots[];
int     g_patternFormationBar = -1;  // 形态形成的K线序号
datetime g_lockedPatternX      = 0;   // 锁定形态的X点时间

//+------------------------------------------------------------------+
//| 辅助函数：绘制填充三角形                                         |
//+------------------------------------------------------------------+
void DrawTriangle(string name, datetime t1, double p1, datetime t2, double p2, datetime t3, double p3, color cl, int width, bool fill, bool back) {
   if(ObjectCreate(0, name, OBJ_TRIANGLE, 0, t1, p1, t2, p2, t3, p3)) {
      ObjectSetInteger(0, name, OBJPROP_COLOR, cl);
      ObjectSetInteger(0, name, OBJPROP_STYLE, STYLE_SOLID);
      ObjectSetInteger(0, name, OBJPROP_WIDTH, width);
      ObjectSetInteger(0, name, OBJPROP_FILL, fill);
      ObjectSetInteger(0, name, OBJPROP_BACK, back);
   }
}

//+------------------------------------------------------------------+
//| 辅助函数：绘制趋势线                                             |
//+------------------------------------------------------------------+
void DrawTrendLine(string name, datetime t1, double p1, datetime t2, double p2, color cl, int width, int style) {
   if(ObjectCreate(0, name, OBJ_TREND, 0, t1, p1, t2, p2)) {
      ObjectSetInteger(0, name, OBJPROP_COLOR, cl);
      ObjectSetInteger(0, name, OBJPROP_STYLE, style);
      ObjectSetInteger(0, name, OBJPROP_WIDTH, width);
   }
}

//+------------------------------------------------------------------+
//| 辅助函数：绘制水平虚线                                           |
//+------------------------------------------------------------------+
void DrawDottedLine(string name, datetime t1, double p, datetime t2, color lineColor) {
   if(ObjectCreate(0, name, OBJ_TREND, 0, t1, p, t2, p)) {
      ObjectSetInteger(0, name, OBJPROP_COLOR, lineColor);
      ObjectSetInteger(0, name, OBJPROP_STYLE, STYLE_DOT);
      ObjectSetInteger(0, name, OBJPROP_WIDTH, 1);
   }
}

//+------------------------------------------------------------------+
//| 辅助函数：绘制转折点标签                                         |
//+------------------------------------------------------------------+
void DrawTextEx(string name, string text, datetime t, double p, color cl, int fontsize, bool isHigh) {
   if(ObjectCreate(0, name, OBJ_TEXT, 0, t, p)) {
      ObjectSetString(0, name, OBJPROP_TEXT, text);
      ObjectSetInteger(0, name, OBJPROP_COLOR, cl);
      ObjectSetInteger(0, name, OBJPROP_FONTSIZE, fontsize);
      ObjectSetString(0, name, OBJPROP_FONT, "Arial Bold");
      if(isHigh)
         ObjectSetInteger(0, name, OBJPROP_ANCHOR, ANCHOR_BOTTOM);
      else
         ObjectSetInteger(0, name, OBJPROP_ANCHOR, ANCHOR_TOP);
      ObjectSetInteger(0, name, OBJPROP_ALIGN, ALIGN_CENTER);
   }
}

//+------------------------------------------------------------------+
//| 主交易函数：OnTick逻辑                                           |
//+------------------------------------------------------------------+
void OnTick() {
   static datetime lastBarTime = 0;
   datetime currentBarTime = iTime(_Symbol, _Period, 1);
   if(currentBarTime == lastBarTime) return;
   lastBarTime = currentBarTime;

   // 清空并重新检测转折点
   ArrayResize(pivots, 0);
   int barsCount = Bars(_Symbol, _Period);
   int start = PivotLeft;
   int end = barsCount - PivotRight;

   for(int i = end - 1; i >= start; i--) {
      bool isPivotHigh = true, isPivotLow = true;
      double currentHigh = iHigh(_Symbol, _Period, i);
      double currentLow = iLow(_Symbol, _Period, i);
      for(int j = i - PivotLeft; j <= i + PivotRight; j++) {
         if(j < 0 || j >= barsCount || j == i) continue;
         if(iHigh(_Symbol, _Period, j) > currentHigh) isPivotHigh = false;
         if(iLow(_Symbol, _Period, j) < currentLow) isPivotLow = false;
      }
      if(isPivotHigh || isPivotLow) {
         Pivot p;
         p.time = iTime(_Symbol, _Period, i);
         p.price = isPivotHigh ? currentHigh : currentLow;
         p.isHigh = isPivotHigh;
         ArrayResize(pivots, ArraySize(pivots) + 1);
         pivots[ArraySize(pivots)-1] = p;
      }
   }

   // 形态识别：需至少5个转折点
   int pivotCount = ArraySize(pivots);
   if(pivotCount < 5) {
      g_patternFormationBar = -1;
      g_lockedPatternX = 0;
      return;
   }

   Pivot X = pivots[pivotCount - 5];
   Pivot A = pivots[pivotCount - 4];
   Pivot B = pivots[pivotCount - 3];
   Pivot C = pivots[pivotCount - 2];
   Pivot D = pivots[pivotCount - 1];

   bool patternFound = false;
   string patternType = "";

   // 检测看跌蝴蝶形态（高-低-高-低-高）
   if(X.isHigh && !A.isHigh && B.isHigh && !C.isHigh && D.isHigh) {
      double diff = X.price - A.price;
      if(diff > 0) {
         double idealB = A.price + 0.786 * diff;
         if(MathAbs(B.price - idealB) <= Tolerance * diff) {
            double BC = B.price - C.price;
            if(BC >= 0.382 * diff && BC <= 0.886 * diff) {
               double CD = D.price - C.price;
               if(CD >= 1.27 * diff && CD <= 1.618 * diff && D.price > X.price) {
                  patternFound = true;
                  patternType = "Bearish";
               }
            }
         }
      }
   }

   // 检测看涨蝴蝶形态（低-高-低-高-低）
   if(!X.isHigh && A.isHigh && !B.isHigh && C.isHigh && !D.isHigh) {
      double diff = A.price - X.price;
      if(diff > 0) {
         double idealB = A.price - 0.786 * diff;
         if(MathAbs(B.price - idealB) <= Tolerance * diff) {
            double BC = C.price - B.price;
            if(BC >= 0.382 * diff && BC <= 0.886 * diff) {
               double CD = C.price - D.price;
               if(CD >= 1.27 * diff && CD <= 1.618 * diff && D.price < X.price) {
                  patternFound = true;
                  patternType = "Bullish";
               }
            }
         }
      }
   }

   // 清理旧图形对象
      for(int i=ObjectsTotal(0,0)-1; i>=0; i--) {
         string objName = ObjectName(0, i, 0);
         if(StringFind(objName, "BF_", 0) == 0)
             ObjectDelete(0, objName);
      }

   // 绘制形态与交易点位（若检测到有效形态）
   if(patternFound) {
      Print(patternType, " Butterfly pattern detected at ", TimeToString(D.time, TIME_DATE|TIME_MINUTES|TIME_SECONDS));
      string signalPrefix = "BF_" + IntegerToString(X.time);
      color triangleColor = (patternType=="Bullish") ? clrBlue : clrRed;

      // 绘制蝴蝶形态的两个三角形
      DrawTriangle(signalPrefix+"_Triangle1", X.time, X.price, A.time, A.price, B.time, B.price, triangleColor, 2, true, true);
      DrawTriangle(signalPrefix+"_Triangle2", B.time, B.price, C.time, C.price, D.time, D.price, triangleColor, 2, true, true);

      // 绘制趋势线
      DrawTrendLine(signalPrefix+"_TL_XA", X.time, X.price, A.time, A.price, clrBlack, 2, STYLE_SOLID);
      DrawTrendLine(signalPrefix+"_TL_AB", A.time, A.price, B.time, B.price, clrBlack, 2, STYLE_SOLID);
      DrawTrendLine(signalPrefix+"_TL_BC", B.time, B.price, C.time, C.price, clrBlack, 2, STYLE_SOLID);
      DrawTrendLine(signalPrefix+"_TL_CD", C.time, C.price, D.time, D.price, clrBlack, 2, STYLE_SOLID);
      DrawTrendLine(signalPrefix+"_TL_XB", X.time, X.price, B.time, B.price, clrBlack, 2, STYLE_SOLID);
      DrawTrendLine(signalPrefix+"_TL_BD", B.time, B.price, D.time, D.price, clrBlack, 2, STYLE_SOLID);

      // 绘制转折点标签
      double point = SymbolInfoDouble(_Symbol, SYMBOL_POINT);
      double offset = 15 * point;
      double textY_X = (X.isHigh ? X.price + offset : X.price - offset);
      double textY_A = (A.isHigh ? A.price + offset : A.price - offset);
      double textY_B = (B.isHigh ? B.price + offset : B.price - offset);
      double textY_C = (C.isHigh ? C.price + offset : C.price - offset);
      double textY_D = (D.isHigh ? D.price + offset : D.price - offset);

      DrawTextEx(signalPrefix+"_Text_X", "X", X.time, textY_X, clrBlack, 11, X.isHigh);
      DrawTextEx(signalPrefix+"_Text_A", "A", A.time, textY_A, clrBlack, 11, A.isHigh);
      DrawTextEx(signalPrefix+"_Text_B", "B", B.time, textY_B, clrBlack, 11, B.isHigh);
      DrawTextEx(signalPrefix+"_Text_C", "C", C.time, textY_C, clrBlack, 11, C.isHigh);
      DrawTextEx(signalPrefix+"_Text_D", "D", D.time, textY_D, clrBlack, 11, D.isHigh);

      // 绘制中心标签
      datetime centralTime = (X.time + B.time) / 2;
      double centralPrice = D.price;
      if(ObjectCreate(0, signalPrefix+"_Text_Center", OBJ_TEXT, 0, centralTime, centralPrice)) {
         ObjectSetString(0, signalPrefix+"_Text_Center", OBJPROP_TEXT, (patternType=="Bullish") ? "Bullish Butterfly" : "Bearish Butterfly");
         ObjectSetInteger(0, signalPrefix+"_Text_Center", OBJPROP_COLOR, clrBlack);
         ObjectSetInteger(0, signalPrefix+"_Text_Center", OBJPROP_FONTSIZE, 11);
         ObjectSetString(0, signalPrefix+"_Text_Center", OBJPROP_FONT, "Arial Bold");
         ObjectSetInteger(0, signalPrefix+"_Text_Center", OBJPROP_ALIGN, ALIGN_CENTER);
      }

      // 计算交易点位并绘制
      datetime lineStart = D.time;
      datetime lineEnd = D.time + PeriodSeconds(_Period)*2;
      double entryPriceLevel, TP1Level, TP2Level, TP3Level, tradeDiff;

      if(patternType=="Bullish") {
         entryPriceLevel = SymbolInfoDouble(_Symbol, SYMBOL_ASK);
         TP3Level = C.price;
         tradeDiff = TP3Level - entryPriceLevel;
         TP1Level = entryPriceLevel + tradeDiff/3;
         TP2Level = entryPriceLevel + 2*tradeDiff/3;
      } else {
         entryPriceLevel = SymbolInfoDouble(_Symbol, SYMBOL_BID);
         TP3Level = C.price;
         tradeDiff = entryPriceLevel - TP3Level;
         TP1Level = entryPriceLevel - tradeDiff/3;
         TP2Level = entryPriceLevel - 2*tradeDiff/3;
      }

      DrawDottedLine(signalPrefix+"_EntryLine", lineStart, entryPriceLevel, lineEnd, clrMagenta);
      DrawDottedLine(signalPrefix+"_TP1Line", lineStart, TP1Level, lineEnd, clrForestGreen);
      DrawDottedLine(signalPrefix+"_TP2Line", lineStart, TP2Level, lineEnd, clrGreen);
      DrawDottedLine(signalPrefix+"_TP3Line", lineStart, TP3Level, lineEnd, clrDarkGreen);

      // 绘制交易点位标签（修复后语法）
      datetime labelTime = lineEnd + PeriodSeconds(_Period)/2;
      string entryLabel = (patternType=="Bullish") ? "BUY" : "SELL";
      entryLabel = entryLabel + " (" + DoubleToString(entryPriceLevel, _Digits) + ")";
      DrawTextEx(signalPrefix+"_EntryLabel", entryLabel, labelTime, entryPriceLevel, clrMagenta, 11, true);
      DrawTextEx(signalPrefix+"_TP1Label", "TP1 (" + DoubleToString(TP1Level, _Digits) + ")", labelTime, TP1Level, clrForestGreen, 11, true);
      DrawTextEx(signalPrefix+"_TP2Label", "TP2 (" + DoubleToString(TP2Level, _Digits) + ")", labelTime, TP2Level, clrGreen, 11, true);
      DrawTextEx(signalPrefix+"_TP3Label", "TP3 (" + DoubleToString(TP3Level, _Digits) + ")", labelTime, TP3Level, clrDarkGreen, 11, true);

      // 形态锁定与交易执行
      int currentBarIndex = Bars(_Symbol, _Period) - 1;
      if(g_patternFormationBar == -1) {
         g_patternFormationBar = currentBarIndex;
         g_lockedPatternX = X.time;
         Print("Pattern detected on bar ", currentBarIndex, ". Waiting for confirmation on next bar.");
         return;
      }
      if(currentBarIndex == g_patternFormationBar) {
         Print("Pattern is repainting; still on locked formation bar ", currentBarIndex, ". No trade yet.");
         return;
      }
      if(currentBarIndex > g_patternFormationBar) {
         if(g_lockedPatternX == X.time) {
            Print("Confirmed pattern (locked on bar ", g_patternFormationBar, "). Opening trade on bar ", currentBarIndex, ".");
            g_patternFormationBar = currentBarIndex;
            if(AllowTrading && !PositionSelect(_Symbol)) {
               double entryPriceTrade = 0, stopLoss = 0, takeProfit = 0;
               point = SymbolInfoDouble(_Symbol, SYMBOL_POINT);
               bool tradeResult = false;
               if(patternType=="Bullish") {
                  entryPriceTrade = SymbolInfoDouble(_Symbol, SYMBOL_ASK);
                  double diffTrade = TP2Level - entryPriceTrade;
                  stopLoss = entryPriceTrade - diffTrade * 3;
                  takeProfit = TP2Level;
                  tradeResult = obj_Trade.Buy(LotSize, _Symbol, entryPriceTrade, stopLoss, takeProfit, "Butterfly Signal");
               } else if(patternType=="Bearish") {
                  entryPriceTrade = SymbolInfoDouble(_Symbol, SYMBOL_BID);
                  double diffTrade = entryPriceTrade - TP2Level;
                  stopLoss = entryPriceTrade + diffTrade * 3;
                  takeProfit = TP2Level;
                  tradeResult = obj_Trade.Sell(LotSize, _Symbol, entryPriceTrade, stopLoss, takeProfit, "Butterfly Signal");
               }
               if(tradeResult) Print("Order opened successfully.");
               else Print("Order failed: ", obj_Trade.ResultRetcodeDescription());
            } else {
               Print("Position already open or trading disabled. No new trade.");
            }
         } else {
            g_patternFormationBar = currentBarIndex;
            g_lockedPatternX = X.time;
            Print("Pattern changed; updating lock on bar ", currentBarIndex, ". Waiting for confirmation.");
            return;
         }
      }
   } else {
      g_patternFormationBar = -1;
      g_lockedPatternX = 0;
   }
}