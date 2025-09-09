/**
 * Fund Management Component for Pocket Hedge Fund React Dashboard
 * 
 * This component provides comprehensive fund management functionality
 * including listing, creating, editing, and monitoring funds.
 */

import React, { useState, useEffect, useCallback } from 'react';
import { Fund, FundDetails, FundType, FundStatus, RiskLevel } from '../types';
import { fundAPI } from '../services/api';
import { useAuth } from '../hooks/useAuth';

// ============================================================================
// FUND LIST COMPONENT
// ============================================================================

interface FundListProps {
  funds: Fund[];
  loading: boolean;
  onEdit: (fund: Fund) => void;
  onView: (fund: Fund) => void;
  onDelete: (fund: Fund) => void;
}

const FundList: React.FC<FundListProps> = ({ funds, loading, onEdit, onView, onDelete }) => {
  const { canManageFunds } = useAuth();

  const getStatusColor = (status: FundStatus) => {
    switch (status) {
      case 'active': return 'bg-green-100 text-green-800';
      case 'paused': return 'bg-yellow-100 text-yellow-800';
      case 'closed': return 'bg-red-100 text-red-800';
      case 'suspended': return 'bg-gray-100 text-gray-800';
      default: return 'bg-gray-100 text-gray-800';
    }
  };

  const getRiskColor = (risk: RiskLevel) => {
    switch (risk) {
      case 'low': return 'text-green-600';
      case 'medium': return 'text-yellow-600';
      case 'high': return 'text-red-600';
      default: return 'text-gray-600';
    }
  };

  const formatCurrency = (value: number) => {
    return new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency: 'USD',
      minimumFractionDigits: 0,
      maximumFractionDigits: 0
    }).format(value);
  };

  const formatPercentage = (value: number) => {
    return `${value.toFixed(2)}%`;
  };

  if (loading) {
    return (
      <div className="bg-white shadow rounded-lg">
        <div className="px-4 py-5 sm:p-6">
          <div className="animate-pulse">
            <div className="h-4 bg-gray-200 rounded w-1/4 mb-4"></div>
            <div className="space-y-3">
              {[1, 2, 3, 4, 5].map(i => (
                <div key={i} className="h-16 bg-gray-200 rounded"></div>
              ))}
            </div>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="bg-white shadow rounded-lg">
      <div className="px-4 py-5 sm:p-6">
        <h3 className="text-lg leading-6 font-medium text-gray-900 mb-4">
          Funds ({funds.length})
        </h3>
        
        {funds.length === 0 ? (
          <div className="text-center py-8">
            <div className="text-gray-400 text-6xl mb-4">🏦</div>
            <h3 className="text-lg font-medium text-gray-900 mb-2">No funds found</h3>
            <p className="text-gray-600">Get started by creating your first fund.</p>
          </div>
        ) : (
          <div className="overflow-hidden">
            <table className="min-w-full divide-y divide-gray-200">
              <thead className="bg-gray-50">
                <tr>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Fund
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Type
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Value
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Return
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Risk
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Status
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Actions
                  </th>
                </tr>
              </thead>
              <tbody className="bg-white divide-y divide-gray-200">
                {funds.map((fund) => {
                  const returnPercentage = ((fund.current_value - fund.initial_capital) / fund.initial_capital) * 100;
                  
                  return (
                    <tr key={fund.fund_id} className="hover:bg-gray-50">
                      <td className="px-6 py-4 whitespace-nowrap">
                        <div>
                          <div className="text-sm font-medium text-gray-900">{fund.name}</div>
                          <div className="text-sm text-gray-500">{fund.description}</div>
                        </div>
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap">
                        <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-blue-100 text-blue-800">
                          {fund.fund_type}
                        </span>
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                        {formatCurrency(fund.current_value)}
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm">
                        <span className={returnPercentage >= 0 ? 'text-green-600' : 'text-red-600'}>
                          {formatPercentage(returnPercentage)}
                        </span>
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm">
                        <span className={getRiskColor(fund.risk_level)}>
                          {fund.risk_level}
                        </span>
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap">
                        <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${getStatusColor(fund.status)}`}>
                          {fund.status}
                        </span>
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm font-medium">
                        <div className="flex space-x-2">
                          <button
                            onClick={() => onView(fund)}
                            className="text-blue-600 hover:text-blue-900"
                          >
                            View
                          </button>
                          {canManageFunds() && (
                            <>
                              <button
                                onClick={() => onEdit(fund)}
                                className="text-indigo-600 hover:text-indigo-900"
                              >
                                Edit
                              </button>
                              <button
                                onClick={() => onDelete(fund)}
                                className="text-red-600 hover:text-red-900"
                              >
                                Delete
                              </button>
                            </>
                          )}
                        </div>
                      </td>
                    </tr>
                  );
                })}
              </tbody>
            </table>
          </div>
        )}
      </div>
    </div>
  );
};

// ============================================================================
// FUND FORM COMPONENT
// ============================================================================

interface FundFormProps {
  fund?: Fund;
  onSubmit: (fundData: Partial<Fund>) => Promise<void>;
  onCancel: () => void;
  loading: boolean;
}

const FundForm: React.FC<FundFormProps> = ({ fund, onSubmit, onCancel, loading }) => {
  const [formData, setFormData] = useState({
    name: fund?.name || '',
    description: fund?.description || '',
    fund_type: fund?.fund_type || 'mini' as FundType,
    initial_capital: fund?.initial_capital || 100000,
    management_fee: fund?.management_fee || 0.02,
    performance_fee: fund?.performance_fee || 0.20,
    min_investment: fund?.min_investment || 1000,
    max_investment: fund?.max_investment || 10000,
    max_investors: fund?.max_investors || 100,
    risk_level: fund?.risk_level || 'medium' as RiskLevel
  });

  const [errors, setErrors] = useState<Record<string, string>>({});

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement | HTMLTextAreaElement>) => {
    const { name, value, type } = e.target;
    
    setFormData(prev => ({
      ...prev,
      [name]: type === 'number' ? parseFloat(value) || 0 : value
    }));

    // Clear error for this field
    if (errors[name]) {
      setErrors(prev => ({ ...prev, [name]: '' }));
    }
  };

  const validateForm = (): boolean => {
    const newErrors: Record<string, string> = {};

    if (!formData.name.trim()) {
      newErrors.name = 'Fund name is required';
    }

    if (formData.initial_capital <= 0) {
      newErrors.initial_capital = 'Initial capital must be greater than 0';
    }

    if (formData.min_investment <= 0) {
      newErrors.min_investment = 'Minimum investment must be greater than 0';
    }

    if (formData.max_investment && formData.max_investment < formData.min_investment) {
      newErrors.max_investment = 'Maximum investment must be greater than minimum investment';
    }

    if (formData.management_fee < 0 || formData.management_fee > 1) {
      newErrors.management_fee = 'Management fee must be between 0 and 1';
    }

    if (formData.performance_fee < 0 || formData.performance_fee > 1) {
      newErrors.performance_fee = 'Performance fee must be between 0 and 1';
    }

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!validateForm()) {
      return;
    }

    await onSubmit(formData);
  };

  return (
    <div className="bg-white shadow rounded-lg">
      <div className="px-4 py-5 sm:p-6">
        <h3 className="text-lg leading-6 font-medium text-gray-900 mb-4">
          {fund ? 'Edit Fund' : 'Create New Fund'}
        </h3>

        <form onSubmit={handleSubmit} className="space-y-6">
          <div className="grid grid-cols-1 gap-6 sm:grid-cols-2">
            {/* Fund Name */}
            <div>
              <label htmlFor="name" className="block text-sm font-medium text-gray-700">
                Fund Name *
              </label>
              <input
                type="text"
                name="name"
                id="name"
                value={formData.name}
                onChange={handleInputChange}
                className={`mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500 sm:text-sm ${errors.name ? 'border-red-300' : ''}`}
                placeholder="Enter fund name"
                disabled={loading}
              />
              {errors.name && <p className="mt-1 text-sm text-red-600">{errors.name}</p>}
            </div>

            {/* Fund Type */}
            <div>
              <label htmlFor="fund_type" className="block text-sm font-medium text-gray-700">
                Fund Type *
              </label>
              <select
                name="fund_type"
                id="fund_type"
                value={formData.fund_type}
                onChange={handleInputChange}
                className="mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
                disabled={loading}
              >
                <option value="mini">Mini ($1K - $10K)</option>
                <option value="standard">Standard ($10K - $100K)</option>
                <option value="premium">Premium ($100K - $1M)</option>
              </select>
            </div>
          </div>

          {/* Description */}
          <div>
            <label htmlFor="description" className="block text-sm font-medium text-gray-700">
              Description
            </label>
            <textarea
              name="description"
              id="description"
              rows={3}
              value={formData.description}
              onChange={handleInputChange}
              className="mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
              placeholder="Enter fund description"
              disabled={loading}
            />
          </div>

          <div className="grid grid-cols-1 gap-6 sm:grid-cols-3">
            {/* Initial Capital */}
            <div>
              <label htmlFor="initial_capital" className="block text-sm font-medium text-gray-700">
                Initial Capital *
              </label>
              <input
                type="number"
                name="initial_capital"
                id="initial_capital"
                value={formData.initial_capital}
                onChange={handleInputChange}
                className={`mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500 sm:text-sm ${errors.initial_capital ? 'border-red-300' : ''}`}
                placeholder="100000"
                disabled={loading}
              />
              {errors.initial_capital && <p className="mt-1 text-sm text-red-600">{errors.initial_capital}</p>}
            </div>

            {/* Min Investment */}
            <div>
              <label htmlFor="min_investment" className="block text-sm font-medium text-gray-700">
                Min Investment *
              </label>
              <input
                type="number"
                name="min_investment"
                id="min_investment"
                value={formData.min_investment}
                onChange={handleInputChange}
                className={`mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500 sm:text-sm ${errors.min_investment ? 'border-red-300' : ''}`}
                placeholder="1000"
                disabled={loading}
              />
              {errors.min_investment && <p className="mt-1 text-sm text-red-600">{errors.min_investment}</p>}
            </div>

            {/* Max Investment */}
            <div>
              <label htmlFor="max_investment" className="block text-sm font-medium text-gray-700">
                Max Investment
              </label>
              <input
                type="number"
                name="max_investment"
                id="max_investment"
                value={formData.max_investment}
                onChange={handleInputChange}
                className={`mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500 sm:text-sm ${errors.max_investment ? 'border-red-300' : ''}`}
                placeholder="10000"
                disabled={loading}
              />
              {errors.max_investment && <p className="mt-1 text-sm text-red-600">{errors.max_investment}</p>}
            </div>
          </div>

          <div className="grid grid-cols-1 gap-6 sm:grid-cols-3">
            {/* Management Fee */}
            <div>
              <label htmlFor="management_fee" className="block text-sm font-medium text-gray-700">
                Management Fee
              </label>
              <input
                type="number"
                name="management_fee"
                id="management_fee"
                step="0.01"
                min="0"
                max="1"
                value={formData.management_fee}
                onChange={handleInputChange}
                className={`mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500 sm:text-sm ${errors.management_fee ? 'border-red-300' : ''}`}
                placeholder="0.02"
                disabled={loading}
              />
              {errors.management_fee && <p className="mt-1 text-sm text-red-600">{errors.management_fee}</p>}
            </div>

            {/* Performance Fee */}
            <div>
              <label htmlFor="performance_fee" className="block text-sm font-medium text-gray-700">
                Performance Fee
              </label>
              <input
                type="number"
                name="performance_fee"
                id="performance_fee"
                step="0.01"
                min="0"
                max="1"
                value={formData.performance_fee}
                onChange={handleInputChange}
                className={`mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500 sm:text-sm ${errors.performance_fee ? 'border-red-300' : ''}`}
                placeholder="0.20"
                disabled={loading}
              />
              {errors.performance_fee && <p className="mt-1 text-sm text-red-600">{errors.performance_fee}</p>}
            </div>

            {/* Risk Level */}
            <div>
              <label htmlFor="risk_level" className="block text-sm font-medium text-gray-700">
                Risk Level
              </label>
              <select
                name="risk_level"
                id="risk_level"
                value={formData.risk_level}
                onChange={handleInputChange}
                className="mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
                disabled={loading}
              >
                <option value="low">Low</option>
                <option value="medium">Medium</option>
                <option value="high">High</option>
              </select>
            </div>
          </div>

          {/* Form Actions */}
          <div className="flex justify-end space-x-3">
            <button
              type="button"
              onClick={onCancel}
              className="bg-white py-2 px-4 border border-gray-300 rounded-md shadow-sm text-sm font-medium text-gray-700 hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
              disabled={loading}
            >
              Cancel
            </button>
            <button
              type="submit"
              className="bg-blue-600 py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 disabled:opacity-50"
              disabled={loading}
            >
              {loading ? 'Saving...' : (fund ? 'Update Fund' : 'Create Fund')}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};

// ============================================================================
// MAIN FUND MANAGEMENT COMPONENT
// ============================================================================

const FundManagement: React.FC = () => {
  const [funds, setFunds] = useState<Fund[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [showForm, setShowForm] = useState(false);
  const [editingFund, setEditingFund] = useState<Fund | undefined>();
  const [formLoading, setFormLoading] = useState(false);

  const { canManageFunds } = useAuth();

  // ============================================================================
  // DATA FETCHING
  // ============================================================================

  const fetchFunds = useCallback(async () => {
    try {
      setLoading(true);
      setError(null);
      
      const response = await fundAPI.getFunds({ page_size: 100 });
      setFunds(response.items);
    } catch (error) {
      console.error('Failed to fetch funds:', error);
      setError(error instanceof Error ? error.message : 'Failed to load funds');
    } finally {
      setLoading(false);
    }
  }, []);

  // ============================================================================
  // FORM HANDLERS
  // ============================================================================

  const handleCreateFund = () => {
    setEditingFund(undefined);
    setShowForm(true);
  };

  const handleEditFund = (fund: Fund) => {
    setEditingFund(fund);
    setShowForm(true);
  };

  const handleCancelForm = () => {
    setShowForm(false);
    setEditingFund(undefined);
  };

  const handleSubmitFund = async (fundData: Partial<Fund>) => {
    try {
      setFormLoading(true);
      
      if (editingFund) {
        await fundAPI.updateFund(editingFund.fund_id, fundData);
      } else {
        await fundAPI.createFund(fundData as any);
      }
      
      setShowForm(false);
      setEditingFund(undefined);
      await fetchFunds();
    } catch (error) {
      console.error('Failed to save fund:', error);
      setError(error instanceof Error ? error.message : 'Failed to save fund');
    } finally {
      setFormLoading(false);
    }
  };

  const handleDeleteFund = async (fund: Fund) => {
    if (!window.confirm(`Are you sure you want to delete "${fund.name}"?`)) {
      return;
    }

    try {
      await fundAPI.deleteFund(fund.fund_id);
      await fetchFunds();
    } catch (error) {
      console.error('Failed to delete fund:', error);
      setError(error instanceof Error ? error.message : 'Failed to delete fund');
    }
  };

  const handleViewFund = (fund: Fund) => {
    // Navigate to fund details page
    window.location.href = `/funds/${fund.fund_id}`;
  };

  // ============================================================================
  // EFFECTS
  // ============================================================================

  useEffect(() => {
    fetchFunds();
  }, [fetchFunds]);

  // ============================================================================
  // RENDER
  // ============================================================================

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">Fund Management</h1>
          <p className="text-gray-600">Manage your investment funds</p>
        </div>
        {canManageFunds() && (
          <button
            onClick={handleCreateFund}
            className="bg-blue-600 text-white px-4 py-2 rounded-md hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500"
          >
            Create Fund
          </button>
        )}
      </div>

      {/* Error Display */}
      {error && (
        <div className="bg-red-50 border border-red-200 rounded-md p-4">
          <div className="flex">
            <div className="flex-shrink-0">
              <svg className="h-5 w-5 text-red-400" viewBox="0 0 20 20" fill="currentColor">
                <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clipRule="evenodd" />
              </svg>
            </div>
            <div className="ml-3">
              <h3 className="text-sm font-medium text-red-800">Error</h3>
              <div className="mt-2 text-sm text-red-700">{error}</div>
            </div>
          </div>
        </div>
      )}

      {/* Content */}
      {showForm ? (
        <FundForm
          fund={editingFund}
          onSubmit={handleSubmitFund}
          onCancel={handleCancelForm}
          loading={formLoading}
        />
      ) : (
        <FundList
          funds={funds}
          loading={loading}
          onEdit={handleEditFund}
          onView={handleViewFund}
          onDelete={handleDeleteFund}
        />
      )}
    </div>
  );
};

export default FundManagement;
