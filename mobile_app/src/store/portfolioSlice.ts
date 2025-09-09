/**
 * Redux slice for portfolio state management
 * 
 * This slice handles portfolio positions, performance,
 * and portfolio-related operations.
 */

import { createSlice, createAsyncThunk, PayloadAction } from '@reduxjs/toolkit';
import { PortfolioPosition, PortfolioState, ApiError } from '../types';
import { portfolioAPI } from '../services/api';

// ============================================================================
// ASYNC THUNKS
// ============================================================================

export const fetchUserPortfolio = createAsyncThunk(
  'portfolio/fetchUserPortfolio',
  async (_, { rejectWithValue }) => {
    try {
      const portfolio = await portfolioAPI.getUserPortfolio();
      return portfolio;
    } catch (error) {
      if (error instanceof ApiError) {
        return rejectWithValue({
          message: error.message,
          code: error.code,
          details: error.details
        });
      }
      return rejectWithValue({
        message: 'Failed to fetch portfolio',
        code: 500
      });
    }
  }
);

export const fetchPortfolioPositions = createAsyncThunk(
  'portfolio/fetchPortfolioPositions',
  async (fundId: string, { rejectWithValue }) => {
    try {
      const positions = await portfolioAPI.getPositions(fundId);
      return positions;
    } catch (error) {
      if (error instanceof ApiError) {
        return rejectWithValue({
          message: error.message,
          code: error.code,
          details: error.details
        });
      }
      return rejectWithValue({
        message: 'Failed to fetch portfolio positions',
        code: 500
      });
    }
  }
);

export const fetchPortfolioPerformance = createAsyncThunk(
  'portfolio/fetchPortfolioPerformance',
  async (days: number = 30, { rejectWithValue }) => {
    try {
      const performance = await portfolioAPI.getPortfolioPerformance(days);
      return performance;
    } catch (error) {
      if (error instanceof ApiError) {
        return rejectWithValue({
          message: error.message,
          code: error.code,
          details: error.details
        });
      }
      return rejectWithValue({
        message: 'Failed to fetch portfolio performance',
        code: 500
      });
    }
  }
);

// ============================================================================
// INITIAL STATE
// ============================================================================

const initialState: PortfolioState = {
  positions: [],
  totalValue: 0,
  totalReturn: 0,
  totalReturnPercentage: 0,
  isLoading: false,
  error: null,
  performance: [],
  lastUpdated: null
};

// ============================================================================
// PORTFOLIO SLICE
// ============================================================================

const portfolioSlice = createSlice({
  name: 'portfolio',
  initialState,
  reducers: {
    clearError: (state) => {
      state.error = null;
    },
    updatePosition: (state, action: PayloadAction<PortfolioPosition>) => {
      const index = state.positions.findIndex(
        pos => pos.asset_symbol === action.payload.asset_symbol
      );
      if (index !== -1) {
        state.positions[index] = action.payload;
      } else {
        state.positions.push(action.payload);
      }
    },
    removePosition: (state, action: PayloadAction<string>) => {
      state.positions = state.positions.filter(
        pos => pos.asset_symbol !== action.payload
      );
    },
    clearPortfolio: (state) => {
      state.positions = [];
      state.totalValue = 0;
      state.totalReturn = 0;
      state.totalReturnPercentage = 0;
      state.performance = [];
    }
  },
  extraReducers: (builder) => {
    // Fetch User Portfolio
    builder
      .addCase(fetchUserPortfolio.pending, (state) => {
        state.isLoading = true;
        state.error = null;
      })
      .addCase(fetchUserPortfolio.fulfilled, (state, action) => {
        state.isLoading = false;
        state.positions = action.payload.positions;
        state.totalValue = action.payload.total_value;
        state.totalReturn = action.payload.total_return;
        state.totalReturnPercentage = action.payload.total_return_percentage;
        state.lastUpdated = new Date().toISOString();
        state.error = null;
      })
      .addCase(fetchUserPortfolio.rejected, (state, action) => {
        state.isLoading = false;
        state.error = action.payload?.message || 'Failed to fetch portfolio';
      });

    // Fetch Portfolio Positions
    builder
      .addCase(fetchPortfolioPositions.pending, (state) => {
        state.isLoading = true;
        state.error = null;
      })
      .addCase(fetchPortfolioPositions.fulfilled, (state, action) => {
        state.isLoading = false;
        state.positions = action.payload;
        state.lastUpdated = new Date().toISOString();
        state.error = null;
      })
      .addCase(fetchPortfolioPositions.rejected, (state, action) => {
        state.isLoading = false;
        state.error = action.payload?.message || 'Failed to fetch positions';
      });

    // Fetch Portfolio Performance
    builder
      .addCase(fetchPortfolioPerformance.pending, (state) => {
        state.isLoading = true;
        state.error = null;
      })
      .addCase(fetchPortfolioPerformance.fulfilled, (state, action) => {
        state.isLoading = false;
        state.performance = action.payload;
        state.error = null;
      })
      .addCase(fetchPortfolioPerformance.rejected, (state, action) => {
        state.isLoading = false;
        state.error = action.payload?.message || 'Failed to fetch performance';
      });
  }
});

// ============================================================================
// SELECTORS
// ============================================================================

export const selectPortfolio = (state: { portfolio: PortfolioState }) => state.portfolio;
export const selectPositions = (state: { portfolio: PortfolioState }) => state.portfolio.positions;
export const selectTotalValue = (state: { portfolio: PortfolioState }) => state.portfolio.totalValue;
export const selectTotalReturn = (state: { portfolio: PortfolioState }) => state.portfolio.totalReturn;
export const selectTotalReturnPercentage = (state: { portfolio: PortfolioState }) => state.portfolio.totalReturnPercentage;
export const selectPortfolioLoading = (state: { portfolio: PortfolioState }) => state.portfolio.isLoading;
export const selectPortfolioError = (state: { portfolio: PortfolioState }) => state.portfolio.error;
export const selectPerformance = (state: { portfolio: PortfolioState }) => state.portfolio.performance;

// ============================================================================
// EXPORTS
// ============================================================================

export const { 
  clearError, 
  updatePosition, 
  removePosition, 
  clearPortfolio 
} = portfolioSlice.actions;

export default portfolioSlice.reducer;
