/**
 * Redux slice for fund management state
 * 
 * This slice handles fund data, search, favorites,
 * and fund-related operations.
 */

import { createSlice, createAsyncThunk, PayloadAction } from '@reduxjs/toolkit';
import { Fund, FundDetails, FundState, ApiError } from '../types';
import { fundAPI } from '../services/api';

// ============================================================================
// ASYNC THUNKS
// ============================================================================

export const fetchFunds = createAsyncThunk(
  'fund/fetchFunds',
  async (params?: { fund_type?: string; status?: string; page?: number; page_size?: number }, { rejectWithValue }) => {
    try {
      const response = await fundAPI.getFunds(params);
      return response;
    } catch (error) {
      if (error instanceof ApiError) {
        return rejectWithValue({
          message: error.message,
          code: error.code,
          details: error.details
        });
      }
      return rejectWithValue({
        message: 'Failed to fetch funds',
        code: 500
      });
    }
  }
);

export const fetchFundDetails = createAsyncThunk(
  'fund/fetchFundDetails',
  async (fundId: string, { rejectWithValue }) => {
    try {
      const fund = await fundAPI.getFund(fundId);
      return fund;
    } catch (error) {
      if (error instanceof ApiError) {
        return rejectWithValue({
          message: error.message,
          code: error.code,
          details: error.details
        });
      }
      return rejectWithValue({
        message: 'Failed to fetch fund details',
        code: 500
      });
    }
  }
);

export const searchFunds = createAsyncThunk(
  'fund/searchFunds',
  async (query: string, { rejectWithValue }) => {
    try {
      const funds = await fundAPI.searchFunds(query);
      return funds;
    } catch (error) {
      if (error instanceof ApiError) {
        return rejectWithValue({
          message: error.message,
          code: error.code,
          details: error.details
        });
      }
      return rejectWithValue({
        message: 'Search failed',
        code: 500
      });
    }
  }
);

export const fetchTrendingFunds = createAsyncThunk(
  'fund/fetchTrendingFunds',
  async (_, { rejectWithValue }) => {
    try {
      const funds = await fundAPI.getTrendingFunds();
      return funds;
    } catch (error) {
      if (error instanceof ApiError) {
        return rejectWithValue({
          message: error.message,
          code: error.code,
          details: error.details
        });
      }
      return rejectWithValue({
        message: 'Failed to fetch trending funds',
        code: 500
      });
    }
  }
);

export const fetchFavoriteFunds = createAsyncThunk(
  'fund/fetchFavoriteFunds',
  async (_, { rejectWithValue }) => {
    try {
      const funds = await fundAPI.getFavoriteFunds();
      return funds;
    } catch (error) {
      if (error instanceof ApiError) {
        return rejectWithValue({
          message: error.message,
          code: error.code,
          details: error.details
        });
      }
      return rejectWithValue({
        message: 'Failed to fetch favorite funds',
        code: 500
      });
    }
  }
);

export const addToFavorites = createAsyncThunk(
  'fund/addToFavorites',
  async (fundId: string, { rejectWithValue }) => {
    try {
      await fundAPI.addToFavorites(fundId);
      return fundId;
    } catch (error) {
      if (error instanceof ApiError) {
        return rejectWithValue({
          message: error.message,
          code: error.code,
          details: error.details
        });
      }
      return rejectWithValue({
        message: 'Failed to add to favorites',
        code: 500
      });
    }
  }
);

export const removeFromFavorites = createAsyncThunk(
  'fund/removeFromFavorites',
  async (fundId: string, { rejectWithValue }) => {
    try {
      await fundAPI.removeFromFavorites(fundId);
      return fundId;
    } catch (error) {
      if (error instanceof ApiError) {
        return rejectWithValue({
          message: error.message,
          code: error.code,
          details: error.details
        });
      }
      return rejectWithValue({
        message: 'Failed to remove from favorites',
        code: 500
      });
    }
  }
);

// ============================================================================
// INITIAL STATE
// ============================================================================

const initialState: FundState = {
  funds: [],
  selectedFund: null,
  isLoading: false,
  error: null,
  lastUpdated: null,
  searchResults: [],
  trendingFunds: [],
  favoriteFunds: [],
  searchQuery: ''
};

// ============================================================================
// FUND SLICE
// ============================================================================

