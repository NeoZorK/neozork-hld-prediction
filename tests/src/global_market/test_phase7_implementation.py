#!/usr/bin/env python3
"""
Test Phase 7 Implementation
Multi-Market Integration, Global Regulatory Compliance, Advanced Risk Management
"""

import asyncio
import sys
import os
from datetime import datetime, timedelta

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', '..', 'src'))

from global_market.multi_market_integration import MultiMarketManager, BinanceConnector, CoinbaseConnector, KrakenConnector
from global_market.regulatory_compliance import RegulatoryComplianceManager, Jurisdiction
from global_market.advanced_risk_management import AdvancedRiskManager

async def test_multi_market_integration():
    """Test Multi-Market Integration System"""
    print("🔍 Testing Multi-Market Integration System...")
    
    try:
        manager = MultiMarketManager()
        
        # Add exchanges
        async with BinanceConnector() as binance:
            async with CoinbaseConnector() as coinbase:
                async with KrakenConnector() as kraken:
                    await manager.add_exchange(binance)
                    await manager.add_exchange(coinbase)
                    await manager.add_exchange(kraken)
                    
                    # Test market data retrieval
                    print("  📊 Testing market data retrieval...")
                    btc_data = await manager.get_market_data("BTCUSDT")
                    print(f"    ✅ Retrieved data from {len(btc_data)} exchanges")
                    
                    # Test arbitrage detection
                    print("  🔍 Testing arbitrage opportunity detection...")
                    opportunities = await manager.detect_arbitrage_opportunities("BTCUSDT", min_spread_percent=0.1)
                    print(f"    ✅ Found {len(opportunities)} arbitrage opportunities")
                    
                    # Test cross-market analysis
                    print("  📈 Testing cross-market analysis...")
                    analysis = await manager.get_cross_market_analysis(["BTCUSDT", "ETHUSDT"])
                    print(f"    ✅ Cross-market analysis completed for {len(analysis['symbols'])} symbols")
                    
                    # Test portfolio exposure
                    print("  💼 Testing portfolio exposure analysis...")
                    portfolio = {"BTCUSDT": 0.1, "ETHUSDT": 1.0}
                    exposure = await manager.get_portfolio_exposure(portfolio)
                    print(f"    ✅ Portfolio exposure analysis completed (Total value: ${exposure['total_value']:,.2f})")
                    
                    # Get system summary
                    summary = manager.get_summary()
                    print(f"    ✅ System summary: {summary['total_exchanges']} exchanges, {summary['total_arbitrage_opportunities']} opportunities")
        
        print("  ✅ Multi-Market Integration System test passed")
        return True
        
    except Exception as e:
        print(f"  ❌ Multi-Market Integration System test failed: {e}")
        return False

async def test_regulatory_compliance():
    """Test Global Regulatory Compliance System"""
    print("🔍 Testing Global Regulatory Compliance System...")
    
    try:
        manager = RegulatoryComplianceManager()
        
        # Initialize jurisdictions
        print("  🌍 Testing jurisdiction initialization...")
        await manager.initialize_jurisdictions()
        print(f"    ✅ Initialized {len(manager.compliance_rules)} jurisdictions")
        
        # Test user onboarding
        print("  👤 Testing user onboarding...")
        user_data = {
            "email": "test@example.com",
            "first_name": "John",
            "last_name": "Doe",
            "date_of_birth": "1990-01-01",
            "nationality": "US",
            "address": {"country": "US", "state": "CA", "city": "San Francisco"},
            "phone": "+1234567890"
        }
        
        onboard_result = await manager.onboard_user(user_data, Jurisdiction.US)
        print(f"    ✅ User onboarded: {onboard_result['user_id']} (Risk level: {onboard_result['risk_level']})")
        
        # Test transaction processing
        print("  💳 Testing transaction processing...")
        transaction_data = {
            "user_id": onboard_result["user_id"],
            "amount": 5000.0,
            "currency": "USD",
            "transaction_type": "trade",
            "source_exchange": "binance",
            "destination_exchange": "coinbase"
        }
        
        transaction_result = await manager.process_transaction(transaction_data)
        print(f"    ✅ Transaction processed: {transaction_result['transaction_id']} (Risk score: {transaction_result['risk_score']:.3f})")
        
        # Test compliance report generation
        print("  📋 Testing compliance report generation...")
        end_date = datetime.now()
        start_date = end_date - timedelta(days=30)
        
        report = await manager.generate_compliance_report(Jurisdiction.US, start_date, end_date)
        print(f"    ✅ Compliance report generated: {report['user_statistics']['total_users']} users, {report['aml_report']['total_transactions']} transactions")
        
        # Test KYC status update
        print("  ✅ Testing KYC status update...")
        kyc_update = await manager.kyc_manager.update_kyc_status(onboard_result["user_id"], "completed")
        print(f"    ✅ KYC status updated: {kyc_update}")
        
        # Test document verification
        print("  📄 Testing document verification...")
        doc_result = await manager.kyc_manager.verify_document(onboard_result["user_id"], "passport", b"fake_document_data")
        print(f"    ✅ Document verified: {doc_result['verification_status']} (Confidence: {doc_result['confidence_score']:.2f})")
        
        # Get system summary
        summary = manager.get_summary()
        print(f"    ✅ System summary: {summary['total_users']} users, {summary['total_transactions']} transactions")
        
        print("  ✅ Global Regulatory Compliance System test passed")
        return True
        
    except Exception as e:
        print(f"  ❌ Global Regulatory Compliance System test failed: {e}")
        return False

