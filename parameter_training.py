//@version=5
strategy("BTC 形態識別 1 - 顯示全還原版", 
     overlay=true, 
     initial_capital=300, 
     currency="USD", 
     default_qty_type=strategy.cash, 
     default_qty_value=1500, 
     commission_type=strategy.commission.percent, 
     commission_value=0.04, 
     calc_on_every_tick = true)

// ==========================================
// --- ⚙️ 參數設定 (同步 Python) ---
// ==========================================
climax_mult   = 4.5          
lookback15    = 50        
lookback5     = 10     
adx_threshold = 25.15      
bbw_threshold = 0.0039   
solid_ratio   = 0.7  
er_length = 18
er_thr = 0.1
r2_len = 10
r2_thr = 0.2
sl_pct        = 1.9       
tp_pct        = 4.0 


min_move_pts  = 500.0
max_loss_pts  = 200
min_gap       = 600
// ==========================================
// --- ⚙️ 指標計算 ---
// ==========================================
body = math.abs(close - open)
avg_body = ta.sma(body, 20) 
upper15 = ta.highest(high[1], lookback15)
lower15 = ta.lowest(low[1], lookback15)
m5_hh = ta.highest(high[1], lookback5)
m5_ll = ta.lowest(low[1], lookback5)

// 效率比 ER (長度 8)
length_er = er_length
netChg = math.abs(close - close[length_er])
totalChg = math.sum(math.abs(close - close[1]), length_er)
efficiencyRatio = totalChg != 0 ? netChg / totalChg : 0
isEfficient = efficiencyRatio > er_thr

// 線性回歸 R2
r2_length    = input.int(r2_len, "R2 週期")
r2_threshold = input.float(r2_thr, "R2 門檻")
r_value = ta.correlation(close, bar_index, r2_length)
r_squared = math.pow(r_value, 2)
is_linear_trend = r_squared > r2_threshold

// ADX & BBW
[_, _, adx_v] = ta.dmi(14, 14)
bbw_v = (ta.highest(high, 14) - ta.lowest(low, 14)) / ta.sma(close, 14)

// 形態判定
is_climax = body > avg_body * climax_mult
is_green_streak = close > open and close[1] > open[1]
is_red_streak   = close < open and close[1] < open[1]

// 進場狀態分類 (用於 bgcolor)
is_breakout = ((close > upper15 and (is_climax or is_green_streak)) or (close < lower15 and (is_climax or is_red_streak))) and isEfficient
is_narrow   = adx_v >= adx_threshold and bbw_v <= bbw_threshold and not is_breakout
is_wide     = adx_v >= 20 and bbw_v > bbw_threshold and not is_breakout
is_choppy   = adx_v < adx_threshold and bbw_v <= bbw_threshold and not is_breakout
wide_vol_ok = (ta.highest(high, 5) - ta.lowest(low, 5)) > 150
is_wide_upper = upper15 - lower15 > min_gap

