#!/bin/bash
# QuillyOS Telegram Bot Startup Script
# Usage: qbot-start    (starts bot in background)
#        qbot-stop     (stops bot)
#        qbot-status   (shows if bot is running)
#        qbot-log      (tails the log)

BOT_DIR="$HOME/quillyos-nexus/engines/frontend"
BOT_SCRIPT="$BOT_DIR/telegram_bot.py"
BOT_LOG="$BOT_DIR/bot.log"
BOT_PID="$BOT_DIR/bot.pid"

case "${1:-start}" in
    start)
        if [ -f "$BOT_PID" ] && kill -0 "$(cat "$BOT_PID")" 2>/dev/null; then
            echo "[+] Bot already running (PID: $(cat $BOT_PID))"
            exit 0
        fi
        cd "$BOT_DIR" || exit 1
        nohup python3 "$BOT_SCRIPT" > "$BOT_LOG" 2>&1 &
        echo $! > "$BOT_PID"
        echo "[+] Bot started. PID: $(cat $BOT_PID)"
        echo "[+] Log: $BOT_LOG"
        ;;
    stop)
        if [ -f "$BOT_PID" ]; then
            kill "$(cat "$BOT_PID")" 2>/dev/null
            rm -f "$BOT_PID"
            echo "[+] Bot stopped."
        else
            pkill -f telegram_bot.py 2>/dev/null
            echo "[+] Bot stopped (via pkill)."
        fi
        ;;
    status)
        if [ -f "$BOT_PID" ] && kill -0 "$(cat "$BOT_PID")" 2>/dev/null; then
            echo "[+] Bot running (PID: $(cat $BOT_PID))"
            echo "[+] Log size: $(stat -c%s $BOT_LOG 2>/dev/null || echo 0) bytes"
        else
            echo "[!] Bot not running"
        fi
        ;;
    log)
        tail -f "$BOT_LOG"
        ;;
    restart)
        $0 stop
        sleep 1
        $0 start
        ;;
    *)
        echo "Usage: qbot-{start|stop|status|log|restart}"
        echo ""
        echo "  start   — Start bot in background"
        echo "  stop    — Stop bot"
        echo "  status  — Check if bot is running"
        echo "  log     — Tail the log file"
        echo "  restart — Stop then start"
        ;;
esac
