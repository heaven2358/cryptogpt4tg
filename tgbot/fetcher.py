import logging, requests
from pytz import timezone
from datetime import datetime

from tgbot.config import AI_ORACLE_API_TEMPLATE


def fetch_price(coin_name: str, is_chinese: bool = False) -> str:
    """
    Fetches the median price of a given cryptocurrency from APRO AI Oracle, and formats it into a human-readable string.
    If is_chinese is True, the output string is in Chinese.
    If the API call fails, logs the error and returns an empty string.
    """
    
    url = AI_ORACLE_API_TEMPLATE.format(name=coin_name.lower())
    headers = {"accept": "application/json"}
    try:
        response = requests.get(url, headers=headers, timeout=5)
        if response.status_code == 200:
            data = response.json().get("data", {})
            logging.info(data)
            symbol = data.get("symbol", coin_name.upper())
            median_price = data.get("price")
            prices = data.get("prices", [])
            timestamp = data.get("timestamp")

            if is_chinese:
                lines = [f"{symbol} 的中位价格是 ${median_price:.2f} 美元。", "以下是详细的价格来源："]
            else:
                lines = [f"The median price of {symbol} is ${median_price:.2f} USD.", "The following are the detailed price sources:"]

            for p in prices:
                provider = p.get("provider_name", "Unknown")
                price = p.get("price")
                if price is not None:
                    lines.append(f"{provider:<18} ${price:.2f}")

            if timestamp:
                tz = timezone("America/Los_Angeles")
                ts = datetime.fromtimestamp(timestamp / 1000, tz)
                tstr = ts.strftime('%Y-%m-%d %H:%M:%S %Z').replace("PDT", "")
                lines.append(f"{'获取价格时间' if is_chinese else 'Get the price at'}：{tstr}(PST)")

            lines.append("\n数据由 APRO AI Oracle 提供，并通过 ATTPs 数据验证。" if is_chinese else "\nThis data is provided by APRO AI Oracle and verified by ATTPs data.")
            return "\n".join(lines)
    except Exception as e:
        logging.error(f"Error fetching price: {e}")
    return ""
