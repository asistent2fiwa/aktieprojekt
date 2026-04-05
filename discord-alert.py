# =============================================================================
# DISCORD ALERT SYSTEM - GEMA AI Trading
# =============================================================================
#
# Sender alerts til Discord når anbefalinger opstår.
# 
# Brug:
#   python discord-alert.py test
#   python discord-alert.py alert "NVDA" "KOEB" "RSI under 30"
#
# Opsætning:
#   1. Opret Discord webhook URL i din server
#   2. Sæt WEBHOOK_URL i denne fil ELLER i .env
#   3. Kør via cron/task scheduler hvert 5. minut
#
# =============================================================================

import os
import sys
import json
import requests
import argparse
from datetime import datetime
from pathlib import Path

# =============================================================================
# KONFIGURATION
# =============================================================================

WORKSPACE = Path(r"C:\Users\asist\.openclaw\workspace\projects\aktieprojekt")
WEBHOOK_URL = os.environ.get('DISCORD_WEBHOOK_URL', '')

# Fallback til .env
env_file = WORKSPACE / '.env'
if env_file.exists() and not WEBHOOK_URL:
    for line in env_file.read_text().splitlines():
        if line.startswith('DISCORD_WEBHOOK'):
            WEBHOOK_URL = line.split('=')[1].strip()

# =============================================================================
# DISCORD FUNKTIONER
# =============================================================================

def send_embed(webhook_url, title, description, color=0x00e5ff, fields=None, footer=None):
    """
    Send en rich embed til Discord webhook.
    
    Args:
        webhook_url: Discord webhook URL
        title: Embed titel
        description: Hovedbeskrivelse
        color: Embed farve (0x00e5ff = cyan)
        fields: Liste af {name, value, inline} dicts
        footer: Footer tekst
    """
    if not webhook_url:
        print("[X] Ingen webhook URL sat!")
        print("    Sæt DISCORD_WEBHOOK_URL i .env eller miljøvariabel")
        return False
    
    payload = {
        "username": "GEMA Alert",
        "avatar_url": "https://i.imgur.com/whatever.png",
        "embeds": [
            {
                "title": title,
                "description": description,
                "color": color,
                "timestamp": datetime.now().isoformat(),
            }
        ]
    }
    
    if fields:
        payload["embeds"][0]["fields"] = fields
    
    if footer:
        payload["embeds"][0]["footer"] = {"text": footer}
    
    try:
        response = requests.post(webhook_url, json=payload, timeout=10)
        if response.status_code == 204:
            print(f"[OK] Alert sendt: {title}")
            return True
        else:
            print(f"[X] Discord fejl: {response.status_code}")
            return False
    except Exception as e:
        print(f"[X] Netværksfejl: {e}")
        return False


def send_koeb_alert(ticker, price, signal, reason):
    """Send købsanbefaling."""
    fields = [
        {"name": "Ticker", "value": ticker, "inline": True},
        {"name": "Pris", "value": f"{price} DKK", "inline": True},
        {"name": "Signal", "value": signal, "inline": True},
    ]
    
    return send_embed(
        WEBHOOK_URL,
        f"📈 KØBSANBEFALING: {ticker}",
        reason,
        color=0x10B981,  # Grøn
        fields=fields,
        footer="GEMA AI Trading Assistant"
    )


def send_salg_alert(ticker, price, signal, reason):
    """Send salgsanbefaling."""
    fields = [
        {"name": "Ticker", "value": ticker, "inline": True},
        {"name": "Pris", "value": f"{price} DKK", "inline": True},
        {"name": "Signal", "value": signal, "inline": True},
    ]
    
    return send_embed(
        WEBHOOK_URL,
        f"📉 SALGSANBEFALING: {ticker}",
        reason,
        color=0xEF4444,  # Rød
        fields=fields,
        footer="GEMA AI Trading Assistant"
    )


def send_rsi_alert(ticker, rsi_value, direction):
    """Send RSI alert."""
    if direction == "oversolgt":
        color = 0x10B981  # Grøn - køb
        emoji = "📈"
    else:
        color = 0xEF4444  # Rød - salg
        emoji = "📉"
    
    return send_embed(
        WEBHOOK_URL,
        f"{emoji} RSI ALERT: {ticker}",
        f"RSI {rsi_value:.1f} - {direction}",
        color=color,
        fields=[
            {"name": "RSI", "value": f"{rsi_value:.1f}", "inline": True},
            {"name": "Status", "value": direction.title(), "inline": True},
        ],
        footer="GEMA AI Trading"
    )


def send_test():
    """Send test besked."""
    return send_embed(
        WEBHOOK_URL,
        "✅ GEMA Alert System Klar!",
        "Discord alerts er nu aktiveret for GEMA AI Trading Assistant.",
        color=0x00e5ff,  # Cyan
        footer="Test kl. " + datetime.now().strftime("%H:%M")
    )


# =============================================================================
# CLI
# =============================================================================

def main():
    parser = argparse.ArgumentParser(description='GEMA Discord Alert System')
    parser.add_argument('command', choices=['test', 'alert', 'rsi-alert'])
    parser.add_argument('--ticker', help='Aktie ticker')
    parser.add_argument('--price', help='Pris')
    parser.add_argument('--signal', help='Signal type')
    parser.add_argument('--reason', help='Begrundelse')
    parser.add_argument('--rsi', type=float, help='RSI værdi')
    
    args = parser.parse_args()
    
    if args.command == 'test':
        send_test()
    
    elif args.command == 'alert':
        if not all([args.ticker, args.signal, args.reason]):
            print("Brug: --ticker NVDA --signal KOEB --reason 'RSI under 30'")
            return
        
        if args.signal.upper() in ['KOEB', 'KOB', 'BUY']:
            send_koeb_alert(args.ticker, args.price or "?", args.signal, args.reason)
        else:
            send_salg_alert(args.ticker, args.price or "?", args.signal, args.reason)
    
    elif args.command == 'rsi-alert':
        if not args.ticker or not args.rsi:
            print("Brug: --ticker NVDA --rsi 28")
            return
        
        direction = "oversolgt" if args.rsi < 30 else "overkobt"
        send_rsi_alert(args.ticker, args.rsi, direction)


if __name__ == "__main__":
    main()
