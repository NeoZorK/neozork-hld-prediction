#!/usr/bin/env python3
"""
Test Phase 7 Completion
All Phase 7 tasks: Multi-Market Integration, Global Regulatory Compliance, 
Advanced Risk Management, Scalable Infrastructure, International Partnerships
"""

import asyncio
import sys
import os
import pytest
from datetime import datetime, timedelta

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', '..', 'src'))

from global_market.multi_market_integration import MultiMarketManager, BinanceConnector, CoinbaseConnector, KrakenConnector
from global_market.regulatory_compliance import RegulatoryComplianceManager, Jurisdiction
from global_market.advanced_risk_management import AdvancedRiskManager
from global_market.scalable_infrastructure import DistributedSystemManager, ServiceDefinition, ScalingPolicy
from global_market.international_partnerships import InternationalPartnershipsManager

@pytest.mark.asyncio
async def test_scalable_infrastructure():
    """Test Scalable Infrastructure System"""
    print("🔍 Testing Scalable Infrastructure System...")
    
    try:
        manager = DistributedSystemManager()
        
        # Initialize system
        print("  ⚙️ Testing system initialization...")
        await manager.initialize_system()
        print(f"    ✅ System initialized successfully")
        
        # Deploy services
        print("  🚀 Testing service deployment...")
        trading_service = ServiceDefinition(
            service_name="trading-service",
            version="1.0.0",
            replicas=3,
            min_replicas=2,
            max_replicas=10,
            cpu_limit=1.0,
            memory_limit=512,
            scaling_policy=ScalingPolicy.CPU_BASED,
            health_check_endpoint="/health",
            dependencies=[],
            environment_variables={"ENV": "production"},
            created_at=datetime.now()
        )
        
        data_service = ServiceDefinition(
            service_name="data-service",
            version="1.0.0",
            replicas=2,
            min_replicas=1,
            max_replicas=5,
            cpu_limit=0.5,
            memory_limit=256,
            scaling_policy=ScalingPolicy.MEMORY_BASED,
            health_check_endpoint="/health",
            dependencies=[],
            environment_variables={"ENV": "production"},
            created_at=datetime.now()
        )
        
        await manager.deploy_service(trading_service)
        await manager.deploy_service(data_service)
        print(f"    ✅ Deployed 2 services successfully")
        
        # Test request routing
        print("  🔄 Testing request routing...")
        for i in range(5):
            request_data = {"request_id": f"req-{i}", "data": f"test-data-{i}"}
            response = await manager.route_request("trading-service", request_data, f"192.168.1.{i}")
            print(f"    ✅ Request {i}: {response['status']} - Instance: {response.get('instance_id', 'N/A')}")
        
        # Test system status
        print("  📊 Testing system status...")
        status = await manager.get_system_status()
        print(f"    ✅ System Status: {status['total_services']} services, {status['total_instances']} instances")
        
        # Test service metrics
        print("  📈 Testing service metrics...")
        metrics = await manager.get_service_metrics("trading-service")
        print(f"    ✅ Trading Service Metrics: {len(metrics['instances'])} instances")
        
        # Test auto-scaling
        print("  📏 Testing auto-scaling...")
        scaling_policies = len(manager.auto_scaler.scaling_policies)
        print(f"    ✅ Auto-scaling policies: {scaling_policies}")
        
        # Get system summary
        summary = manager.get_summary()
        print(f"    ✅ System summary: {summary['total_services']} services, {summary['total_instances']} instances")
        
        print("  ✅ Scalable Infrastructure System test passed")
        return True
        
    except Exception as e:
        print(f"  ❌ Scalable Infrastructure System test failed: {e}")
        return False

