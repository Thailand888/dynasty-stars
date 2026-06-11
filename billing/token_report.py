#!/usr/bin/env python3
"""
token_report.py — учёт расхода токенов Hermes Agent и перевод в стоимость
для выставления счёта клиенту.

Источник данных: SQLite-база сессий Hermes (~/.hermes/state.db, таблица sessions).
База открывается ТОЛЬКО НА ЧТЕНИЕ (mode=ro) — запись/изменения исключены.

Цены по умолчанию — OpenRouter, Anthropic Claude Opus:
  вход  (input)  ~ $15 / 1M токенов
  выход (output) ~ $75 / 1M токенов
Курс USD->RUB по умолчанию ~90.

Использование:
  python3 token_report.py
  python3 token_report.py --from 2026-06-07 --to 2026-06-11
  python3 token_report.py --rub-rate 92 --in-price 15 --out-price 75
  python3 token_report.py --db /Users/thai/.hermes/state.db
"""
import argparse
import os
import sqlite3
import sys
from datetime import datetime, timezone

DEFAULT_DB = os.path.expanduser("~/.hermes/state.db")
DEFAULT_IN_PRICE = 15.0    # USD за 1M входных токенов
DEFAULT_OUT_PRICE = 75.0   # USD за 1M выходных токенов
DEFAULT_RUB_RATE = 90.0    # RUB за 1 USD


def parse_date(s):
    """Парсит YYYY-MM-DD (или YYYY-MM-DD HH:MM:SS) в Unix timestamp (UTC)."""
    for fmt in ("%Y-%m-%d %H:%M:%S", "%Y-%m-%d"):
        try:
            dt = datetime.strptime(s, fmt).replace(tzinfo=timezone.utc)
            return dt.timestamp()
        except ValueError:
            continue
    raise argparse.ArgumentTypeError(
        f"Неверный формат даты: {s!r}. Используйте YYYY-MM-DD"
    )


def open_ro(db_path):
    if not os.path.exists(db_path):
        sys.exit(f"ОШИБКА: база не найдена: {db_path}")
    uri = f"file:{db_path}?mode=ro"
    return sqlite3.connect(uri, uri=True)


def fmt_money(x):
    return f"{x:,.2f}".replace(",", " ")


def fmt_int(x):
    return f"{x:,}".replace(",", " ")


