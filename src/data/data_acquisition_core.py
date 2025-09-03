# -*- coding: utf-8 -*-
# src/data/data_acquisition_core.py

"""
Core data acquisition functionality with args-based interface.
Handles the main data acquisition process with argument parsing.
All comments are in English.
"""

import time
import pandas as pd
from pathlib import Path
from typing import Dict, Any, Optional

from src.common import logger
from src.data.fetchers.demo_fetcher import get_demo_data
from src.data.fetchers.yfinance_fetcher import fetch_yfinance_data
from src.data.fetchers.csv_fetcher import fetch_csv_data
from src.data.fetchers.polygon_fetcher import fetch_polygon_data
from src.data.fetchers.binance_fetcher import fetch_binance_data
from src.data.fetchers.exrate_fetcher import fetch_exrate_data


def acquire_data(args) -> Dict[str, Any]:
    """
    Main data acquisition function that accepts parsed command-line arguments.
    
    Args:
        args: Parsed command-line arguments containing mode, ticker, etc.
        
    Returns:
        Dict containing ohlcv_df and metadata about the acquisition
    """
    logger.print_info(f"Starting data acquisition in mode: {args.mode}")
    
    # Initialize result dictionary
    data_info = {
        "ohlcv_df": None,
        "data_source_label": "Unknown",
        "effective_mode": args.mode,
        "rows_count": 0,
        "columns_count": 0,
        "data_size_mb": 0.0,
        "data_size_bytes": 0,
        "file_size_bytes": None,
        "parquet_cache_used": False,
        "parquet_cache_file": None,
        "error_message": None
    }
    
    try:
        # Handle different modes
        if args.mode == 'demo':
            logger.print_info("Generating demo data...")
            ohlcv_df = get_demo_data()
            data_info["data_source_label"] = "Demo Data"
            data_info["effective_mode"] = "demo"
            
        elif args.mode in ['yfinance', 'yf']:
            logger.print_info(f"Fetching YFinance data for {args.ticker}")
            ohlcv_df = fetch_yfinance_data(
                ticker=args.ticker,
                interval=args.interval,
                period=args.period,
                start=args.start,
                end=args.end
            )
            data_info["data_source_label"] = f"YFinance ({args.ticker})"
            data_info["effective_mode"] = "yfinance"
            
        elif args.mode == 'csv':
            if args.csv_file:
                logger.print_info(f"Loading CSV file: {args.csv_file}")
                ohlcv_df = fetch_csv_data(csv_file=args.csv_file)
                data_info["data_source_label"] = f"CSV ({args.csv_file})"
            elif args.csv_folder:
                logger.print_info(f"Processing CSV folder: {args.csv_folder}")
                # Handle CSV folder processing
                from src.data.processing import CSVFolderProcessor
                processor = CSVFolderProcessor()
                folder_results = processor.process_folder(
                    folder_path=args.csv_folder,
                    args=args
                )
                data_info["folder_processing_results"] = folder_results
                return data_info
            else:
                raise ValueError("CSV mode requires either --csv-file or --csv-folder")
            data_info["effective_mode"] = "csv"
            
        elif args.mode == 'polygon':
            logger.print_info(f"Fetching Polygon data for {args.ticker}")
            ohlcv_df = fetch_polygon_data(
                ticker=args.ticker,
                interval=args.interval,
                start=args.start,
                end=args.end
            )
            data_info["data_source_label"] = f"Polygon ({args.ticker})"
            data_info["effective_mode"] = "polygon"
            
        elif args.mode == 'binance':
            logger.print_info(f"Fetching Binance data for {args.ticker}")
            ohlcv_df = fetch_binance_data(
                symbol=args.ticker,
                interval=args.interval,
                start=args.start,
                end=args.end
            )
            data_info["data_source_label"] = f"Binance ({args.ticker})"
            data_info["effective_mode"] = "binance"
            
        elif args.mode == 'exrate':
            logger.print_info(f"Fetching Exchange Rate data for {args.ticker}")
            ohlcv_df = fetch_exrate_data(
                base_currency=args.ticker.split('/')[0] if '/' in args.ticker else 'USD',
                target_currency=args.ticker.split('/')[1] if '/' in args.ticker else args.ticker,
                start_date=args.start,
                end_date=args.end
            )
            data_info["data_source_label"] = f"ExchangeRate ({args.ticker})"
            data_info["effective_mode"] = "exrate"
            
        else:
            raise ValueError(f"Unsupported mode: {args.mode}")
        
        # Validate and process the acquired data
        if ohlcv_df is not None and not ohlcv_df.empty:
            # Calculate data metrics
            data_info["ohlcv_df"] = ohlcv_df
            data_info["rows_count"] = len(ohlcv_df)
            data_info["columns_count"] = len(ohlcv_df.columns)
            data_info["data_size_bytes"] = ohlcv_df.memory_usage(deep=True).sum()
            data_info["data_size_mb"] = data_info["data_size_bytes"] / (1024 * 1024)
            
            logger.print_success(f"Data acquisition successful: {data_info['rows_count']} rows, {data_info['data_size_mb']:.3f} MB")
        else:
            data_info["error_message"] = f"No data acquired for mode {args.mode}"
            logger.print_error(data_info["error_message"])
            
    except Exception as e:
        data_info["error_message"] = str(e)
        logger.print_error(f"Data acquisition failed: {e}")
    
    return data_info
