// orderRoutes.js

import React, { lazy } from 'react';
import { Navigate } from 'react-router-dom';
import { useAuth } from '../hooks/useAuth'; // Custom hook for authentication

// Lazy-loaded Components for Code Splitting
const OrderList = lazy(() => import('../pages/Orders/OrderList'));
const OrderDetails = lazy(() => import('../pages/Orders/OrderDetails'));
const Checkout = lazy(() => import('../pages/Orders/Checkout'));
const PaymentSuccess = lazy(() => import('../pages/Orders/PaymentSuccess'));
const PaymentFailure = lazy(() => import('../pages/Orders/PaymentFailure'));

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
 * Order Routes Configuration
 * Defines all the routes related to orders in the application.
 */
const orderRoutes = [
    {
        path: '/orders',
        element: (
            <ProtectedRoute>
                <OrderList />
            </ProtectedRoute>
        ),
        name: 'Order List',
        exact: true,
    },
    {
        path: '/orders/:orderId',
        element: (
            <ProtectedRoute>
                <OrderDetails />
            </ProtectedRoute>
        ),
        name: 'Order Details',
        exact: true,
    },
    {
        path: '/checkout',
        element: (
            <ProtectedRoute>
                <Checkout />
            </ProtectedRoute>
        ),
        name: 'Checkout',
        exact: true,
    },
    {
        path: '/payment-success',
        element: <PaymentSuccess />,
        name: 'Payment Success',
        exact: true,
    },
    {
        path: '/payment-failure',
        element: <PaymentFailure />,
        name: 'Payment Failure',
        exact: true,
    },
];

export default orderRoutes;
