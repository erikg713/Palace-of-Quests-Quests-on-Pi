// userRoutes.js

import React, { lazy } from 'react';
import { Navigate } from 'react-router-dom';
import { useAuth } from '../hooks/useAuth'; // Custom hook for authentication

// Lazy-loaded Components for Code Splitting
const UserProfile = lazy(() => import('../pages/Users/UserProfile'));
const UserSettings = lazy(() => import('../pages/Users/UserSettings'));
const Register = lazy(() => import('../pages/Users/Register'));
const Login = lazy(() => import('../pages/Users/Login'));
const UserSuccess = lazy(() => import('../pages/Users/UserSuccess'));
const UserFailure = lazy(() => import('../pages/Users/UserFailure'));
const AdminUserList = lazy(() => import('../pages/Users/AdminUserList'));
const AdminEditUser = lazy(() => import('../pages/Users/AdminEditUser'));

/**
 * ProtectedRoute Component
 * Ensures that only authenticated users can access certain routes.
 */
const ProtectedRoute = ({ children }) => {
    const { isAuthenticated } = useAuth();

    if (!isAuthenticated) {
        // Redirect to login page if not authenticated
        return <Navigate to="/login" replace />;
    }

    return children;
};

/**
 * AdminRoute Component
 * Ensures that only users with admin privileges can access certain routes.
 */
const AdminRoute = ({ children }) => {
    const { isAuthenticated, currentUser } = useAuth();

    if (!isAuthenticated) {
        // Redirect to login page if not authenticated
        return <Navigate to="/login" replace />;
    }

    if (currentUser.role !== 'admin') {
        // Redirect to unauthorized page or home if not an admin
        return <Navigate to="/unauthorized" replace />;
    }

    return children;
};

/**
 * User Routes Configuration
 * Defines all the routes related to users in the application.
 */
const userRoutes = [
    {
        path: '/register',
        element: <Register />,
        name: 'Register',
        exact: true,
    },
    {
        path: '/login',
        element: <Login />,
        name: 'Login',
        exact: true,
    },
    {
        path: '/profile',
        element: (
            <ProtectedRoute>
                <UserProfile />
            </ProtectedRoute>
        ),
        name: 'User Profile',
        exact: true,
    },
    {
        path: '/settings',
        element: (
            <ProtectedRoute>
                <UserSettings />
            </ProtectedRoute>
        ),
        name: 'User Settings',
        exact: true,
    },
    {
        path: '/user-success',
        element: <UserSuccess />,
        name: 'User Success',
        exact: true,
    },
    {
        path: '/user-failure',
        element: <UserFailure />,
        name: 'User Failure',
        exact: true,
    },
    // Admin Routes
    {
        path: '/admin/users',
        element: (
            <AdminRoute>
                <AdminUserList />
            </AdminRoute>
        ),
        name: 'Admin User List',
        exact: true,
    },
    {
        path: '/admin/users/edit/:userId',
        element: (
            <AdminRoute>
                <AdminEditUser />
            </AdminRoute>
        ),
        name: 'Admin Edit User',
        exact: true,
    },
];

export default userRoutes;
