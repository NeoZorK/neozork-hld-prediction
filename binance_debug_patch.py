# Patch for adding debug information and slow progress updates to binance_fetcher.py

# Add this after line 73 (after metrics initialization):

    # --- DEBUG INFORMATION ---
    logger.print_debug(f"=== BINANCE FETCHER DEBUG INFO ===")
    logger.print_debug(f"Ticker: {ticker}")
    logger.print_debug(f"Interval: {interval}")
    logger.print_debug(f"Start Date: {start_date}")
    logger.print_debug(f"End Date: {end_date}")
    logger.print_debug(f"Binance Ticker: {binance_ticker}")
    logger.print_debug(f"Binance Interval: {binance_interval_str}")

# Add this after line 83 (after API key check):

    logger.print_debug(f"API Key Available: {bool(api_key)}")
    logger.print_debug(f"API Secret Available: {bool(api_secret)}")

# Add this after line 100 (after date conversion):

    logger.print_debug(f"Date range (ms): {start_ms} ({start_dt_obj}) to {end_ms} ({end_dt_obj})")
    logger.print_debug(f"Total duration: {total_duration_ms} ms")

# Add this after line 118 (after estimated data size calculation):

    logger.print_debug(f"Estimated rows: {estimated_rows}")
    logger.print_debug(f"Estimated chunks: {estimated_chunks}")
    logger.print_debug(f"Estimated data size: {estimated_data_size_kb:.1f}KB")

# Add this after line 128 (after progress bar initialization):

    logger.print_debug("Starting data fetching loop...")

# Add this after line 144 (after progress bar setup):

    # --- SLOW PROGRESS UPDATER ---
    import threading
    def slow_progress_updater():
        """Update progress slowly even before data is fetched"""
        nonlocal total_data_loaded_kb
        while chunks_processed == 0 and total_data_loaded_kb == 0:
            # Simulate slow progress during setup phase
            setup_progress = min(5.0, pbar.format_dict['elapsed'] * 0.5)  # Max 5KB during setup
            pbar.n = setup_progress
            pbar.set_postfix_str(f"Initializing... | {setup_progress:.1f}KB | Setup phase", refresh=True)
            pbar.refresh()
            time.sleep(0.5)
    
    # Start slow progress updater in background
    progress_thread = threading.Thread(target=slow_progress_updater, daemon=True)
    progress_thread.start()

# Add this after line 269 (after final data processing):

    logger.print_debug(f"=== BINANCE FETCHER COMPLETED ===")
    logger.print_debug(f"Final rows: {len(df)}")
    logger.print_debug(f"Final data size: {total_data_loaded_kb:.1f}KB")
    logger.print_debug(f"Chunks processed: {chunks_processed}")

# Add this in the finally block (after pbar.close()):

    # Stop the slow progress updater
    if 'progress_thread' in locals():
        progress_thread.join(timeout=1)