// 背景顏色 (還原界面)
bg_color = is_breakout ? color.new(#ff5252, 85) : is_narrow ? color.new(color.orange, 85) : is_wide ? color.new(#1dec24, 92) : is_choppy ? color.new(#1a1357, 86) : color.new(color.black, 95)
bgcolor(bg_color)

// 盈虧計算函數
calc_pnl(ent_p, ext_p, qty, long_pos) =>
    float gross = long_pos ? (ext_p - ent_p) * qty : (ent_p - ext_p) * qty
    float fees  = (ent_p * qty * 0.0004) + (ext_p * qty * 0.0004)
    gross - fees

// ==========================================
// --- ⚔️ 進場邏輯 ---
// ==========================================
can_enter = (is_breakout or is_narrow or (is_wide and wide_vol_ok)) and isEfficient and is_linear_trend and is_wide_upper
long_cond  = can_enter and close > upper15 and close > m5_hh
short_cond = can_enter and close < lower15 and close < m5_ll

if (strategy.position_size == 0)
    if (long_cond)
        strategy.entry("Long", strategy.long, comment="long")
        alert("🚀 BTC 建議【做多】進場！價格：" + str.tostring(close, "#.#"), alert.freq_once_per_bar)
    else if (short_cond)
        strategy.entry("Short", strategy.short, comment="short")
        alert("🔻 BTC 建議【做空】進場！價格：" + str.tostring(close, "#.#"), alert.freq_once_per_bar)

// ==========================================
// --- 🛡️ 離場邏輯 (完全同步 Python 並還原界面) ---
// ==========================================
ent_p = strategy.position_avg_price
cur_q = math.abs(strategy.position_size)
is_l  = strategy.position_size > 0
is_s  = strategy.position_size < 0

// 實體判斷
full_len = high - low
is_solid_body = full_len > 0 ? (body / full_len) >= solid_ratio : false
is_solid_red   = (close < open) and is_solid_body
is_solid_green = (close > open) and is_solid_body

// 形態反轉訊號 (同步 Python prev 邏輯使用 [1])
is_rev_r = is_solid_red and (body > avg_body * climax_mult)
is_rev_g = is_solid_green and (body > avg_body * climax_mult)
loss_l = is_solid_red  and is_solid_red[1]
loss_s = is_solid_green and is_solid_green[1]

// 離場觸發判定
morph_exit_sig = is_l ? (loss_l) : (loss_s)
curr_profit_pts = is_l ? (close - ent_p) : (ent_p - close)
// 獲利移動平倉門檻 (Profit > 0)
safe_exit = (math.abs(close - ent_p) >= min_move_pts) and (curr_profit_pts > 0)
// 虧損移動平倉門檻 (Loss < 0)
safe_loss_exit = (math.abs(close - ent_p) >= max_loss_pts) and (curr_profit_pts < 0)
// 整合觸發器
exit_trigger = (safe_exit or safe_loss_exit) and morph_exit_sig

// 執行離場
if (is_l)
    float pnl = calc_pnl(ent_p, close, cur_q, true)
    if (exit_trigger)
        strategy.close("Long", comment="Take Profit\n" + (pnl >= 0 ? "+" : "") + str.tostring(pnl, "#.##") + " USD")
        alert("⚠️ BTC 形態反轉【平多】跑路！盈虧：" + str.tostring(pnl, "#.##"), alert.freq_once_per_bar)
    
    strategy.exit("Exit Long", "Long", stop=ent_p*(1-sl_pct/100), limit=ent_p*(1+tp_pct/100), 
          comment_loss="Stop long\n" + str.tostring(calc_pnl(ent_p, ent_p*(1-sl_pct/100), cur_q, true), "#.##") + " USD", 
          comment_profit="Stop long\n+" + str.tostring(calc_pnl(ent_p, ent_p*(1+tp_pct/100), cur_q, true), "#.##") + " USD")

if (is_s)
    float pnl = calc_pnl(ent_p, close, cur_q, false)
    if (exit_trigger)
        strategy.close("Short", comment="Take Profit\n" + (pnl >= 0 ? "+" : "") + str.tostring(pnl, "#.##") + " USD")
        alert("⚠️ BTC 形態反轉【平空】跑路！盈虧：" + str.tostring(pnl, "#.##"), alert.freq_once_per_bar)
        
    strategy.exit("Exit Short", "Short", stop=ent_p*(1+sl_pct/100), limit=ent_p*(1-tp_pct/100), 
          comment_loss="Stop short\n" + str.tostring(calc_pnl(ent_p, ent_p*(1+sl_pct/100), cur_q, false), "#.##") + " USD", 
          comment_profit="Stop short\n+" + str.tostring(calc_pnl(ent_p, ent_p*(1-tp_pct/100), cur_q, false), "#.##") + " USD")

// ==========================================
// --- 📊 全功能面板 (還原原樣) ---
// ==========================================
var table board = table.new(position.top_right, 2, 13, bgcolor=color.new(color.black, 85), border_width=1, border_color=color.gray)
float tp_price = is_l ? ent_p * (1 + tp_pct/100) : is_s ? ent_p * (1 - tp_pct/100) : na
float sl_price = is_l ? ent_p * (1 - sl_pct/100) : is_s ? ent_p * (1 + sl_pct/100) : na

if barstate.islast
    table.cell(board, 0, 0, "suggestion", text_color=color.white)
    table.cell(board, 1, 0, is_l ? "持有多單" : is_s ? "持有空單" : long_cond ? " 建議做多" : short_cond ? "建議做空" :"Wait", text_color=color.lime)
    table.cell(board, 0, 1, "TP price", text_color=color.lime)
    table.cell(board, 1, 1, not na(tp_price) ? str.tostring(tp_price, "#.#") : "--",text_color = color.lime)
    table.cell(board, 0, 2, "SL price", text_color=color.red)
    table.cell(board, 1, 2, not na(sl_price) ? str.tostring(sl_price, "#.#") : "--",text_color = color.red)
    table.cell(board, 0, 3, "Pattern-based Exit", text_color=color.orange)
    table.cell(board, 1, 3, (is_l or is_s) and exit_trigger ? str.tostring(open, "#.#") : "--", text_color=exit_trigger ? color.red : color.white)
    float p_usd = (is_l or is_s) ? calc_pnl(ent_p, close, cur_q, is_l) : 0
    table.cell(board, 0, 4, "Current Profit (USD)", text_color=color.white)
    table.cell(board, 1, 4, str.tostring(p_usd, "#.##") + " USD", text_color=p_usd >= 0 ? color.lime : color.red)
    table.cell(board, 0, 5, "BTC price", text_color=color.yellow)
    table.cell(board, 1, 5, str.tostring(close, "#.#"))
    table.cell(board, 0, 6, "Entry", text_color=color.green)
    table.cell(board, 1, 6, (is_l or is_s) ? str.tostring(ent_p, "#.#") : (long_cond ? str.tostring(upper15, "#.#") : str.tostring(lower15, "#.#")), text_color=color.blue)

// 繪圖
plot(upper15, "15M 壓力", color=color.new(color.red, 60), style=plot.style_stepline)
plot(lower15, "15M 支撐", color=color.new(color.green, 60), style=plot.style_stepline)
