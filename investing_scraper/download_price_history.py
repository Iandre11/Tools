import argparse
import time

import pandas as pd
import yfinance as yf

from symbol_catalog import PRICE_HISTORY_FILE, get_tracked_tickers


def batched(items, batch_size):
    for start in range(0, len(items), batch_size):
        yield items[start:start + batch_size]


def normalize_download(raw_df, tickers):
    if raw_df.empty:
        return pd.DataFrame()

    if raw_df.columns.nlevels == 1:
        raw_df = pd.concat({tickers[0]: raw_df}, axis=1)

    frames = []
    first_level = set(raw_df.columns.get_level_values(0))

    for ticker in tickers:
        if ticker not in first_level:
            continue

        ticker_df = raw_df[ticker].copy()
        if ticker_df.empty or "Close" not in ticker_df.columns:
            continue

        ticker_df = ticker_df.reset_index()
        date_column = ticker_df.columns[0]
        ticker_df.rename(columns={date_column: "Date"}, inplace=True)
        ticker_df["Date"] = pd.to_datetime(ticker_df["Date"], errors="coerce").dt.normalize()
        ticker_df["Ticker"] = ticker

        if "Adj Close" not in ticker_df.columns:
            ticker_df["Adj Close"] = ticker_df["Close"]
        if "Volume" not in ticker_df.columns:
            ticker_df["Volume"] = None

        ticker_df = ticker_df.dropna(subset=["Date", "Close"])
        frames.append(
            ticker_df[["Date", "Ticker", "Open", "High", "Low", "Close", "Adj Close", "Volume"]]
        )

    if not frames:
        return pd.DataFrame()

    return pd.concat(frames, ignore_index=True)


def download_batch(tickers, start_date, end_date, pause_seconds, max_retries):
    last_error = None

    for attempt in range(1, max_retries + 1):
        try:
            raw_df = yf.download(
                tickers=tickers,
                start=start_date,
                end=end_date,
                group_by="ticker",
                auto_adjust=False,
                threads=False,
                progress=False,
            )
            normalized_df = normalize_download(raw_df, tickers)
            if normalized_df.empty:
                raise RuntimeError("Yahoo devolvio un dataset vacio para este lote.")
            return normalized_df
        except Exception as exc:
            last_error = exc
            wait_seconds = pause_seconds * attempt
            print(f"Lote {tickers} fallo en intento {attempt}/{max_retries}: {exc}")
            if attempt < max_retries:
                print(f"Reintentando en {wait_seconds} segundos...")
                time.sleep(wait_seconds)

    raise RuntimeError(f"No se pudo descargar el lote {tickers}: {last_error}") from last_error


def main():
    parser = argparse.ArgumentParser(description="Descarga precios historicos de Yahoo Finance a un CSV local.")
    parser.add_argument("--start", default="2023-12-01", help="Fecha inicial inclusive en formato YYYY-MM-DD.")
    parser.add_argument("--end", default="2026-01-31", help="Fecha final exclusiva en formato YYYY-MM-DD.")
    parser.add_argument("--batch-size", type=int, default=8, help="Numero de tickers por lote.")
    parser.add_argument("--pause", type=int, default=2, help="Segundos base de espera entre reintentos.")
    parser.add_argument("--retries", type=int, default=4, help="Numero maximo de intentos por lote.")
    args = parser.parse_args()

    tracked_tickers = get_tracked_tickers()
    all_frames = []
    missing_tickers = []

    print(f"Descargando {len(tracked_tickers)} tickers hacia {PRICE_HISTORY_FILE}...")
    for index, ticker_batch in enumerate(batched(tracked_tickers, args.batch_size), start=1):
        print(f"Lote {index}: {', '.join(ticker_batch)}")
        batch_df = download_batch(
            ticker_batch,
            start_date=args.start,
            end_date=args.end,
            pause_seconds=args.pause,
            max_retries=args.retries,
        )
        all_frames.append(batch_df)
        downloaded_batch_tickers = set(batch_df["Ticker"].unique())
        missing_tickers.extend([ticker for ticker in ticker_batch if ticker not in downloaded_batch_tickers])
        time.sleep(args.pause)

    rescued_frames = []
    still_missing = []
    for ticker in missing_tickers:
        print(f"Reintento individual: {ticker}")
        try:
            single_df = download_batch(
                [ticker],
                start_date=args.start,
                end_date=args.end,
                pause_seconds=args.pause,
                max_retries=args.retries,
            )
            rescued_frames.append(single_df)
            time.sleep(args.pause)
        except Exception as exc:
            still_missing.append(ticker)
            print(f"No se pudo descargar {ticker}: {exc}")

    all_frames.extend(rescued_frames)

    if not all_frames:
        raise RuntimeError("No se descargaron datos.")

    output_df = pd.concat(all_frames, ignore_index=True)
    output_df.sort_values(["Ticker", "Date"], inplace=True)
    output_df.drop_duplicates(subset=["Ticker", "Date"], keep="last", inplace=True)
    output_df.to_csv(PRICE_HISTORY_FILE, index=False)

    min_date = output_df["Date"].min()
    max_date = output_df["Date"].max()
    print(
        f"Guardado {PRICE_HISTORY_FILE.name} con {len(output_df)} filas, "
        f"{output_df['Ticker'].nunique()} tickers, rango {min_date} -> {max_date}."
    )
    if still_missing:
        print(f"Tickers sin datos tras reintentos: {', '.join(still_missing)}")


if __name__ == "__main__":
    main()
