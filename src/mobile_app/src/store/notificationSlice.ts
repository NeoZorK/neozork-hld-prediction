/**
 * Redux slice for notification state management
 * 
 * This slice handles push notifications, in-app notifications,
 * and notification settings.
 */

import { createSlice, createAsyncThunk, PayloadAction } from '@reduxjs/toolkit';
import { NotificationData, NotificationState, ApiError } from '../types';
import { notificationAPI } from '../services/api';

// ============================================================================
// ASYNC THUNKS
// ============================================================================

export const fetchNotifications = createAsyncThunk(
  'notification/fetchNotifications',
  async (params?: { page?: number; page_size?: number; unread_only?: boolean }, { rejectWithValue }) => {
    try {
      const response = await notificationAPI.getNotifications(params);
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
        message: 'Failed to fetch notifications',
        code: 500
      });
    }
  }
);

export const markNotificationAsRead = createAsyncThunk(
  'notification/markAsRead',
  async (notificationId: string, { rejectWithValue }) => {
    try {
      await notificationAPI.markAsRead(notificationId);
      return notificationId;
    } catch (error) {
      if (error instanceof ApiError) {
        return rejectWithValue({
          message: error.message,
          code: error.code,
          details: error.details
        });
      }
      return rejectWithValue({
        message: 'Failed to mark notification as read',
        code: 500
      });
    }
  }
);

export const markAllNotificationsAsRead = createAsyncThunk(
  'notification/markAllAsRead',
  async (_, { rejectWithValue }) => {
    try {
      await notificationAPI.markAllAsRead();
      return true;
    } catch (error) {
      if (error instanceof ApiError) {
        return rejectWithValue({
          message: error.message,
          code: error.code,
          details: error.details
        });
      }
      return rejectWithValue({
        message: 'Failed to mark all notifications as read',
        code: 500
      });
    }
  }
);

export const deleteNotification = createAsyncThunk(
  'notification/deleteNotification',
  async (notificationId: string, { rejectWithValue }) => {
    try {
      await notificationAPI.deleteNotification(notificationId);
      return notificationId;
    } catch (error) {
      if (error instanceof ApiError) {
        return rejectWithValue({
          message: error.message,
          code: error.code,
          details: error.details
        });
      }
      return rejectWithValue({
        message: 'Failed to delete notification',
        code: 500
      });
    }
  }
);

export const updatePushSettings = createAsyncThunk(
  'notification/updatePushSettings',
  async (settings: {
    enabled: boolean;
    fund_updates: boolean;
    investment_alerts: boolean;
    performance_notifications: boolean;
    system_announcements: boolean;
  }, { rejectWithValue }) => {
    try {
      await notificationAPI.updatePushSettings(settings);
      return settings;
    } catch (error) {
      if (error instanceof ApiError) {
        return rejectWithValue({
          message: error.message,
          code: error.code,
          details: error.details
        });
      }
      return rejectWithValue({
        message: 'Failed to update push settings',
        code: 500
      });
    }
  }
);

// ============================================================================
// INITIAL STATE
// ============================================================================

const initialState: NotificationState = {
  notifications: [],
  unreadCount: 0,
  isLoading: false,
  error: null,
  pushSettings: {
    enabled: true,
    fund_updates: true,
    investment_alerts: true,
    performance_notifications: true,
    system_announcements: true
  }
};

// ============================================================================
// NOTIFICATION SLICE
// ============================================================================

const notificationSlice = createSlice({
  name: 'notification',
  initialState,
  reducers: {
    clearError: (state) => {
      state.error = null;
    },
    addNotification: (state, action: PayloadAction<NotificationData>) => {
      state.notifications.unshift(action.payload);
      if (!action.payload.read) {
        state.unreadCount += 1;
      }
    },
    removeNotification: (state, action: PayloadAction<string>) => {
      const notification = state.notifications.find(n => n.id === action.payload);
      if (notification && !notification.read) {
        state.unreadCount = Math.max(0, state.unreadCount - 1);
      }
      state.notifications = state.notifications.filter(n => n.id !== action.payload);
    },
    markAsRead: (state, action: PayloadAction<string>) => {
      const notification = state.notifications.find(n => n.id === action.payload);
      if (notification && !notification.read) {
        notification.read = true;
        state.unreadCount = Math.max(0, state.unreadCount - 1);
      }
    },
    clearAllNotifications: (state) => {
      state.notifications = [];
      state.unreadCount = 0;
    },
    updateUnreadCount: (state, action: PayloadAction<number>) => {
      state.unreadCount = action.payload;
    }
  },
  extraReducers: (builder) => {
    // Fetch Notifications
    builder
      .addCase(fetchNotifications.pending, (state) => {
        state.isLoading = true;
        state.error = null;
      })
      .addCase(fetchNotifications.fulfilled, (state, action) => {
        state.isLoading = false;
        state.notifications = action.payload.items;
        state.unreadCount = action.payload.items.filter(n => !n.read).length;
        state.error = null;
      })
      .addCase(fetchNotifications.rejected, (state, action) => {
        state.isLoading = false;
        state.error = action.payload?.message || 'Failed to fetch notifications';
      });

    // Mark Notification as Read
    builder
      .addCase(markNotificationAsRead.fulfilled, (state, action) => {
        const notification = state.notifications.find(n => n.id === action.payload);
        if (notification && !notification.read) {
          notification.read = true;
          state.unreadCount = Math.max(0, state.unreadCount - 1);
        }
      })
      .addCase(markNotificationAsRead.rejected, (state, action) => {
        state.error = action.payload?.message || 'Failed to mark notification as read';
      });

    // Mark All Notifications as Read
    builder
      .addCase(markAllNotificationsAsRead.fulfilled, (state) => {
        state.notifications.forEach(notification => {
          notification.read = true;
        });
        state.unreadCount = 0;
      })
      .addCase(markAllNotificationsAsRead.rejected, (state, action) => {
        state.error = action.payload?.message || 'Failed to mark all notifications as read';
      });

    // Delete Notification
    builder
      .addCase(deleteNotification.fulfilled, (state, action) => {
        const notification = state.notifications.find(n => n.id === action.payload);
        if (notification && !notification.read) {
          state.unreadCount = Math.max(0, state.unreadCount - 1);
        }
        state.notifications = state.notifications.filter(n => n.id !== action.payload);
      })
      .addCase(deleteNotification.rejected, (state, action) => {
        state.error = action.payload?.message || 'Failed to delete notification';
      });

    // Update Push Settings
    builder
      .addCase(updatePushSettings.fulfilled, (state, action) => {
        state.pushSettings = action.payload;
      })
      .addCase(updatePushSettings.rejected, (state, action) => {
        state.error = action.payload?.message || 'Failed to update push settings';
      });
  }
});

// ============================================================================
// SELECTORS
// ============================================================================

export const selectNotifications = (state: { notification: NotificationState }) => state.notification.notifications;
export const selectUnreadCount = (state: { notification: NotificationState }) => state.notification.unreadCount;
export const selectNotificationLoading = (state: { notification: NotificationState }) => state.notification.isLoading;
export const selectNotificationError = (state: { notification: NotificationState }) => state.notification.error;
export const selectPushSettings = (state: { notification: NotificationState }) => state.notification.pushSettings;

// ============================================================================
// EXPORTS
// ============================================================================

export const { 
  clearError, 
  addNotification, 
  removeNotification, 
  markAsRead, 
  clearAllNotifications, 
  updateUnreadCount 
} = notificationSlice.actions;

export default notificationSlice.reducer;
