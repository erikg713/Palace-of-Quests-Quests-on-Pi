// paymentRoutes.js

import React, { lazy } from 'react';
import { Navigate } from 'react-router-dom';
import { useAuth } from '../hooks/useAuth';

// Lazy-loaded Components for Performance Optimization
const PaymentList = lazy(() => import('../pages/Payments/PaymentList'));
const PaymentDetails = lazy(() => import('../pages/Payments/PaymentDetails'));
const InitiatePayment = lazy(() => import('../pages/Payments/InitiatePayment'));
const PaymentSuccess = lazy(() => import('../pages/Payments/PaymentSuccess'));
const PaymentFailure = lazy(() => import('../pages/Payments/PaymentFailure'));

/**
 * ProtectedRoute Component
 * Restricts access to authenticated users only.
 */
const ProtectedRoute = ({ children }) => {
    const { isAuthenticated } = useAuth();

    if (!isAuthenticated) {
        return <Navigate to="/login" replace />;
    }
    return children;
};

/**
 * Payment Routes Configuration
 * Defines all payment-related routes with appropriate protection.
 */
const paymentRoutes = [
    {
        path: '/payments',
        element: (
            <ProtectedRoute>
                <PaymentList />
            </ProtectedRoute>
        ),
        name: 'Payment List',
        exact: true,
    },
    {
        path: '/payments/:paymentId',
        element: (
            <ProtectedRoute>
                <PaymentDetails />
            </ProtectedRoute>
        ),
        name: 'Payment Details',
        exact: true,
    },
    {
        path: '/payments/initiate',
        element: (
            <ProtectedRoute>
                <InitiatePayment />
            </ProtectedRoute>
        ),
        name: 'Initiate Payment',
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

export default paymentRoutes;
