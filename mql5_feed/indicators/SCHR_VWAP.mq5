//+------------------------------------------------------------------+
//|                                                    SCHR_VWAP.mq5 |
//|                             Copyright 2023, Neozork HLD Project |
//|                                           https://github.com/... |
//+------------------------------------------------------------------+
#property copyright "Copyright 2023, Neozork HLD Project"
#property link      "https://github.com/..."
#property version   "1.00"
#property indicator_chart_window
#property indicator_buffers 1
#property indicator_plots   1
//--- plot VWAP
#property indicator_label1  "VWAP"
#property indicator_type1   DRAW_LINE
#property indicator_color1  clrBlue
#property indicator_style1  STYLE_SOLID
#property indicator_width1  2

//--- input parameters
input int InpPeriod = 20; // VWAP Period
input ENUM_APPLIED_PRICE InpAppliedPrice = PRICE_TYPICAL; // Applied price type

//--- indicator buffers
double VWAPBuffer[];

//--- global variables
double PriceVolume[];
double Volume[];

//+------------------------------------------------------------------+
//| Custom indicator initialization function                         |
//+------------------------------------------------------------------+
int OnInit()
{
   //--- indicator buffers mapping
   SetIndexBuffer(0, VWAPBuffer, INDICATOR_DATA);
   
   //--- set precision
   IndicatorSetInteger(INDICATOR_DIGITS, _Digits);
   
   //--- set first bar from what index will be drawn
   PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, InpPeriod);
   
   //--- indicator short name
   IndicatorSetString(INDICATOR_SHORTNAME, "SCHR_VWAP(" + (string)InpPeriod + ")");
   
   //--- initialization successful
   return(INIT_SUCCEEDED);
}

//+------------------------------------------------------------------+
//| Custom indicator iteration function                              |
//+------------------------------------------------------------------+
int OnCalculate(const int rates_total,
                const int prev_calculated,
                const datetime &time[],
                const double &open[],
                const double &high[],
                const double &low[],
                const double &close[],
                const long &tick_volume[],
                const long &volume[],
                const int &spread[])
{
   //--- check for minimum bars
   if(rates_total < InpPeriod)
      return(0);
      
   //--- set array as series
   ArraySetAsSeries(VWAPBuffer, true);
   ArraySetAsSeries(high, true);
   ArraySetAsSeries(low, true);
   ArraySetAsSeries(close, true);
   ArraySetAsSeries(volume, true);
   
   //--- calculate VWAP
   int limit = rates_total - prev_calculated;
   if(prev_calculated == 0)
      limit = rates_total - InpPeriod;
      
   for(int i = limit; i >= 0; i--)
   {
      double sum_pv = 0.0;
      double sum_vol = 0.0;
      
      for(int j = i; j < i + InpPeriod && j < rates_total; j++)
      {
         double typical_price = (high[j] + low[j] + close[j]) / 3.0;
         double vol = volume[j] > 0 ? volume[j] : 1;
         
         sum_pv += typical_price * vol;
         sum_vol += vol;
      }
      
      if(sum_vol > 0)
         VWAPBuffer[i] = sum_pv / sum_vol;
      else
         VWAPBuffer[i] = close[i];
   }
   
   //--- return value of prev_calculated for next call
   return(rates_total);
}
//+------------------------------------------------------------------+