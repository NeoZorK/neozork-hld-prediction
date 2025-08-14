//+------------------------------------------------------------------+
//|                                                    SCHR_DDAV.mq5 |
//| Copyright 2020, Shcherbyna Rostyslav                             |
//+------------------------------------------------------------------+
#property copyright   "Copyright 2020, \x2662 Shcherbyna Rostyslav"
#property version     "1.04"
#property description "\x2662 SCHR \x2662 DDAV"
#property indicator_chart_window
#property indicator_buffers         6
#property indicator_plots           6

//-----INCLUDES------
#include <RInclude\RNotify.mqh>
#include <RInclude\ROnOpenPrice.mqh>
#include <RInclude\RSAbilityIndex.mqh>

// Class for Check if it is New Bar
ROnOpenPrice _NEWBAR;

// Class for Calculating RSAbility Index
RSAbilityIndex _RSAI;

// Class for Notify via Alerts & Pushes
RNotify _Notify;

//---Indicator Buffers:
//---FAST Line
#property indicator_type1   DRAW_LINE
#property indicator_color1  Aqua
#property indicator_width1  1
#property indicator_label1  "Fast"
//---SLOW Line
#property indicator_type2   DRAW_LINE
#property indicator_color2  DarkViolet
#property indicator_width2  1
#property indicator_label2  "Slow"
//--- Direction
#property indicator_label3  "Direction"
#property indicator_type3   DRAW_NONE
#property indicator_color3  clrBlack
#property indicator_style3  STYLE_SOLID
#property indicator_width3  1
//--- Signal
#property indicator_label4  "Signal"
#property indicator_type4   DRAW_NONE
#property indicator_color4  clrNONE
#property indicator_style4  STYLE_SOLID
#property indicator_width4  1
//--- DRAW_Signal_BUY
#property indicator_label5  "DRAW_Signal_BUY"
#property indicator_type5   DRAW_ARROW
#property indicator_color5  clrBlue
#property indicator_style5  STYLE_SOLID
#property indicator_width5  50
//--- DRAW_Signal_SELL
#property indicator_label6  "DRAW_Signal_SELL"
#property indicator_type6   DRAW_ARROW
#property indicator_color6  clrRed
#property indicator_style6  STYLE_SOLID
#property indicator_width6  50

//--- input parameters
input int                _inpFastMoment=25;          // Fast Moment (25)
input int                _inpSlowMoment=50;          // Slow Moment (50)
sinput short             _DrawCode=204;              // DrawCode    (204)
sinput bool              _Alert=false;               // Alerts ?
sinput bool              _Push=false;                // PUSH ?
sinput string            _PushText="\x2662 DDAV";    // PUSH Comment
sinput bool              _CalcRSAI=false;            // Calc RSAI
input  int               _RSAI_MaxRisk_pts=500;      // RSAI MaxRisk pts
input  int               _RSAI_MinProfit_pts=150;    // RSAI MinProfit pts

const int period = _inpSlowMoment*2;

//--- indicator buffers
double                  _Fast_Buf[];
double                  _Slow_Buf[];
double                  _Direction[];
double                  _Signal[];
double                  _DRAW_Signal_BUY[];
double                  _DRAW_Signal_SELL[];

//GLOBAL VARS
double                  Fast_SmoothFactor, Slow_SmoothFactor;
//+------------------------------------------------------------------+
//| Trading Rule Signals (6)                                         |
//+------------------------------------------------------------------+
enum ENUM_TR_SIGNAL
  {
   NOTRADE,
   BUY,
   SELL,
   DBL_BUY,                      // Needed For Reverse (In Netting Broker Account)
   DBL_SELL,                     // Needed For Reverse (In Netting Broker Account)
   BUY_AND_SELL,                 // Simultaneously Buy and Sell (On Hedge Accounts)
  };
//+------------------------------------------------------------------+
//| Expert deinitialization function                                 |
//+------------------------------------------------------------------+
void OnDeinit(const int reason)
  {
   _RSAI.ResetData();
  }
//+------------------------------------------------------------------+
//| Custom indicator initialization function                         |
//+------------------------------------------------------------------+
void OnInit()
  {
// Init NEWBAR
   _NEWBAR.Init();

   SetIndexBuffer(0,_Fast_Buf,INDICATOR_DATA);
   PlotIndexSetInteger(0,PLOT_DRAW_BEGIN,period-1);
   PlotIndexSetDouble(0,PLOT_EMPTY_VALUE,0);

   SetIndexBuffer(1,_Slow_Buf,INDICATOR_DATA);
   PlotIndexSetInteger(1,PLOT_DRAW_BEGIN,period-1);
   PlotIndexSetDouble(1,PLOT_EMPTY_VALUE,0);

   SetIndexBuffer(2,_Direction,INDICATOR_DATA);
   PlotIndexSetInteger(2,PLOT_DRAW_BEGIN,period-1);
   PlotIndexSetDouble(2,PLOT_EMPTY_VALUE,0);

   SetIndexBuffer(3,_Signal,INDICATOR_DATA);
   PlotIndexSetInteger(3,PLOT_DRAW_BEGIN,period-1);
   PlotIndexSetDouble(3,PLOT_EMPTY_VALUE,0);

//_DRAW_Signal_BUY
   SetIndexBuffer(4,_DRAW_Signal_BUY,INDICATOR_DATA);
   PlotIndexSetInteger(4,PLOT_DRAW_BEGIN,period-1);
   PlotIndexSetDouble(4,PLOT_EMPTY_VALUE,0);
   PlotIndexSetInteger(4,PLOT_ARROW,_DrawCode);

//_DRAW_Signal_SELL
   SetIndexBuffer(5,_DRAW_Signal_SELL,INDICATOR_DATA);
   PlotIndexSetInteger(5,PLOT_DRAW_BEGIN,period-1);
   PlotIndexSetDouble(5,PLOT_EMPTY_VALUE,0);
   PlotIndexSetInteger(5,PLOT_ARROW,_DrawCode);

   IndicatorSetString(INDICATOR_SHORTNAME,"DDAV \x2662 ("+string(_inpFastMoment)+")/("+string(_inpSlowMoment)+")");

   Fast_SmoothFactor=2.0/(1.0+_inpFastMoment);
   Slow_SmoothFactor=2.0/(1.0+_inpSlowMoment);

   _RSAI.Init(PERIOD_CURRENT,_Symbol,_RSAI_MaxRisk_pts,_RSAI_MinProfit_pts);
   _Notify.Init();
  }
