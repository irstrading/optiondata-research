from flask import Flask, render_template, jsonify
from nsepython import nse_option_chain, nse_get_quote, nse_get_index_quote
from datetime import datetime
from vollib.black_scholes.greeks import analytical

app = Flask(__name__)

def calculate_greeks_for_option(option, underlying_value, risk_free_rate):
    """
    Calculates the greeks for a single option contract.
    """
    try:
        S = underlying_value
        K = option['strikePrice']
        sigma = option['impliedVolatility'] / 100 # Convert from percentage
        flag = 'c' if option['optionType'] == 'Call' else 'p'

        # Calculate time to expiration in years
        expiry_date = datetime.strptime(option['expiryDate'], '%d-%b-%Y')
        time_to_expiry = (expiry_date - datetime.now()).days / 365.25

        # If time to expiry is negative or zero, greeks are not meaningful
        if time_to_expiry <= 0:
            return {}

        # Calculate greeks using vollib
        greeks = {
            'delta': analytical.delta(flag, S, K, time_to_expiry, risk_free_rate, sigma),
            'gamma': analytical.gamma(flag, S, K, time_to_expiry, risk_free_rate, sigma),
            'vega': analytical.vega(flag, S, K, time_to_expiry, risk_free_rate, sigma),
            'theta': analytical.theta(flag, S, K, time_to_expiry, risk_free_rate, sigma)
        }
        return greeks
    except Exception as e:
        # This can happen if IV is 0 or other data is missing/invalid
        # print(f"Could not calculate greeks for strike {option['strikePrice']}: {e}")
        return {}


def calculate_max_pain(data):
    """
    Calculates the Max Pain strike price from option chain data.
    """
    if not data or 'records' not in data or not data['records']['data']:
        return 0

    oc_data = data['records']['data']
    strike_prices = [record['strikePrice'] for record in oc_data if 'strikePrice' in record]

    total_loss_at_strike = {}

    for strike_s in strike_prices:
        total_loss = 0
        for record in oc_data:
            # Calculate loss from Calls
            if 'CE' in record and record['CE']:
                ce = record['CE']
                if ce['strikePrice'] < strike_s:
                    total_loss += (strike_s - ce['strikePrice']) * ce['openInterest']

            # Calculate loss from Puts
            if 'PE' in record and record['PE']:
                pe = record['PE']
                if pe['strikePrice'] > strike_s:
                    total_loss += (pe['strikePrice'] - strike_s) * pe['openInterest']

        total_loss_at_strike[strike_s] = total_loss

    if not total_loss_at_strike:
        return 0

    # Find the strike with the minimum loss
    max_pain_strike = min(total_loss_at_strike, key=total_loss_at_strike.get)
    return max_pain_strike

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/option-chain/<symbol>')
def get_option_chain(symbol):
    try:
        # Fetch the option chain data for the given symbol
        oc_data = nse_option_chain(symbol.upper())
        if not oc_data or 'records' not in oc_data or not oc_data['records']['data']:
            return jsonify({"error": "No option chain data found for this symbol."}), 404

        # Calculate Max Pain
        max_pain = calculate_max_pain(oc_data)

        # Add max_pain to the response
        response_data = oc_data
        response_data['records']['maxPain'] = max_pain

        # Calculate Greeks for each option
        underlying_value = response_data['records']['underlyingValue']
        risk_free_rate = 0.05 # Assume 5% risk-free rate

        for record in response_data['records']['data']:
            if 'CE' in record and record['CE']:
                ce_greeks = calculate_greeks_for_option(record['CE'], underlying_value, risk_free_rate)
                record['CE'].update(ce_greeks)

            if 'PE' in record and record['PE']:
                pe_greeks = calculate_greeks_for_option(record['PE'], underlying_value, risk_free_rate)
                record['PE'].update(pe_greeks)

        return jsonify(response_data)
    except Exception as e:
        # Log the error for debugging
        print(f"Error fetching option chain for {symbol}: {e}")
        return jsonify({"error": "Failed to fetch option chain data."}), 500

@app.route('/api/index-quotes')
def get_index_quotes():
    try:
        nifty50 = nse_get_index_quote("NIFTY 50")
        banknifty = nse_get_index_quote("NIFTY BANK")
        return jsonify({
            "nifty50": {
                "lastPrice": nifty50.get('lastPrice', 0),
                "change": nifty50.get('change', 0),
                "pChange": nifty50.get('pChange', 0)
            },
            "banknifty": {
                "lastPrice": banknifty.get('lastPrice', 0),
                "change": banknifty.get('change', 0),
                "pChange": banknifty.get('pChange', 0)
            }
        })
    except Exception as e:
        print(f"Error fetching index quotes: {e}")
        return jsonify({"error": "Failed to fetch index quotes."}), 500

@app.route('/api/watchlist')
def get_watchlist():
    # For this example, we'll screen a predefined list of NIFTY stocks.
    # In a real application, this list could be much larger (e.g., NIFTY 200).
    symbols_to_scan = ['RELIANCE', 'TCS', 'INFY', 'HDFCBANK', 'ICICIBANK', 'SBIN']
    watchlist = []

    for symbol in symbols_to_scan:
        try:
            quote = nse_get_quote(symbol)
            if quote:
                # Basic filter: Let's say we're interested in stocks with a positive change.
                # The 'reason' can be made more sophisticated later.
                if quote.get('change', 0) > 0:
                    watchlist.append({
                        "symbol": symbol,
                        "reason": "Positive Momentum",
                        "currentPrice": quote.get('lastPrice', 0),
                        "volume": quote.get('totalTradedVolume', 0), # Assuming this key, may need adjustment
                        "oiChange": "N/A" # OI change is not in a simple quote
                    })
        except Exception as e:
            print(f"Could not fetch watchlist data for {symbol}: {e}")
            # Continue to the next symbol
            pass

    return jsonify(watchlist)

if __name__ == '__main__':
    app.run(debug=True)