async def test_advanced_risk_management():
    """Test Advanced Risk Management System"""
    print("🔍 Testing Advanced Risk Management System...")
    
    try:
        manager = AdvancedRiskManager()
        
        # Initialize risk system
        print("  ⚙️ Testing risk system initialization...")
        await manager.initialize_risk_system()
        print(f"    ✅ Risk system initialized with {len(manager.stress_test_manager.scenarios)} stress test scenarios")
        
        # Add positions
        print("  📊 Testing position management...")
        btc_position = await manager.add_position("BTC", 0.5, 45000.0)
        eth_position = await manager.add_position("ETH", 2.0, 3000.0)
        bnb_position = await manager.add_position("BNB", 10.0, 300.0)
        print(f"    ✅ Added 3 positions: BTC, ETH, BNB")
        
        # Update prices
        print("  💰 Testing price updates...")
        price_updates = {
            "BTC": 46000.0,
            "ETH": 3100.0,
            "BNB": 320.0
        }
        await manager.update_portfolio_prices(price_updates)
        print(f"    ✅ Updated prices for {len(price_updates)} assets")
        
        # Run comprehensive risk analysis
        print("  📈 Testing comprehensive risk analysis...")
        risk_analysis = await manager.run_comprehensive_risk_analysis()
        
        portfolio_summary = risk_analysis['portfolio_summary']
        risk_metrics = risk_analysis['risk_metrics']
        
        print(f"    ✅ Risk analysis completed:")
        print(f"      - Total Portfolio Value: ${portfolio_summary['total_value']:,.2f}")
        print(f"      - Total P&L: ${portfolio_summary['total_pnl']:,.2f}")
        print(f"      - VaR 95%: {risk_metrics['var_95']:.4f}")
        print(f"      - Max Drawdown: {risk_metrics['max_drawdown']:.4f}")
        print(f"      - Sharpe Ratio: {risk_metrics['sharpe_ratio']:.2f}")
        print(f"      - Concentration Risk: {risk_metrics['concentration_risk']:.4f}")
        
        # Test risk limit checking
        print("  🚨 Testing risk limit checking...")
        limit_check = risk_analysis['limit_check']
        breaches = limit_check['breaches']
        warnings = limit_check['warnings']
        
        print(f"    ✅ Risk limit check completed:")
        print(f"      - Breaches: {len(breaches)}")
        print(f"      - Warnings: {len(warnings)}")
        
        if breaches:
            for breach in breaches:
                print(f"        - {breach['metric']}: {breach['current_value']:.4f} (limit: {breach['limit']:.4f})")
        
        # Test stress testing
        print("  🌪️ Testing stress testing...")
        stress_results = risk_analysis['stress_test_results']['summary']
        
        print(f"    ✅ Stress test completed:")
        print(f"      - Total Scenarios: {stress_results['total_scenarios']}")
        print(f"      - Worst Case P&L: ${stress_results['worst_case_pnl']:,.2f}")
        print(f"      - Best Case P&L: ${stress_results['best_case_pnl']:,.2f}")
        print(f"      - Average P&L Impact: ${stress_results['average_pnl_impact']:,.2f}")
        print(f"      - Max Stressed VaR: {stress_results['max_stressed_var']:.4f}")
        
        # Test individual stress test scenario
        print("  🎯 Testing individual stress test scenario...")
        market_crash_result = await manager.stress_test_manager.run_stress_test("market_crash", manager.portfolio_manager)
        print(f"    ✅ Market crash scenario: P&L impact ${market_crash_result['total_pnl_impact']:,.2f}")
        
        # Test risk report generation
        print("  📊 Testing risk report generation...")
        risk_report = await manager.generate_risk_report("comprehensive")
        print(f"    ✅ Risk report generated with {len(risk_report)} sections")
        
        # Get system summary
        summary = manager.get_summary()
        print(f"    ✅ System summary: {summary['total_positions']} positions, {summary['total_scenarios']} scenarios")
        
        print("  ✅ Advanced Risk Management System test passed")
        return True
        
    except Exception as e:
        print(f"  ❌ Advanced Risk Management System test failed: {e}")
        return False