//+------------------------------------------------------------------+
//| Double DAV                                                       |
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
//--- Check For Data
   if(rates_total<period-1)
      return(0);

//---POST_INIT
   int limit;
   if(prev_calculated<period-1)
     {
      limit=period-1;

      for(int i=0; i<limit; i++)
        {
         _Fast_Buf[i]=open[i];
         _Slow_Buf[i]=open[i];
        }
     }
   else
      limit=prev_calculated-1;

//--- MAIN CYCLE
   for(int i=limit; i<rates_total && !IsStopped(); i++)
     {
      //---Deafult
      _Direction[i]=NOTRADE;
      _Signal[i]=NOTRADE;
      _Fast_Buf[i]=0;
      _Slow_Buf[i]=0;
      _DRAW_Signal_BUY[i]=0;
      _DRAW_Signal_SELL[i]=0;

      //---  Fast & Slow Momentums
      double Fast_Momentum=fabs(Momentum(i,_inpFastMoment,open));
      double Slow_Momentum=fabs(Momentum(i,_inpSlowMoment,open));

      //---  FAST & SLOW DAV
      _Fast_Buf[i]=(open[i]*Fast_SmoothFactor*Fast_Momentum)+_Fast_Buf[i-1]*(1-Fast_SmoothFactor*Fast_Momentum);
      _Slow_Buf[i]=(open[i]*Slow_SmoothFactor*Slow_Momentum)+_Slow_Buf[i-1]*(1-Slow_SmoothFactor*Slow_Momentum);

      //Check Signals
      if(_Fast_Buf[i]>_Slow_Buf[i])
        {
         _Direction[i]=BUY;
        }
      else
         if(_Fast_Buf[i]<_Slow_Buf[i])
           {
            _Direction[i]=SELL;
           }//END OF CHECK DIRECTION

      //Check Signal
      if(_Direction[i]==BUY && _Direction[i-1]!=BUY)
        {
         _Signal[i]=BUY;
         _DRAW_Signal_BUY[i]=open[i];

         //Send Signal to RS Ability Index
         if(_CalcRSAI)
           {
            _RSAI.AddNewSignal((ENUM_IND_SIGNAL)_Signal[i],time[i],open[i]);
           }
         Notify(i);
        }
      else
        {
         if(_Direction[i]==SELL && _Direction[i-1]!=SELL)
           {
            _Signal[i]=SELL;
            _DRAW_Signal_SELL[i]=open[i];

            //Send Signal to RS Ability Index
            if(_CalcRSAI)
              {
               _RSAI.AddNewSignal((ENUM_IND_SIGNAL)_Signal[i],time[i],open[i]);
              }
            Notify(i);
           }
        }//END OF CHECK SIGNAL
     }//END OF FOR

//Calculate RSAI
   if(_CalcRSAI)
     {
      //Try to Calculate when all Indicator data was ready
      if(rates_total==prev_calculated)
         _RSAI.CalculateData();
     }

   return(rates_total);
  }
//+------------------------------------------------------------------+
//| Momentum                                                         |
//+------------------------------------------------------------------+
double Momentum(int &i,const int &PeriodMomentum,const double &open[])
  {
   double momentum=0.0, UpSum=0.0, DownSum=0.0;

   if(i>=PeriodMomentum && ArrayRange(open,0)>i)
     {
      for(int j=0; j<PeriodMomentum; j++)
        {
         double diff=open[i-j]-open[i-j-1];

         if(diff>0.0)
            UpSum+=diff;
         else
            DownSum+=(-diff);
        }

      if(UpSum+DownSum!=0.0)
         momentum=(UpSum-DownSum)/(UpSum+DownSum);
     }
   return(momentum);
  }
//+------------------------------------------------------------------+
//+------------------------------------------------------------------+
//|  Notification Alert and Push                                     |
//+------------------------------------------------------------------+
void Notify(const int &i)
  {
//Form Notification Message:
   string txt = _PushText +(string)_inpFastMoment + "::"
                +(string)_inpSlowMoment+ "=> "
                + EnumToString(ENUM_TR_SIGNAL(_Signal[i]));

//Fill info
   STRUCT_NOTIFY n= {};

   n.acc_number=false;
   n.account_fifo_close=true;
   n.broker=false;
   n.custom_text=txt;
   n.holder_name=false;
   n.magic=55555;
   n.pair=_Symbol;
   n.period=_Period;
   n.server=false;
   n.time=false;
   n.trade_allow_for_robot=false;
   n.trade_allowed_by_broker=true;
   n.trade_mode=true;


   if(_Alert)
      _Notify.Notify_Alert(n);

   if(_Push)
      _Notify.Notify_Push(n,true);

  }//END OF NOTIFY
//+------------------------------------------------------------------+

//+------------------------------------------------------------------+