@pytest.mark.asyncio
async def test_international_partnerships():
    """Test International Partnerships System"""
    print("🔍 Testing International Partnerships System...")
    
    try:
        manager = InternationalPartnershipsManager()
        
        # Initialize partnerships
        print("  🌍 Testing partnership initialization...")
        await manager.initialize_partnerships()
        print(f"    ✅ Partnerships initialized successfully")
        
        # Test partnership dashboard
        print("  📊 Testing partnership dashboard...")
        dashboard = await manager.get_partnership_dashboard()
        print(f"    ✅ Dashboard: {dashboard['partnerships']['total']} partnerships, {dashboard['data_providers']['total']} data providers")
        
        # Test data provider functionality
        print("  📈 Testing data provider functionality...")
        market_data = await manager.data_provider_manager.fetch_market_data("market_data_provider", ["BTC", "ETH"])
        print(f"    ✅ Market data fetched: {market_data['status']}")
        
        news_data = await manager.data_provider_manager.fetch_news_data("news_data_provider", ["BTC"], 5)
        print(f"    ✅ News data fetched: {news_data['status']} ({news_data['total_count']} articles)")
        
        # Test liquidity provider functionality
        print("  💰 Testing liquidity provider functionality...")
        quote = await manager.liquidity_provider_manager.get_liquidity_quote("liquidity_provider_1", "BTC", 0.1)
        print(f"    ✅ Liquidity quote: {quote['status']}")
        
        order_data = {"symbol": "BTC", "quantity": 0.1, "order_type": "market"}
        order_result = await manager.liquidity_provider_manager.place_order("liquidity_provider_1", order_data)
        print(f"    ✅ Order placed: {order_result['status']}")
        
        # Test trading workflow
        print("  🔄 Testing trading workflow...")
        workflow = await manager.execute_trading_workflow("BTC", 0.1)
        print(f"    ✅ Trading workflow completed:")
        print(f"      - Market Data: {workflow['steps']['market_data']['status']}")
        print(f"      - News Data: {workflow['steps']['news_data']['status']}")
        print(f"      - Liquidity Quote: {workflow['steps']['liquidity_quote']['status']}")
        print(f"      - Order Execution: {workflow['steps']['order_execution']['status']}")
        
        # Test provider performance
        print("  📊 Testing provider performance...")
        performance = await manager.liquidity_provider_manager.get_provider_performance("liquidity_provider_1")
        print(f"    ✅ Provider performance: Success rate {performance['success_rate']:.2%}")
        
        # Test data quality report
        print("  🔍 Testing data quality report...")
        quality_report = await manager.data_provider_manager.get_data_quality_report("market_data_provider")
        print(f"    ✅ Data quality report: Overall score {quality_report['overall_score']:.2f}")
        
        # Get system summary
        summary = manager.get_summary()
        print(f"    ✅ System summary: {summary['total_partnerships']} partnerships, {summary['total_api_requests']} API requests")
        
        print("  ✅ International Partnerships System test passed")
        return True
        
    except Exception as e:
        print(f"  ❌ International Partnerships System test failed: {e}")
        return False