async def test_integration():
    """Test integration between all Phase 7 components"""
    print("🔍 Testing Phase 7 Integration...")
    
    try:
        # Initialize all managers
        multi_market_manager = MultiMarketManager()
        compliance_manager = RegulatoryComplianceManager()
        risk_manager = AdvancedRiskManager()
        
        # Initialize systems
        await compliance_manager.initialize_jurisdictions()
        await risk_manager.initialize_risk_system()
        
        # Add exchanges to multi-market manager
        async with BinanceConnector() as binance:
            async with CoinbaseConnector() as coinbase:
                await multi_market_manager.add_exchange(binance)
                await multi_market_manager.add_exchange(coinbase)
                
                # Test integrated workflow
                print("  🔄 Testing integrated workflow...")
                
                # 1. User onboarding
                user_data = {
                    "email": "trader@example.com",
                    "first_name": "Jane",
                    "last_name": "Smith",
                    "date_of_birth": "1985-05-15",
                    "nationality": "US",
                    "address": {"country": "US", "state": "NY", "city": "New York"},
                    "phone": "+1987654321"
                }
                
                onboard_result = await compliance_manager.onboard_user(user_data, Jurisdiction.US)
                print(f"    ✅ User onboarded: {onboard_result['user_id']}")
                
                # 2. Add positions to risk manager
                btc_position = await risk_manager.add_position("BTC", 1.0, 45000.0)
                eth_position = await risk_manager.add_position("ETH", 5.0, 3000.0)
                print(f"    ✅ Positions added to risk manager")
                
                # 3. Get market data from multi-market manager
                market_data = await multi_market_manager.get_market_data("BTCUSDT")
                print(f"    ✅ Market data retrieved from {len(market_data)} exchanges")
                
                # 4. Update risk manager with market data
                price_updates = {}
                for exchange, data in market_data.items():
                    if data:
                        price_updates[data.symbol] = data.price
                
                if price_updates:
                    await risk_manager.update_portfolio_prices(price_updates)
                    print(f"    ✅ Portfolio prices updated with market data")
                
                # 5. Run risk analysis
                risk_analysis = await risk_manager.run_comprehensive_risk_analysis()
                print(f"    ✅ Risk analysis completed")
                
                # 6. Process transaction through compliance
                transaction_data = {
                    "user_id": onboard_result["user_id"],
                    "amount": 10000.0,
                    "currency": "USD",
                    "transaction_type": "trade",
                    "source_exchange": "binance",
                    "destination_exchange": "coinbase"
                }
                
                transaction_result = await compliance_manager.process_transaction(transaction_data)
                print(f"    ✅ Transaction processed with risk score: {transaction_result['risk_score']:.3f}")
                
                # 7. Generate comprehensive reports
                compliance_report = await compliance_manager.generate_compliance_report(Jurisdiction.US, datetime.now() - timedelta(days=30), datetime.now())
                risk_report = await risk_manager.generate_risk_report("comprehensive")
                
                print(f"    ✅ Reports generated:")
                print(f"      - Compliance: {compliance_report['user_statistics']['total_users']} users")
                print(f"      - Risk: {len(risk_report)} sections")
                
                # 8. Get system summaries
                multi_market_summary = multi_market_manager.get_summary()
                compliance_summary = compliance_manager.get_summary()
                risk_summary = risk_manager.get_summary()
                
                print(f"    ✅ System summaries:")
                print(f"      - Multi-Market: {multi_market_summary['total_exchanges']} exchanges")
                print(f"      - Compliance: {compliance_summary['total_users']} users")
                print(f"      - Risk: {risk_summary['total_positions']} positions")
        
        print("  ✅ Phase 7 Integration test passed")
        return True
        
    except Exception as e:
        print(f"  ❌ Phase 7 Integration test failed: {e}")
        return False

async def main():
    """Main test function"""
    print("🚀 Starting Phase 7 Implementation Tests")
    print("=" * 60)
    
    test_results = []
    
    # Test individual components
    test_results.append(await test_multi_market_integration())
    test_results.append(await test_regulatory_compliance())
    test_results.append(await test_advanced_risk_management())
    
    # Test integration
    test_results.append(await test_integration())
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 Phase 7 Implementation Test Results:")
    
    passed_tests = sum(test_results)
    total_tests = len(test_results)
    
    print(f"✅ Passed: {passed_tests}/{total_tests}")
    print(f"❌ Failed: {total_tests - passed_tests}/{total_tests}")
    
    if passed_tests == total_tests:
        print("\n🎉 All Phase 7 tests passed! System is ready for production.")
        return True
    else:
        print(f"\n⚠️ {total_tests - passed_tests} tests failed. Please review and fix issues.")
        return False

if __name__ == "__main__":
    success = asyncio.run(main())
    sys.exit(0 if success else 1)