def main():
    ap = argparse.ArgumentParser(
        description="Отчёт по расходу токенов Hermes и стоимости для счёта."
    )
    ap.add_argument("--db", default=DEFAULT_DB, help="путь к state.db")
    ap.add_argument("--from", dest="dfrom", type=parse_date,
                    help="начало периода YYYY-MM-DD (включительно)")
    ap.add_argument("--to", dest="dto", type=parse_date,
                    help="конец периода YYYY-MM-DD (включительно, до конца суток)")
    ap.add_argument("--in-price", type=float, default=DEFAULT_IN_PRICE,
                    help=f"цена входа USD/1M (def {DEFAULT_IN_PRICE})")
    ap.add_argument("--out-price", type=float, default=DEFAULT_OUT_PRICE,
                    help=f"цена выхода USD/1M (def {DEFAULT_OUT_PRICE})")
    ap.add_argument("--rub-rate", type=float, default=DEFAULT_RUB_RATE,
                    help=f"курс RUB/USD (def {DEFAULT_RUB_RATE})")
    args = ap.parse_args()

    # Если задан --to как дата без времени — расширяем до конца суток.
    dto = args.dto
    if dto is not None:
        dto = dto + 86400 - 1  # включительно весь день

    where = ["1=1"]
    params = []
    if args.dfrom is not None:
        where.append("started_at >= ?")
        params.append(args.dfrom)
    if dto is not None:
        where.append("started_at <= ?")
        params.append(dto)
    where_sql = " AND ".join(where)

    conn = open_ro(args.db)
    cur = conn.cursor()

    # Итоги.
    cur.execute(f"""
        SELECT
            COUNT(*),
            COALESCE(SUM(input_tokens),0),
            COALESCE(SUM(output_tokens),0),
            COALESCE(SUM(cache_read_tokens),0),
            COALESCE(SUM(cache_write_tokens),0),
            COALESCE(SUM(reasoning_tokens),0),
            COALESCE(SUM(COALESCE(actual_cost_usd, estimated_cost_usd)),0)
        FROM sessions WHERE {where_sql}
    """, params)
    (sess_n, in_tok, out_tok, cache_r, cache_w,
     reason_tok, provider_cost) = cur.fetchone()

    total_tok = in_tok + out_tok
    in_cost = in_tok / 1_000_000 * args.in_price
    out_cost = out_tok / 1_000_000 * args.out_price
    usd = in_cost + out_cost
    rub = usd * args.rub_rate

    # Разбивка по дням.
    cur.execute(f"""
        SELECT date(started_at,'unixepoch') AS day,
               COUNT(*) AS n,
               COALESCE(SUM(input_tokens),0),
               COALESCE(SUM(output_tokens),0)
        FROM sessions WHERE {where_sql}
        GROUP BY day ORDER BY day
    """, params)
    by_day = cur.fetchall()

    # Разбивка по платформам.
    cur.execute(f"""
        SELECT source,
               COUNT(*) AS n,
               COALESCE(SUM(input_tokens),0),
               COALESCE(SUM(output_tokens),0)
        FROM sessions WHERE {where_sql}
        GROUP BY source ORDER BY (SUM(input_tokens)+SUM(output_tokens)) DESC
    """, params)
    by_src = cur.fetchall()

    # Фактический диапазон дат.
    cur.execute(f"""
        SELECT datetime(MIN(started_at),'unixepoch'),
               datetime(MAX(started_at),'unixepoch')
        FROM sessions WHERE {where_sql}
    """, params)
    rmin, rmax = cur.fetchone()
    conn.close()

    p_from = datetime.fromtimestamp(args.dfrom, tz=timezone.utc).strftime("%Y-%m-%d") if args.dfrom else "(начало)"
    p_to = datetime.fromtimestamp(args.dto, tz=timezone.utc).strftime("%Y-%m-%d") if args.dto else "(конец)"

    line = "=" * 64
    print(line)
    print("  ОТЧЁТ ПО РАСХОДУ ТОКЕНОВ HERMES — для выставления счёта")
    print(line)
    print(f"  База:        {args.db}  (read-only)")
    print(f"  Период:      {p_from} .. {p_to}")
    print(f"  Данные за:   {rmin} .. {rmax} (UTC)")
    print(f"  Сессий:      {sess_n}")
    print(f"  Цены:        вход ${args.in_price}/1M, выход ${args.out_price}/1M, курс {args.rub_rate} RUB/USD")
    print(line)
    print("  ТОКЕНЫ")
    print(f"    Входные  (input):  {fmt_int(in_tok):>18}")
    print(f"    Выходные (output): {fmt_int(out_tok):>18}")
    print(f"    ВСЕГО (in+out):    {fmt_int(total_tok):>18}")
    print(f"    --- справочно (не тарифицируется ниже) ---")
    print(f"    Cache read:        {fmt_int(cache_r):>18}")
    print(f"    Cache write:       {fmt_int(cache_w):>18}")
    print(f"    Reasoning:         {fmt_int(reason_tok):>18}")
    print(line)
    print("  СТОИМОСТЬ")
    print(f"    Вход:   ${fmt_money(in_cost):>12}")
    print(f"    Выход:  ${fmt_money(out_cost):>12}")
    print(f"    ИТОГО:  ${fmt_money(usd):>12} USD")
    print(f"    ИТОГО:   {fmt_money(rub):>12} RUB  (курс {args.rub_rate})")
    print(f"    (для сверки) оценка провайдера: ${fmt_money(provider_cost)} USD")
    print(line)
    print("  РАЗБИВКА ПО ДНЯМ")
    print(f"    {'Дата':<12}{'Сес':>5}{'Вход':>14}{'Выход':>13}{'USD':>11}{'RUB':>13}")
    for day, n, di, do in by_day:
        du = di / 1_000_000 * args.in_price + do / 1_000_000 * args.out_price
        print(f"    {day:<12}{n:>5}{fmt_int(di):>14}{fmt_int(do):>13}"
              f"{fmt_money(du):>11}{fmt_money(du*args.rub_rate):>13}")
    print(line)
    print("  РАЗБИВКА ПО ПЛАТФОРМАМ")
    print(f"    {'Платформа':<12}{'Сес':>5}{'Вход':>14}{'Выход':>13}{'USD':>11}{'RUB':>13}")
    for src, n, di, do in by_src:
        du = di / 1_000_000 * args.in_price + do / 1_000_000 * args.out_price
        print(f"    {src:<12}{n:>5}{fmt_int(di):>14}{fmt_int(do):>13}"
              f"{fmt_money(du):>11}{fmt_money(du*args.rub_rate):>13}")
    print(line)
    print("  ПРИМЕЧАНИЕ: Hermes пока НЕ тегирует сессии по проектам/клиентам,")
    print("  поэтому это ОБЩИЙ расход. Разбивка по проектам — см. README.")
    print(line)


if __name__ == "__main__":
    main()