@pytest.mark.asyncio
async def test_phase7_integration():
    """Test integration between all Phase 7 components"""
    print("🔍 Testing Phase 7 Full Integration...")
    
    try:
        # Initialize all managers
        multi_market_manager = MultiMarketManager()
        compliance_manager = RegulatoryComplianceManager()
        risk_manager = AdvancedRiskManager()
        infrastructure_manager = DistributedSystemManager()
        partnerships_manager = InternationalPartnershipsManager()
        
        # Initialize all systems
        await compliance_manager.initialize_jurisdictions()
        await risk_manager.initialize_risk_system()
        await infrastructure_manager.initialize_system()
        await partnerships_manager.initialize_partnerships()
        
        print("  🔄 Testing integrated global trading workflow...")
        
        # 1. User onboarding with compliance
        user_data = {
            "email": "global_trader@example.com",
            "first_name": "Global",
            "last_name": "Trader",
            "date_of_birth": "1980-01-01",
            "nationality": "US",
            "address": {"country": "US", "state": "CA", "city": "San Francisco"},
            "phone": "+1234567890"
        }
        
        onboard_result = await compliance_manager.onboard_user(user_data, Jurisdiction.US)
        print(f"    ✅ User onboarded: {onboard_result['user_id']}")
        
        # 2. Deploy trading services
        trading_service = ServiceDefinition(
            service_name="global-trading-service",
            version="1.0.0",
            replicas=3,
            min_replicas=2,
            max_replicas=10,
            cpu_limit=1.0,
            memory_limit=512,
            scaling_policy=ScalingPolicy.CPU_BASED,
            health_check_endpoint="/health",
            dependencies=[],
            environment_variables={"ENV": "production"},
            created_at=datetime.now()
        )
        
        await infrastructure_manager.deploy_service(trading_service)
        print(f"    ✅ Trading service deployed")
        
        # 3. Add positions to risk manager
        btc_position = await risk_manager.add_position("BTC", 1.0, 45000.0)
        eth_position = await risk_manager.add_position("ETH", 5.0, 3000.0)
        print(f"    ✅ Positions added to risk manager")
        
        # 4. Execute trading workflow through partnerships
        workflow = await partnerships_manager.execute_trading_workflow("BTC", 0.1)
        print(f"    ✅ Trading workflow executed through partnerships")
        
        # 5. Process transaction through compliance
        transaction_data = {
            "user_id": onboard_result["user_id"],
            "amount": 5000.0,
            "currency": "USD",
            "transaction_type": "trade",
            "source_exchange": "binance",
            "destination_exchange": "coinbase"
        }
        
        transaction_result = await compliance_manager.process_transaction(transaction_data)
        print(f"    ✅ Transaction processed with compliance: Risk score {transaction_result['risk_score']:.3f}")
        
        # 6. Update risk manager with market data
        price_updates = {"BTC": 46000.0, "ETH": 3100.0}
        await risk_manager.update_portfolio_prices(price_updates)
        print(f"    ✅ Portfolio prices updated")
        
        # 7. Run comprehensive risk analysis
        risk_analysis = await risk_manager.run_comprehensive_risk_analysis()
        print(f"    ✅ Risk analysis completed")
        
        # 8. Route requests through infrastructure
        for i in range(3):
            request_data = {"request_id": f"global-req-{i}", "data": f"global-data-{i}"}
            response = await infrastructure_manager.route_request("global-trading-service", request_data)
            print(f"    ✅ Request {i} routed: {response['status']}")
        
        # 9. Generate comprehensive reports
        compliance_report = await compliance_manager.generate_compliance_report(Jurisdiction.US, datetime.now() - timedelta(days=30), datetime.now())
        risk_report = await risk_manager.generate_risk_report("comprehensive")
        infrastructure_status = await infrastructure_manager.get_system_status()
        partnerships_dashboard = await partnerships_manager.get_partnership_dashboard()
        
        print(f"    ✅ Reports generated:")
        print(f"      - Compliance: {compliance_report['user_statistics']['total_users']} users")
        print(f"      - Risk: {len(risk_report)} sections")
        print(f"      - Infrastructure: {infrastructure_status['total_services']} services")
        print(f"      - Partnerships: {partnerships_dashboard['partnerships']['total']} partnerships")
        
        # 10. Get system summaries
        multi_market_summary = multi_market_manager.get_summary()
        compliance_summary = compliance_manager.get_summary()
        risk_summary = risk_manager.get_summary()
        infrastructure_summary = infrastructure_manager.get_summary()
        partnerships_summary = partnerships_manager.get_summary()
        
        print(f"    ✅ System summaries:")
        print(f"      - Multi-Market: {multi_market_summary['total_exchanges']} exchanges")
        print(f"      - Compliance: {compliance_summary['total_users']} users")
        print(f"      - Risk: {risk_summary['total_positions']} positions")
        print(f"      - Infrastructure: {infrastructure_summary['total_services']} services")
        print(f"      - Partnerships: {partnerships_summary['total_partnerships']} partnerships")
        
        print("  ✅ Phase 7 Full Integration test passed")
        return True
        
    except Exception as e:
        print(f"  ❌ Phase 7 Full Integration test failed: {e}")
        return False

async def main():
    """Main test function"""
    print("🚀 Starting Phase 7 Completion Tests")
    print("=" * 60)
    
    test_results = []
    
    # Test individual components (first 3 already tested)
    print("📋 Testing remaining Phase 7 components...")
    test_results.append(await test_scalable_infrastructure())
    test_results.append(await test_international_partnerships())
    
    # Test full integration
    test_results.append(await test_phase7_integration())
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 Phase 7 Completion Test Results:")
    
    passed_tests = sum(test_results)
    total_tests = len(test_results)
    
    print(f"✅ Passed: {passed_tests}/{total_tests}")
    print(f"❌ Failed: {total_tests - passed_tests}/{total_tests}")
    
    if passed_tests == total_tests:
        print("\n🎉 All Phase 7 tests passed! System is ready for global expansion.")
        return True
    else:
        print(f"\n⚠️ {total_tests - passed_tests} tests failed. Please review and fix issues.")
        return False

if __name__ == "__main__":
    success = asyncio.run(main())
    sys.exit(0 if success else 1)
