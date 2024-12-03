// error.js

/**
 * Error Handling Middleware
 * Captures errors from Redux actions and dispatches error-related actions.
 */

import { logoutUser } from '../slices/userSlice';
import { setError, clearError } from '../slices/errorSlice';

/**
 * Error Middleware
 * Intercepts actions with errors and handles them appropriately.
 */
const errorMiddleware = (store) => (next) => (action) => {
    // Check if the action is a rejected async thunk
    if (action.type.endsWith('rejected')) {
        // Extract error message from the action payload or fallback to a generic message
        const errorMessage =
            action.payload?.message ||
            action.error?.message ||
            'An unknown error occurred';

        // Dispatch the error to the error slice
        store.dispatch(setError(errorMessage));

        // Optionally, handle specific error statuses
        if (action.payload?.status === 401) {
            // Unauthorized error, logout the user
            store.dispatch(logoutUser());
            // Redirect to login page
            window.location.href = '/login';
        }
    }

    // Pass all actions through to the next middleware or reducer
    return next(action);
};

export default errorMiddleware;
