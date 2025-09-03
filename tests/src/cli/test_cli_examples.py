def test_import():
    """Test that all CLI examples modules can be imported."""
    # Test importing the main examples module
    import src.cli.examples.main_examples
    
    # Test importing specific indicator group examples
    import src.cli.examples.oscillators.oscillator_examples
    import src.cli.examples.trend.trend_examples
    import src.cli.examples.momentum.momentum_examples
    
    # Test importing the main examples package
    from src.cli.examples import show_all_cli_examples, show_indicator_group_examples
    
    # Test importing specific example classes
    from src.cli.examples.oscillators import OscillatorExamples
    from src.cli.examples.trend import TrendExamples
    from src.cli.examples.momentum import MomentumExamples 