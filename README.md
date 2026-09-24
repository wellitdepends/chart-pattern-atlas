# Chart Pattern Atlas

A single-page gallery of candlestick and chart (trend) patterns, drawn with [TradingView Lightweight Charts](https://github.com/tradingview/lightweight-charts).

- **Candlestick Patterns**: 78 one- to five-candle patterns with OHLC data, signal (bullish / indecision / bearish) and plain-English descriptions, including alternative names.
- **Trend Patterns**: 42 classic chart patterns (reversal, continuation, bilateral) with textbook OHLC data, dashed guide lines, and a real-market example for each one.

## Using it

Open `index.html` in a browser. It is self-contained apart from Google Fonts and the Lightweight Charts script (loaded from jsDelivr, with unpkg as a fallback).

Controls: mouse wheel anywhere moves the carousel, the arrow buttons (or ← →) step and glide when held, `R` toggles textbook / real-world charts on the Trend Patterns page. Search is loose: it matches names, descriptions and alternative names, and tolerates small typos.

## Data

- `data/candlestick-patterns.csv`: `pattern, candles, description`. Candles are `open,high,low,close` groups separated by ` | `.
- `data/trend-patterns.csv`: `pattern, signal, type, candles, guides, description` plus `example_*` columns for the real-world example (symbol, bar interval, dates, candles, guides, shape-match score). Guides are polylines of `index:price` points separated by `;`, lines separated by ` | `.

The data is embedded in `index.html`; the CSVs are the source copies.

## Scripts

`scripts/` holds the Python used to build the trend data:

1. `generate_trend_patterns.py`: builds the textbook OHLC series from each pattern's turning points.
2. `scan_matches.py`, `select_examples.py`, `fit_guides.py`, `write_examples.py`: scan ten years of daily prices for 25 markets (stocks, ETFs, FX, crypto; fetched from TradingView) for the window whose shape best matches each pattern, fit guide lines to that window's turning points, and write the `example_*` columns. The raw price data is not included.

Real-world examples were found by a shape-matching scan, not hand-picked by an analyst. They are illustrations, not trading signals.