const fundSlice = createSlice({
  name: 'fund',
  initialState,
  reducers: {
    clearError: (state) => {
      state.error = null;
    },
    setSelectedFund: (state, action: PayloadAction<Fund | null>) => {
      state.selectedFund = action.payload;
    },
    setSearchQuery: (state, action: PayloadAction<string>) => {
      state.searchQuery = action.payload;
    },
    clearSearchResults: (state) => {
      state.searchResults = [];
      state.searchQuery = '';
    },
    updateFundInList: (state, action: PayloadAction<Fund>) => {
      const index = state.funds.findIndex(fund => fund.fund_id === action.payload.fund_id);
      if (index !== -1) {
        state.funds[index] = action.payload;
      }
    }
  },
  extraReducers: (builder) => {
    // Fetch Funds
    builder
      .addCase(fetchFunds.pending, (state) => {
        state.isLoading = true;
        state.error = null;
      })
      .addCase(fetchFunds.fulfilled, (state, action) => {
        state.isLoading = false;
        state.funds = action.payload.items;
        state.lastUpdated = new Date().toISOString();
        state.error = null;
      })
      .addCase(fetchFunds.rejected, (state, action) => {
        state.isLoading = false;
        state.error = action.payload?.message || 'Failed to fetch funds';
      });

    // Fetch Fund Details
    builder
      .addCase(fetchFundDetails.pending, (state) => {
        state.isLoading = true;
        state.error = null;
      })
      .addCase(fetchFundDetails.fulfilled, (state, action) => {
        state.isLoading = false;
        state.selectedFund = action.payload;
        state.error = null;
      })
      .addCase(fetchFundDetails.rejected, (state, action) => {
        state.isLoading = false;
        state.error = action.payload?.message || 'Failed to fetch fund details';
      });

    // Search Funds
    builder
      .addCase(searchFunds.pending, (state) => {
        state.isLoading = true;
        state.error = null;
      })
      .addCase(searchFunds.fulfilled, (state, action) => {
        state.isLoading = false;
        state.searchResults = action.payload;
        state.error = null;
      })
      .addCase(searchFunds.rejected, (state, action) => {
        state.isLoading = false;
        state.error = action.payload?.message || 'Search failed';
      });

    // Fetch Trending Funds
    builder
      .addCase(fetchTrendingFunds.fulfilled, (state, action) => {
        state.trendingFunds = action.payload;
      })
      .addCase(fetchTrendingFunds.rejected, (state, action) => {
        state.error = action.payload?.message || 'Failed to fetch trending funds';
      });

    // Fetch Favorite Funds
    builder
      .addCase(fetchFavoriteFunds.fulfilled, (state, action) => {
        state.favoriteFunds = action.payload;
      })
      .addCase(fetchFavoriteFunds.rejected, (state, action) => {
        state.error = action.payload?.message || 'Failed to fetch favorite funds';
      });

    // Add to Favorites
    builder
      .addCase(addToFavorites.fulfilled, (state, action) => {
        const fundId = action.payload;
        const fund = state.funds.find(f => f.fund_id === fundId);
        if (fund) {
          state.favoriteFunds.push(fund);
        }
      })
      .addCase(addToFavorites.rejected, (state, action) => {
        state.error = action.payload?.message || 'Failed to add to favorites';
      });

    // Remove from Favorites
    builder
      .addCase(removeFromFavorites.fulfilled, (state, action) => {
        const fundId = action.payload;
        state.favoriteFunds = state.favoriteFunds.filter(f => f.fund_id !== fundId);
      })
      .addCase(removeFromFavorites.rejected, (state, action) => {
        state.error = action.payload?.message || 'Failed to remove from favorites';
      });
  }
});

// ============================================================================
// SELECTORS
// ============================================================================

export const selectFunds = (state: { fund: FundState }) => state.fund.funds;
export const selectSelectedFund = (state: { fund: FundState }) => state.fund.selectedFund;
export const selectFundLoading = (state: { fund: FundState }) => state.fund.isLoading;
export const selectFundError = (state: { fund: FundState }) => state.fund.error;
export const selectSearchResults = (state: { fund: FundState }) => state.fund.searchResults;
export const selectTrendingFunds = (state: { fund: FundState }) => state.fund.trendingFunds;
export const selectFavoriteFunds = (state: { fund: FundState }) => state.fund.favoriteFunds;
export const selectSearchQuery = (state: { fund: FundState }) => state.fund.searchQuery;

// ============================================================================
// EXPORTS
// ============================================================================

export const { 
  clearError, 
  setSelectedFund, 
  setSearchQuery, 
  clearSearchResults, 
  updateFundInList 
} = fundSlice.actions;

export default fundSlice.reducer;
