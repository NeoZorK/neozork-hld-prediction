"""
Financial Analysis Color Utilities

This module provides color utilities for terminal output in financial analysis.
It follows the same patterns as existing color utilities in the project.
"""


class ColorUtils:
    """Color utilities for terminal output."""
    
    # ANSI color codes
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'
    
    @staticmethod
    def red(text: str) -> str:
        """Return red colored text."""
        return f"{ColorUtils.RED}{text}{ColorUtils.END}"
    
    @staticmethod
    def green(text: str) -> str:
        """Return green colored text."""
        return f"{ColorUtils.GREEN}{text}{ColorUtils.END}"
    
    @staticmethod
    def yellow(text: str) -> str:
        """Return yellow colored text."""
        return f"{ColorUtils.YELLOW}{text}{ColorUtils.END}"
    
    @staticmethod
    def blue(text: str) -> str:
        """Return blue colored text."""
        return f"{ColorUtils.BLUE}{text}{ColorUtils.END}"
    
    @staticmethod
    def magenta(text: str) -> str:
        """Return magenta colored text."""
        return f"{ColorUtils.MAGENTA}{text}{ColorUtils.END}"
    
    @staticmethod
    def cyan(text: str) -> str:
        """Return cyan colored text."""
        return f"{ColorUtils.CYAN}{text}{ColorUtils.END}"
    
    @staticmethod
    def white(text: str) -> str:
        """Return white colored text."""
        return f"{ColorUtils.WHITE}{text}{ColorUtils.END}"
    
    @staticmethod
    def bold(text: str) -> str:
        """Return bold text."""
        return f"{ColorUtils.BOLD}{text}{ColorUtils.END}"
    
    @staticmethod
    def underline(text: str) -> str:
        """Return underlined text."""
        return f"{ColorUtils.UNDERLINE}{text}{ColorUtils.END}"
    
    @staticmethod
    def success(text: str) -> str:
        """Return success colored text (green)."""
        return ColorUtils.green(f"✅ {text}")
    
    @staticmethod
    def error(text: str) -> str:
        """Return error colored text (red)."""
        return ColorUtils.red(f"❌ {text}")
    
    @staticmethod
    def warning(text: str) -> str:
        """Return warning colored text (yellow)."""
        return ColorUtils.yellow(f"⚠️  {text}")
    
    @staticmethod
    def info(text: str) -> str:
        """Return info colored text (blue)."""
        return ColorUtils.blue(f"ℹ️  {text}")
    
    @staticmethod
    def progress(text: str) -> str:
        """Return progress colored text (cyan)."""
        return ColorUtils.cyan(f"🔄 {text}")
    
    @staticmethod
    def analysis(text: str) -> str:
        """Return analysis colored text (magenta)."""
        return ColorUtils.magenta(f"📊 {text}")
    
    @staticmethod
    def financial(text: str) -> str:
        """Return financial colored text (bold green)."""
        return ColorUtils.bold(ColorUtils.green(f"💰 {text}"))
    
    @staticmethod
    def risk(text: str) -> str:
        """Return risk colored text (bold red)."""
        return ColorUtils.bold(ColorUtils.red(f"📉 {text}"))
    
    @staticmethod
    def volatility(text: str) -> str:
        """Return volatility colored text (bold yellow)."""
        return ColorUtils.bold(ColorUtils.yellow(f"📈 {text}"))
    
    @staticmethod
    def returns(text: str) -> str:
        """Return returns colored text (bold blue)."""
        return ColorUtils.bold(ColorUtils.blue(f"📊 {text}"))
    
    @staticmethod
    def drawdown(text: str) -> str:
        """Return drawdown colored text (bold magenta)."""
        return ColorUtils.bold(ColorUtils.magenta(f"📉 {text}"))
    
    @staticmethod
    def ohlcv(text: str) -> str:
        """Return OHLCV colored text (bold cyan)."""
        return ColorUtils.bold(ColorUtils.cyan(f"📊 {text}"))
    
    @staticmethod
    def header(text: str) -> str:
        """Return header colored text (bold white with underline)."""
        return ColorUtils.bold(ColorUtils.underline(ColorUtils.white(text)))
    
    @staticmethod
    def section(text: str) -> str:
        """Return section colored text (bold blue)."""
        return ColorUtils.bold(ColorUtils.blue(text))
    
    @staticmethod
    def metric(text: str) -> str:
        """Return metric colored text (cyan)."""
        return ColorUtils.cyan(text)
    
    @staticmethod
    def value(text: str) -> str:
        """Return value colored text (white)."""
        return ColorUtils.white(text)
    
    @staticmethod
    def percentage(text: str) -> str:
        """Return percentage colored text (green for positive, red for negative)."""
        try:
            # Try to parse as float to determine color
            value = float(text.replace('%', '').replace('+', ''))
            if value >= 0:
                return ColorUtils.green(f"+{text}")
            else:
                return ColorUtils.red(text)
        except:
            return ColorUtils.white(text)
    
    @staticmethod
    def positive(text: str) -> str:
        """Return positive colored text (green)."""
        return ColorUtils.green(f"+{text}")
    
    @staticmethod
    def negative(text: str) -> str:
        """Return negative colored text (red)."""
        return ColorUtils.red(f"-{text}")
    
    @staticmethod
    def neutral(text: str) -> str:
        """Return neutral colored text (white)."""
        return ColorUtils.white(text)
    
    @staticmethod
    def highlight(text: str) -> str:
        """Return highlighted text (bold yellow)."""
        return ColorUtils.bold(ColorUtils.yellow(text))
    
    @staticmethod
    def emphasis(text: str) -> str:
        """Return emphasized text (bold white)."""
        return ColorUtils.bold(ColorUtils.white(text))
    
    @staticmethod
    def dim(text: str) -> str:
        """Return dimmed text (default color)."""
        return text  # No color modification for dim effect
    
    @staticmethod
    def create_progress_bar(current: int, total: int, width: int = 30) -> str:
        """
        Create a visual progress bar.
        
        Args:
            current: Current progress
            total: Total progress
            width: Width of the progress bar
            
        Returns:
            Formatted progress bar string
        """
        if total == 0:
            percentage = 0
        else:
            percentage = (current / total) * 100
        
        filled_width = int((percentage / 100) * width)
        bar = '█' * filled_width + '░' * (width - filled_width)
        return f"[{bar}] {percentage:.1f}%"
    
    @staticmethod
    def create_status_indicator(status: str) -> str:
        """
        Create a status indicator with appropriate color.
        
        Args:
            status: Status string
            
        Returns:
            Colored status indicator
        """
        status_lower = status.lower()
        
        if status_lower in ['success', 'completed', 'done', 'ok', 'passed']:
            return ColorUtils.success(status)
        elif status_lower in ['error', 'failed', 'failed', 'error', 'critical']:
            return ColorUtils.error(status)
        elif status_lower in ['warning', 'warn', 'caution', 'attention']:
            return ColorUtils.warning(status)
        elif status_lower in ['info', 'information', 'note']:
            return ColorUtils.info(status)
        elif status_lower in ['progress', 'processing', 'running', 'active']:
            return ColorUtils.progress(status)
        else:
            return ColorUtils.neutral(status)
